#!/usr/bin/ruby

require_relative "../html"
require "csv"
require "cgi"
require 'cgi/session'
$cgi = CGI.new
$session = CGI::Session.new($cgi,{"session_path" =>  "/"})

h = HTML.new("Supportchat")
messages = []
if $cgi.include?("support_id") && $cgi["support_id"] =~ /\A[a-f0-9]+\Z/

	if $cgi.include?("message") && $cgi["message"] != ""
		t = Time.new.to_i
		File.open("../../db/chat/#{$cgi["support_id"]}","a"){|f|
			f << ["Admin", t, $cgi["message"]].to_csv
		}
	end

	chats = ["../../db/chat/#{$cgi["support_id"]}"]
h << <<CONTENT
<div>
<form id='chat' method='POST'>
<input type="submit" id='send' name="Send" value="Send" style='width: 5%'/>
<input type="text" id='message' name="message" placeholder="Message" style='width: 90%' />
<input type="hidden" name="support_id" value="#{$cgi["support_id"]}" />
<input type='hidden' name='secure' value='secure' />
</form>
</div>
CONTENT
else
	chats = Dir["../../db/chat/*"]
end

chats.each{|f|
	CSV.read(f,{headers:true}).each{|chat|
		messages << [chat["time"].to_i,chat["user"],chat["message"],File.basename(f)]
	}
}

h << "<div style='margin-top:10px'>"
messages.sort.each{|time,user,m,support_id|
	if !$cgi.include?("question_time") || time == $cgi["question_time"].to_i
		h << "<b>"
		if $cgi.include?("support_id")
			href = "?secure"
		else
			href = "?secure&support_id=#{support_id}"
		end
		h << "<a href='#{href}'>#{user}</a>"
		href = "?secure&support_id=#{support_id}"
		href += "&question_time=#{time}" unless $cgi.include?("question_time")

		h << "(<a href='#{href}'>#{Time.at(time).strftime("%H:%M")}</a>):</b>"
		h << " #{$cgi.include?("secure") ? CGI.escapeHTML(m) : m}<br />"
	end
}
h << "</div>"
h.out($cgi)
