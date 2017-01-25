#!/usr/bin/env ruby
#

require_relative "../../config_defaults"
require "cgi"
require "yaml"
require "json"
$cgi = CGI.new
solutions = {}
Dir.glob("#{INSTALLDIR}/challenge-descriptions/*.yaml").collect{|f|
	challenge = YAML::load_file(f)
	challenge_id = File.basename(f,".yaml")
  solutions[challenge_id] = challenge[:solutions]
}

$cgi.out({ "content-type" => "application/json" }){solutions.to_json}
