#!/usr/bin/ruby

require_relative "../../config_defaults"
require "cgi"

require "pp"

$cgi = CGI.new
if $cgi.include?("calendarconf")
	if $cgi["calendarconf"].class == StringIO
		File.open("#{$conf.dbdir_absolute}/calendarconf.json","w"){|f|
			f << $cgi["calendarconf"].read
		}
	elsif $cgi["calendarconf"].class == String
		File.open("#{$conf.dbdir_absolute}/calendarconf.json","w"){|f|
			f << $cgi["calendarconf"]
		}
	else
		require "fileutils"
		FileUtils.mv($cgi["calendarconf"].local_path(),"#{$conf.dbdir_absolute}/calendarconf.json")
	end
	out = "OK"
else
	out = <<~FORM
	<form method='POST' enctype='multipart/form-data'>
		<input type="file" name="calendarconf" />
		<input type='submit' />
	</form>
FORM
end
$cgi.out{out}
