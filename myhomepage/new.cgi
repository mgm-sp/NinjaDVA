#!/usr/bin/ruby

require_relative "../config_defaults"
require_relative "html"
require "cgi"
$cgi = CGI.new
h = HTML.new("My Homepage")


if $cgi.include?("url") && $cgi["url"] =~ /\A[\w\-_]*\Z/
	url = $cgi["url"]
	if File.exists?("#{$conf.myhomepagedb}/#{url}.yaml")
		h.header["status"] = "REDIRECT"
		h.header["Cache-Control"] = "no-cache"
		h.header["Location"] = "/?error=#{CGI.escape("This Homepage already exists.")}"
	else
		if $cgi.include?("password")
			pw = $cgi["password"]
		else
			chars = ("a".."z").to_a + ("A".."Z").to_a + ("0".."9").to_a 
			pw = Array.new(12){chars[rand(chars.size)]}.join
		end
		html = HTML.new("My Homepage -- #{url}")
		html.add_head_script("jquery-2.2.3.min.js")
		html << "<h1>Welcome</h1>"
		html << "<img style='width:10em;' src='construction.svg' alt='Under Construction' />"
		homepage = {
			:html => html,
			:password => pw
		}
		require "yaml"
		File.open("#{$conf.myhomepagedb}/#{url}.yaml","w"){|f|
			f << homepage.to_yaml
		}
		require "csv"
		File.open("#{$conf.myhomepagedb}/#{url}_access.log","w"){|f|
			f << ["ADDR","METHOD","URI","USER_AGENT","TIME","REFERER"].to_csv
		}
		h.header["status"] = "REDIRECT"
		h.header["Cache-Control"] = "no-cache"
		h.header["Location"] = "/edit.cgi?url=#{$cgi["url"]}&password=#{pw}"
	end
else
	h.header["status"] = "REDIRECT"
	h.header["Cache-Control"] = "no-cache"
	h.header["Location"] = "/?error=#{CGI.escape("URL may only contain letters, numbers, and dashes.")}"
end

h.out($cgi)
