#!/usr/bin/ruby

require_relative "../../config_defaults"
require "cgi"

require "pp"

$cgi = CGI.new
if $cgi.include?("schedule")
	File.open("#{$conf.dbdir_absolute}/schedule.json","w"){|f|
		if $cgi["schedule"].class == StringIO
			f << $cgi["schedule"].read
		else
			f << $cgi["schedule"]
		end
	}
	out = "OK"
else
	out = <<FORM
<form method='POST' enctype='multipart/form-data'>
	<input type="file" name="schedule" />
	<input type='submit' />
</form>
FORM
end
$cgi.out{out}
