#!/usr/bin/ruby

require_relative "../../config_defaults"
require "cgi"

require "pp"

$cgi = CGI.new
if $cgi.include?("weather")
	if $cgi["weather"].class == StringIO
		File.open("#{$conf.dbdir_absolute}/weather.json","w"){|f|
			f << $cgi["weather"].read
		}
	elsif $cgi["weather"].class == String
		File.open("#{$conf.dbdir_absolute}/weather.json","w"){|f|
			f << $cgi["weather"]
		}
	else
		require "fileutils"
		FileUtils.mv($cgi["weather"].local_path(),"#{$conf.dbdir_absolute}/weather.json")
	end
	out = "OK"
else
	out = <<~FORM
	<form method='POST' enctype='multipart/form-data'>
		<input type="file" name="weather" />
		<input type='submit' />
	</form>
FORM
end
$cgi.out{out}
