#!/usr/bin/ruby

require_relative "../config_defaults"
require "cgi"
require "json"


$cgi = CGI.new
$cgi.out({
	"Content-Type" => "application/json"
}){$conf.events.to_json}
