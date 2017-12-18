#!/usr/bin/ruby

require_relative "../../config_defaults"
require "cgi"

require "pp"

$cgi = CGI.new
if $cgi.include?("layout")
	if $cgi["layout"].class == StringIO
		File.open("#{$conf.dbdir_absolute}/layout.json","w"){|f|
			f << $cgi["layout"].read
		}
	elsif $cgi["layout"].class == String
		File.open("#{$conf.dbdir_absolute}/layout.json","w"){|f|
			f << $cgi["layout"]
		}
	else
		require "fileutils"
		FileUtils.mv($cgi["layout"].local_path(),"#{$conf.dbdir_absolute}/layout.json")
	end
	out = "OK"
else
	out = <<~FORM
	<form method='POST' enctype='multipart/form-data'>
		<input type="file" name="layout" />
		<input type='submit' />
	</form>
FORM
end
$cgi.out{out}
