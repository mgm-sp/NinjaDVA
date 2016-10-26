#!/usr/bin/ruby

require_relative "../config_defaults"
require_relative "html"
require "cgi"
$cgi = CGI.new
h = HTML.new("My Homepage")

if $cgi.include?("url") && $cgi["url"] =~ /\A[\w\-_]+\Z/ && File.exists?("#{$conf.myhomepagedb}/#{$cgi["url"]}.yaml")

	require "yaml"
	homepage = YAML::load_file("#{$conf.myhomepagedb}/#{$cgi["url"]}.yaml")
	if homepage[:password] == $cgi["password"]
		homepage[:html].body = $cgi["body"]
		File.open("#{$conf.myhomepagedb}/#{$cgi["url"]}.yaml","w"){|f|
			f << homepage.to_yaml
		}
		h.header["status"] = "REDIRECT"
		h.header["Cache-Control"] = "no-cache"
		h.header["Location"] = "/edit.cgi?url=#{$cgi["url"]}&password=#{$cgi["password"]}"


		require "sqlite3"
		userdb = SQLite3::Database.new($conf.userdb)
		user = "susi"
		pass = userdb.get_first_row("SELECT password FROM users WHERE id = ?",user)[0]
		`./admin/myhomepage.js #{$conf.domain} #{user} #{pass} #{$cgi["url"]}`

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
