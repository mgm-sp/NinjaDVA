#!/usr/bin/ruby

require_relative "html"
require "csv"
require "cgi"
require 'cgi/session'
$cgi = CGI.new
$session = CGI::Session.new($cgi)

numpics = $cgi.include?("num") ? $cgi["num"].to_i : 10

h = HTML.new("Funny Pics")

if $cgi.include?("refresh")
	time = $cgi["refresh"].to_i == 0 ? 60 : $cgi["refresh"].to_i
	h.add_html_head("<meta http-equiv='refresh' content='#{time}'>")
end

h << <<CONTENT
<div>
<form method="POST">
This Picture URL is really funny:
	<input type='text' name='pic_url' placeholder='http://...'/>
	<input type='submit' />
	Show only last:
CONTENT
[5,10,15,20,25].each{|i|
	if numpics == i
		h << i.to_s
	else
		h << "<a href='?num=#{i}' />#{i}</a>"
	end
}
h << <<CONTENT
</form>
</div>
CONTENT


if $cgi.include?("pic_url")
	if $cgi["pic_url"] =~ /^https?:\/\//
		File.open('pics.csv', 'a') { |f|
			f << [$session.session_id,$cgi["pic_url"]].to_csv
		}
	else
		h << "<div style='color: red'>URL should start with http</div>"
	end
end
if $cgi.include?("delete")
	File.open('delete.csv', 'a') { |f|
		f << [$session.session_id,$cgi["delete"]].to_csv
	}
end

h << "<div style='margin:10px'>"
pics = CSV.read("pics.csv",{headers: true, col_sep: ","})
del = CSV.read("delete.csv",{headers: true, col_sep: ","}).to_a

pics_to_use = []
pics.reverse_each{|l|
		unless del.include?([l["sid"],l["url"]])
			if (!(l["url"] =~ /^https?:\/\/*\.mgmsp-lab\.com\// || l["url"] =~ /^https?:\/\/172\.23\.42\.[0-9]{1,3}\//)) ||
					l["sid"] == $session.session_id ||
					$cgi.include?("all_pics")
				pics_to_use << l
			end
		end
}

pics_to_use[0..(numpics-1)].each{|l|
	h << "<div style='display: inline-block; min-width: 10em'>"
	if l["sid"] == $session.session_id
		h << "<div style='position: absolute;'>"
		h << "<form method='POST'>"
		h << "<input type='submit' value='Delete' />"
		h << "<input type='hidden' name='delete' value=\"#{CGI.escapeHTML(l["url"])}\" />"
		h << "</form></div>"
	end
	h << "<img src='#{CGI.escapeHTML(l["url"])}' height='250px' />"
	h << "</div>"
}

h << "</div>"

h.out($cgi)
