#!/usr/bin/env ruby

require_relative "../config_defaults"
require "cgi"
require "json"
require "csv"
$cgi = CGI.new

oResult = JSON[{}]
if $cgi.include?("url") && $cgi.include?("password")
    configPath = "#{$conf.myhomepagedb}/#{$cgi["url"]}.yaml"
    logPath = "#{$conf.myhomepagedb}/#{$cgi["url"]}_access.log"
    if File.exists?(configPath) && File.exists?(logPath)
        require "yaml"
        homepage = YAML::load_file(configPath)
        if homepage[:password] == $cgi["password"]
            # convert csv to json
            lines = CSV.open(logPath).readlines
            keys = lines.delete lines.first
            data = lines.map do |values|
                Hash[keys.zip(values)]
            end
            oResult = JSON.generate(data)
        end
    end
end

$cgi.out({ "content-type" => "application/json" }){oResult}