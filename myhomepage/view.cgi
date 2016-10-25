#!/usr/bin/ruby

DB = "../db/myhomepage/"
require_relative "html"
require "cgi"
$cgi = CGI.new

h = HTML.new("My Homepage")

if $cgi.include?("url") && $cgi["url"] =~ /\A[\w\-_]+\Z/ && File.exists?("#{DB}/#{$cgi["url"]}.yaml")

	require "yaml"
	h = YAML::load_file("#{DB}/#{$cgi["url"]}.yaml")[:html]

else
	h.header["status"] = "REDIRECT"
	h.header["Cache-Control"] = "no-cache"
	h.header["Location"] = "/"
end

h.out($cgi)
