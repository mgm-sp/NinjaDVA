#!/usr/bin/env ruby

require_relative "../../config_defaults"
require "cgi"
require "json"

sPathToJson = "#{$conf.dbdir_absolute}/weather.json"
oResult = JSON[{}]

if File.exists?(sPathToJson)
    oResult = File.read(sPathToJson)
end
CGI.new.out({ "content-type" => "application/json" }){oResult}