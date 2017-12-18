#!/usr/bin/env ruby


require_relative "../config_defaults"
require "cgi"
require "json"
$cgi = CGI.new

sJsonPlain = File.read("#{$conf.dbdir_absolute}/layout.json")
sJson = JSON.parse(sJsonPlain).to_json()

$cgi.out({ "content-type" => "application/json" }){sJsonPlain}
