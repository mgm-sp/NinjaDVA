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

h << "<div style='margin:10px'>"
pics = CSV.read("pics.csv",{headers: true, col_sep: ","})

pics.reverse_each{|l|
	if (!(l["url"] =~ /^https?:\/\/dvmail.*\.mgm-sp\.com\//)) || l["sid"] == $session.session_id || $cgi.include?("all_pics")
		h << "<img src='#{l["url"].gsub("'","")}' height='200' />"
	end
}
h << "</div>"

h.out($cgi)
