#!/usr/bin/ruby

require_relative "../config_defaults"
require_relative "html"
require "cgi"
$cgi = CGI.new

if $cgi.include?("url") && $cgi["url"] =~ /\A[\w\-_]+\Z/ && File.exists?("#{$conf.myhomepagedb}/#{$cgi["url"]}.yaml")

	require "yaml"
	page = YAML::load_file("#{$conf.myhomepagedb}/#{$cgi["url"]}.yaml")

	puts page[:header].lines[0].gsub(/^HTTP\/.* (\d\d\d).*$/,'Status: \1')
	puts page[:header].lines[1..-1].join
	puts page[:contents]

	require "csv"
	File.open("#{$conf.myhomepagedb}/#{$cgi["url"]}_access.log","a"){|f|
		f << [$cgi.remote_addr,ENV["REQUEST_METHOD"],ENV["REQUEST_URI"],$cgi.user_agent,Time.now,ENV["HTTP_REFERER"]].to_csv
	}

else
	h = HTML.new("My Homepage")
	h.header["status"] = "REDIRECT"
	h.header["Cache-Control"] = "no-cache"
	h.header["Location"] = "/"
	h.out($cgi)
end

