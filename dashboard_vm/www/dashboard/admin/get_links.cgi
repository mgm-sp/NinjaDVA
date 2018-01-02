#!/usr/bin/ruby

require_relative "../../config_defaults"
require "cgi"

require "pp"
require "yaml"
require "json"

$cgi = CGI.new

result = {}

# get links of running vms
if File.exists?("#{INSTALLDIR}/dashboard-widgets/available_favourite_links.yaml")
	links = YAML::load_file("#{INSTALLDIR}/dashboard-widgets/available_favourite_links.yaml")
	links.each{|linkhash|
		linkhash[:href] = "http://#{linkhash[:hostname]}.#{$conf.domain}"
	}
	result["vms"] = links
end

#get links configured in json
if File.exists?("#{$conf.dbdir_absolute}/links.json")
	json_links = JSON.parse(File.read("#{$conf.dbdir_absolute}/links.json"), :symbolize_names => true)
	result["links"] = json_links
end


out = JSON.dump(result)
CGI.new.out{out}
