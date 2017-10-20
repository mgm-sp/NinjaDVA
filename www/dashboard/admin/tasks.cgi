#!/usr/bin/env ruby
#

require_relative "../../config_defaults"
require "cgi"
require "yaml"
require "json"

def exchange_lab_text string
	string.gsub(/#PENTESTLAB-DOMAIN#/,$conf.domain).gsub(/#ATTACKER-IP#/,$cgi.remote_addr)
end

$cgi = CGI.new
tasks = {}
$conf.exercises.each{|challenge_id|
	challenge = YAML::load_file("#{INSTALLDIR}/challenge-descriptions/#{challenge_id}.yaml")
	tasks[challenge_id] = {
		title: challenge[:name],
		category: challenge[:category],
		description: exchange_lab_text(challenge[:description])
	}
  tasks[challenge_id][:solutions] = []
  tasks[challenge_id][:solutions] += challenge[:solutions].collect{|s|
		exchange_lab_text(s)
  } if challenge[:solutions]
}

$cgi.out({ "content-type" => "application/json" }){tasks.to_json}
