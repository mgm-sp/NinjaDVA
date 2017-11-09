#!/usr/bin/ruby

require_relative "../config_defaults"
require_relative "html"
require "cgi"
$cgi = CGI.new
h = HTML.new("My Homepage")

if $cgi.include?("url") && $cgi["url"] =~ /\A[\w\-_]+\Z/ && File.exists?("#{$conf.myhomepagedb}/#{$cgi["url"]}.yaml")

	require "yaml"
	h = YAML::load_file("#{$conf.myhomepagedb}/#{$cgi["url"]}.yaml")[:html]

	require "csv"
	File.open("#{$conf.myhomepagedb}/#{$cgi["url"]}_access.log","a"){|f|
		f << [$cgi.remote_addr,ENV["REQUEST_METHOD"],ENV["REQUEST_URI"],$cgi.user_agent,Time.now,ENV["HTTP_REFERER"]].to_csv
	}

else
	h.header["status"] = "REDIRECT"
	h.header["Cache-Control"] = "no-cache"
	h.header["Location"] = "/"
end

h.out($cgi)
