#!/usr/bin/env ruby
#

require_relative "../../config_defaults"
require "cgi"
require "yaml"
require "json"
$cgi = CGI.new
solutions = {}
$conf.exercises.each{|challenge_id|
	challenge = YAML::load_file("#{INSTALLDIR}/challenge-descriptions/#{challenge_id}.yaml")
  solutions[challenge_id] = challenge[:solutions]
}

$cgi.out({ "content-type" => "application/json" }){solutions.to_json}
