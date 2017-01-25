#!/usr/bin/ruby

require_relative "../../config_defaults"
require "csv"
require "cgi"
require "pp"
require "json"

$cgi = CGI.new

header = { "content-type" => "application/json" }
s = CSV.read($conf.solutiondb,{headers: true, col_sep: ","})
solves = {}
s.each{|l|
	ip = l["ip"]
	c = l["challenge"]
	state = l["state"].to_i

	solves[ip] ||= {}
	if (!solves[ip][c]) || solves[ip][c][:state] < state
		solves[ip][c] = {
			:state => state,
			:comment => l["comment"],
			:time => l["time"]
		}
	end
}

$cgi.out(header){solves.to_json}
