#!/usr/bin/ruby

require_relative "../config_defaults"
require_relative "html"
require "cgi"
$cgi = CGI.new
file = ENV["REQUEST_URI"].gsub(/\A\/([\w\-_]+).*\Z/,"\\1")
if File.exists?("#{$conf.myhomepagedb}/#{file}.yaml")

	require "yaml"
	page = YAML::load_file("#{$conf.myhomepagedb}/#{file}.yaml")

	puts page[:header].lines[0].gsub(/^HTTP\/.* (\d\d\d).*$/,'Status: \1')
	puts page[:header].lines[1..-1].join.strip
	puts
	puts page[:contents]

	require "csv"
	File.open("#{$conf.myhomepagedb}/#{file}_access.log","a"){|f|
		f << [$cgi.remote_addr,ENV["REQUEST_METHOD"],ENV["REQUEST_URI"],$cgi.user_agent,Time.now,ENV["HTTP_REFERER"]].to_csv
	}

else
	h = HTML.new("My Homepage")
	h.header["status"] = "REDIRECT"
	h.header["Cache-Control"] = "no-cache"
	h.header["Location"] = "/"
	h.out($cgi)
end

