#!/usr/bin/ruby

require_relative "../../config_defaults"
require "cgi"

require "pp"

$cgi = CGI.new
if $cgi.include?("links")
	if $cgi["links"].class == StringIO
		File.open("#{$conf.dbdir_absolute}/links.json","w"){|f|
			f << $cgi["links"].read
		}
	elsif $cgi["links"].class == String
		File.open("#{$conf.dbdir_absolute}/links.json","w"){|f|
			f << $cgi["links"]
		}
	else
		require "fileutils"
		FileUtils.mv($cgi["links"].local_path(),"#{$conf.dbdir_absolute}/links.json")
	end
	out = "OK"
else
	out = <<~FORM
		<form method='POST' enctype='multipart/form-data'>
			<input type="file" name="links" />
			<input type='submit' />
		</form>
	FORM
end
$cgi.out{out}
