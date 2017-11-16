#!/usr/bin/ruby

require_relative "../config_defaults"
require "cgi"

if File.exists?("#{$conf.dbdir_absolute}/schedule.json")
	out = File.open("#{$conf.dbdir_absolute}/schedule.json").read
else
	out = "[]"
end

$cgi = CGI.new
$cgi.out({
	"Content-Type" => "application/json"
}){out}
