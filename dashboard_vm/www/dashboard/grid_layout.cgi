#!/usr/bin/env ruby


require_relative "../config_defaults"
require "cgi"
require "json"
$cgi = CGI.new

if File.exists?("#{$conf.dbdir_absolute}/layout.json")
    sJsonPlain = File.read("#{$conf.dbdir_absolute}/layout.json")
    sJson = JSON.parse(sJsonPlain).to_json()
else
    sJson = "[]"
end


$cgi.out({ "content-type" => "application/json" }){sJson}
