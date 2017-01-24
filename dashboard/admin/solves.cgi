#!/usr/bin/ruby

require_relative "../html"
require_relative "../../config_defaults"
require "csv"
require "cgi"
require 'cgi/session'
require "pp"
require "yaml"

$cgi = CGI.new
$session = CGI::Session.new($cgi,{"session_path" =>  "/"})

h = HTML.new("Solves")
s = CSV.read($conf.solutiondb,{headers: true, col_sep: ","})
solves = {}
s.each{|l|
	solves[l["challenge"]] ||= {}
	state = l["state"].to_i
	if !solves[l["challenge"]][l["ip"]] || solves[l["challenge"]][l["ip"]][:state] < state
		solves[l["challenge"]][l["ip"]] = {
			:state => state,
			:comment => l["comment"],
			:time => l["time"]
		}
	end
}
h.add_html_head <<CSS
<style>
table {
	text-align: left;
}
td, th {
	padding: 0px 10px;
}
h2 {
font-size: 1.1em;
}
</style>
CSS
solves.each{|chal_id,solver|
	challengefile = "#{INSTALLDIR}/challenge-descriptions/#{chal_id}.yaml"
	if File.exists?(challengefile)
		challenge = YAML::load_file("#{INSTALLDIR}/challenge-descriptions/#{chal_id}.yaml")
	else
		challenge = {category:chal_id,name:chal_id}
	end

	h << "<fieldset><legend>#{challenge[:category]} -- #{challenge[:name]}</legend>"
	h << "<table><tr><th>IP Address</th><th>Points</th></th><th>Comment</th></tr>"
	solver.each{|ip,state|
		h << "<tr><td>#{ip}</td><td>#{state[:state]}</td></td><td>#{CGI.escapeHTML(state[:comment])}</td></tr>"
	}
	h << "</table>"
	if challenge[:solutions]
		h << "<h2>Solutions</h2><ul>"
		h << "<li>#{challenge[:solutions].collect{|s| CGI.escapeHTML(s)}.join('</li><li>')}</li>"
		h << "</ul>"
	end
	h << "</fieldset>"
}

h.out($cgi)
