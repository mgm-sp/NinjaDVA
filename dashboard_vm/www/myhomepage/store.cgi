#!/usr/bin/ruby

require_relative "../config_defaults"
require_relative "html"
require "cgi"
$cgi = CGI.new
h = HTML.new("My Homepage")

if $cgi.include?("url") && $cgi["url"] =~ /\A[\w-]+\Z/ && File.exists?("#{$conf.myhomepagedb}/#{$cgi["url"]}.yaml")

	require "yaml"
	homepage = YAML::load_file("#{$conf.myhomepagedb}/#{$cgi["url"]}.yaml")
	if homepage[:password] == $cgi["password"]
		homepage[:contents] = $cgi["contents"]
		homepage[:header] = $cgi["header"]
		File.open("#{$conf.myhomepagedb}/#{$cgi["url"]}.yaml","w"){|f|
			f << homepage.to_yaml
		}
		h.header["status"] = "OK"

	else # wrong PW
		h.header["status"] = "FORBIDDEN"
		#h.header["Cache-Control"] = "no-cache"
		#h.header["Location"] = "/"
	end
else # url does not exist
	h.header["status"] = "NOT_FOUND"
	#h.header["Cache-Control"] = "no-cache"
	#h.header["Location"] = "/"
end


h.out($cgi)
