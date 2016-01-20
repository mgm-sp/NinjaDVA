#!/usr/bin/ruby

require_relative "../html"
require "csv"
require "cgi"
require 'cgi/session'
$cgi = CGI.new

h = HTML.new("Supportchat")
if $cgi.include?("support_id") && $cgi["support_id"] =~ /\A[a-f0-9]\z/ && File.exists?("../chat/#{$cgi['support_id']}")
	File.open("../chat/#{$cgi['support_id']}").each_line{|l|
		t,m = l.scan(/^([0-9]+),(.*)/).flatten
		h << "#{m}" if t == $cgi["question_time"]
	}
end

h.out($cgi)
