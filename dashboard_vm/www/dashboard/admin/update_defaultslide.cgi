#!/usr/bin/ruby

require_relative "../../config_defaults"
require "cgi"

require "pp"

$cgi = CGI.new
if $cgi.include?("defaultslide")
	if $cgi["defaultslide"].class == StringIO
		File.open("#{$conf.dbdir_absolute}/defaultslide.json","w"){|f|
			f << $cgi["defaultslide"].read
		}
	elsif $cgi["defaultslide"].class == String
		File.open("#{$conf.dbdir_absolute}/defaultslide.json","w"){|f|
			f << $cgi["defaultslide"]
		}
	else
		require "fileutils"
		FileUtils.mv($cgi["defaultslide"].local_path(),"#{$conf.dbdir_absolute}/defaultslide.json")
	end
	out = "OK"
else
	out = <<~FORM
	<form method='POST' enctype='multipart/form-data'>
		<input type="file" name="defaultslide" />
		<input type='submit' />
	</form>
FORM
end
$cgi.out{out}
