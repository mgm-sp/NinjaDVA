#!/usr/bin/env ruby


require_relative "../config_defaults"
require "cgi"
$cgi = CGI.new

$cgi.out({ "content-type" => "application/json" }){$conf.dashboard_grid_layout}
