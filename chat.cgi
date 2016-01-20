#!/usr/bin/ruby

require_relative "html"
require "csv"
require "cgi"
require 'cgi/session'
$cgi = CGI.new
$session = CGI::Session.new($cgi)

h = HTML.new("Supportchat")
unless $session.session_id =~ /^[a-f0-9]+/
	$session.delete
	h.header["status"] = "REDIRECT"
	h.header["Cache-Control"] = "no-cache"
	h.header["Location"] = "/login.cgi"
else

	if $cgi.include?("message") && $cgi["message"] != ""
		t = Time.new.to_i
		File.open("chat/#{$session.session_id}","a"){|f|
			f << "#{t},#{$cgi["message"]}\n"
		}
require "yaml"
		user = "xaver"
		pass = YAML::load_file("users/#{user}.yaml")[:password]
		`./admin/chat.js #{$cgi.server_name} #{user} #{pass} #{$session.session_id} #{t}`
	end

h << <<CONTENT
<form method='POST'>
<input type="text" name="message" placeholder="Message" size="30" />
<input type="submit" name="Send" value="Send message"/>
</form>
CONTENT

if File.exist?("chat/#{$session.session_id}")
	File.open("chat/#{$session.session_id}").each_line{|l|
		message = l.scan(/^[0-9]+,(.*)/).flatten[0]
		h << "<div><b>User:</b> #{message}"
	}
end


end
h.out($cgi)
