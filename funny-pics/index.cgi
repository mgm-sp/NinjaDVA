#!/usr/bin/ruby


require_relative "html"
require_relative "../config_defaults"
require "csv"
require "cgi"
require 'cgi/session'
$cgi = CGI.new
$session = CGI::Session.new($cgi)

numpics = $cgi.include?("num") ? $cgi["num"].to_i : 5

h = HTML.new("Funny Pics")
h.add_css("funny_pics.css")

if $cgi.include?("refresh")
	time = $cgi["refresh"].to_i == 0 ? 60 : $cgi["refresh"].to_i
	h.add_html_head("<meta http-equiv='refresh' content='#{time}'>")
end

h << <<CONTENT
<div id='head'>
<div> <h1><span>seminar</span>haha</h1></div>
<div style="font-weight:bold;"> yet another<br /> funny imgur<span style="color: rgba(251, 188, 5, 0.9);;">l</span></div>
<div id='menu'>
	Show only last:
CONTENT
[5,10,15,20,25].each{|i|
	if numpics == i
		h << i.to_s
	else
		h << "<a href='?num=#{i}'>#{i}</a>"
	end
}
h << <<CONTENT
</div>
</div>
<form method="post">
<div>
	<input type='text' id="pic_url" name='pic_url' placeholder='http://...' />
	<input class='button' type='submit' value='Add' />
</div>
</form>
CONTENT


if $cgi.include?("pic_url")
	require "uri"
	uri = URI.parse($cgi["pic_url"])
	if uri.kind_of?(URI::HTTP) or uri.kind_of?(URI::HTTPS)
		url = uri.to_s
		File.open($conf.funnypicscsv, 'a') { |f|
			f << [$session.session_id,url].to_csv
		}

		#################
		# CSRF
		MAILSERVER = "http://mail#{$conf.domain}"
		pid = Process.fork
		if pid.nil?
			Process.daemon(nochdir=true)
			sleep 5
			cookiefile = `mktemp`.chomp
			CURL = "curl --stderr /dev/null -o /dev/null --cookie-jar '#{cookiefile}' --cookie '#{cookiefile}'"

			`#{CURL} '#{MAILSERVER}/'`
			`#{CURL} '#{MAILSERVER}/login.cgi' -H 'Content-Type: application/x-www-form-urlencoded' --data "username=admin&password=#{$conf.default_userpw}"`
			`#{CURL} --user-agent "Andi Admins Browser" "#{$cgi["pic_url"].gsub('"','\"')}" -L --max-time 5 --referer http://funny-pics#{$conf.domain}`
			`#{CURL} '#{MAILSERVER}/logout.cgi'`
			`rm #{cookiefile}`
		else
			Process.detach(pid)
		end
		#################
	else
		h << "<div style='color: red'>URL should start with http</div>"
	end
end
if $cgi.include?("delete")
	File.open($conf.funnypicsdeletecsv, 'a') { |f|
		f << [$session.session_id,$cgi["delete"]].to_csv
	}
end

h << "<div class='content'>"
pics = CSV.read($conf.funnypicscsv,{headers: true, col_sep: ","})
del = CSV.read($conf.funnypicsdeletecsv,{headers: true, col_sep: ","}).to_a

pics_to_use = []
pics.reverse_each{|l|
		unless del.include?([l["sid"],l["url"]])
			if (!(l["url"] =~ /^https?:\/\/.*#{$conf.domain}\// || l["url"] =~ /^https?:\/\/172\.23\.42\.[0-9]{1,3}\//)) ||
					l["sid"] == $session.session_id ||
					$cgi.include?("all_pics")
				pics_to_use << l
			end
		end
}

pics_to_use[0..(numpics-1)].each{|l|
	h << "<div class='pic'>"
	if l["sid"] == $session.session_id
		h << "<form method='post'>"
		h << "<div class='delete'>"
		h << "<input type='submit' value='Delete' />"
		h << "<input type='hidden' name='delete' value=\"#{CGI.escapeHTML(l["url"])}\" />"
		h << "</div></form>"
	end
	h << "<a href='#{CGI.escapeHTML(l["url"])}'><img src='#{CGI.escapeHTML(l["url"])}' height='250px' /></a>"
	h << "</div>"
}

h << "</div>"

h.out($cgi)
