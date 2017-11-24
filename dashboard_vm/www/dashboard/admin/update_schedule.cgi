#!/usr/bin/ruby

require_relative "../../config_defaults"
require "cgi"

require "pp"

$cgi = CGI.new
if $cgi.include?("schedule")
	if $cgi["schedule"].class == StringIO
		File.open("#{$conf.dbdir_absolute}/schedule.json","w"){|f|
			f << $cgi["schedule"].read
		}
	elsif $cgi["schedule"].class == String
		File.open("#{$conf.dbdir_absolute}/schedule.json","w"){|f|
			f << $cgi["schedule"]
		}
	else
		require "fileutils"
		FileUtils.mv($cgi["schedule"].local_path(),"#{$conf.dbdir_absolute}/schedule.json")
	end
	out = "OK"
else
	out = <<~FORM
	<form method='POST' enctype='multipart/form-data'>
		<input type="file" name="schedule" />
		<input type='submit' />
	</form>
FORM
end
$cgi.out{out}
