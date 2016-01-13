#!/usr/bin/ruby

require_relative "html"
require "csv"
require "cgi"
require 'cgi/session'
$cgi = CGI.new
$session = CGI::Session.new($cgi)

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
</form>
</div>
CONTENT


if $cgi.include?("pic_url")
	File.open('pics.csv', 'a') { |f|
		f.puts "\"#{$session.session_id}\",\"#{$cgi["pic_url"].gsub("\"","")}\""
	}
end
if $cgi.include?("delete")
	File.open('delete.csv', 'a') { |f|
		f.puts "\"#{$session.session_id}\",\"#{$cgi["delete"].gsub("\"","")}\""
	}
end

h << "<div style='margin:10px'>"
pics = CSV.read("pics.csv",{headers: true, col_sep: ","})
del = CSV.read("delete.csv",{headers: true, col_sep: ","}).to_a

pics.reverse_each{|l|
		unless del.include?([l["sid"],l["url"]])
			if (!(l["url"] =~ /^https?:\/\/mail.*\.mgm-sp\.com\//)) ||
					l["sid"] == $session.session_id ||
					$cgi.include?("all_pics")

				h << "<div>"
				if l["sid"] == $session.session_id
					h << "<div style='position: absolute;'>"
					h << "<form method='POST'>"
					h << "<input type='submit' value='Delete' />"
					h << "<input type='hidden' name='delete' value=\"#{CGI.escapeHTML(l["url"])}\" />"
					h << "</form></div>"
				end
				h << "<img src='#{l["url"].gsub("'","")}' width='500' />"
				h << "</div>"
			end
		end
}
h << "</div>"

h.out($cgi)
