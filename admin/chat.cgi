#!/usr/bin/ruby

require_relative "../html"
require "csv"
require "cgi"
require 'cgi/session'
$cgi = CGI.new

h = HTML.new("Supportchat")
if $cgi.include?("support_id") && $cgi["support_id"] =~ /\A[a-f0-9]+\z/ && File.exists?("../chat/#{$cgi['support_id']}")
	CSV.read("../chat/#{$cgi['support_id']}",{headers:true}).each{|chat|
		h << "#{chat["message"]}" if chat["time"] == $cgi["question_time"]
	}
end

h.out($cgi)
