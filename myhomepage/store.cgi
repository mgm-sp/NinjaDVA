#!/usr/bin/ruby

DB = "../db/myhomepage/"

require_relative "html"
require "cgi"
$cgi = CGI.new
h = HTML.new("My Homepage")

if $cgi.include?("url") && $cgi["url"] =~ /\A[\w\-_]+\Z/ && File.exists?("#{DB}/#{$cgi["url"]}.yaml")

	require "yaml"
	homepage = YAML::load_file("#{DB}/#{$cgi["url"]}.yaml")
	if homepage[:password] == $cgi["password"]
		homepage[:html].body = $cgi["body"]
		File.open("#{DB}/#{$cgi["url"]}.yaml","w"){|f|
			f << homepage.to_yaml
		}
		h.header["status"] = "REDIRECT"
		h.header["Cache-Control"] = "no-cache"
		h.header["Location"] = "/edit.cgi?url=#{$cgi["url"]}&password=#{$cgi["password"]}"
	else # wrong PW
		h.header["status"] = "REDIRECT"
		h.header["Cache-Control"] = "no-cache"
		h.header["Location"] = "/"
	end
else # url does not exist
	h.header["status"] = "REDIRECT"
	h.header["Cache-Control"] = "no-cache"
	h.header["Location"] = "/"
end


h.out($cgi)
