#!/usr/bin/env ruby

require_relative "../../config_defaults"
require "cgi"
require "json"

CGI.new.out({ "content-type" => "application/json" }){Dir.glob("#{$conf.cloudfiles}/*").collect{|f| File.basename(f)}.to_json}