#!/usr/bin/ruby

require_relative "html"
require "csv"
require "cgi"
require 'cgi/session'
$cgi = CGI.new
$session = CGI::Session.new($cgi)

h = HTML.new("Supportchat")
unless $session.session_id =~ /\A[a-f0-9]+\Z/
	$session.delete
	h.header["status"] = "REDIRECT"
	h.header["Cache-Control"] = "no-cache"
	h.header["Location"] = "/login.cgi"
else
	unless File.exist?("chat/#{$session.session_id}")
		File.open("chat/#{$session.session_id}","w"){|f|
			f << ["user","time","message"].to_csv
		}
	end

	if $cgi.include?("message") && $cgi["message"] != ""
		t = Time.new.to_i
		File.open("chat/#{$session.session_id}","a"){|f|
		# 997 -> größte Primzahl < 1000
		# Algorithmus ist nicht kollisionsresistent -> Studenten können user faken!
			f << ["User #{$session.session_id.to_i(16) % 997}",t,$cgi["message"]].to_csv
		}
		require "yaml"
		user = "xaver"
		pass = YAML::load_file("users/#{user}.yaml")[:password]
		`./admin/chat.js #{$cgi.server_name} #{user} #{pass} #{$session.session_id} #{t}`
	end

h << <<CONTENT
<div>
<form id='chat' method='POST'>
<input type="submit" id='send' name="Send" value="Send" style='width: 5%'/>
<input type="text" id='message' name="message" placeholder="Message" style='width: 90%' />
</form>
</div>
CONTENT

h << "<div style='margin-top:10px'>"
CSV.read("chat/#{$session.session_id}",{headers:true}).reverse_each{|chat|
	h << "<b>#{chat["user"]}:</b> #{chat["message"]}</br>"
}
h << "</div>"


end
h.out($cgi)
