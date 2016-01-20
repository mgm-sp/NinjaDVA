#!/usr/bin/ruby

require_relative "../html"
require "csv"
require "cgi"
require 'cgi/session'
$cgi = CGI.new
$session = CGI::Session.new($cgi)

h = HTML.new("Supportchat")
messages = []
Dir["../chat/*"].each{|f|
	File.open(f).each_line{|l|
		messages << l.scan(/^([0-9]+),(.*)/).flatten
	}
}
messages.sort.each{|time,m|
	h << "<div><b>#{time}:</b> #{CGI.escapeHTML(m)}"
}
h.out($cgi)
