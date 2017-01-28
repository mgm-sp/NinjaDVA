#!/usr/bin/ruby

require_relative "../html"
require_relative "../../config_defaults"
require "cgi"
require 'cgi/session'
require "pp"
require "yaml"
require "json"

$cgi = CGI.new
$session = CGI::Session.new($cgi,{"session_path" =>  "/"})

h = HTML.new("Solves")

h.add_css("solves.css")
h.add_css("../jquery.gridster.min.css")

h.add_head_script("../jquery-2.2.3.min.js")
h.add_head_script("../jquery.gridster.min.js")

h << <<MENU
<div id="menu">
<form>
  <input class="button" type="button" value="Save" onclick="save_grid_layout()">
  <input class="button" type="button" value="Reload" onclick="update_data()"><br>
  <div class="radio">
MENU
ex = {}
$conf.exercises.each{|challenge_id|
	ex[challenge_id] = YAML::load_file("#{INSTALLDIR}/challenge-descriptions/#{challenge_id}.yaml")
}
ex.each{|challenge_id,challenge|
  h << "<input type='radio' name='task' value='#{challenge_id}' onclick='select_task(this)' id='#{challenge_id}'>"
  h << "<label title='#{challenge[:name]}' for='#{challenge_id}'>#{challenge_id}</label><br />"
}
h << "<input type='radio' name='task' value='ping' onclick='select_task(this)' id='ping'>"
h << "<label for='ping'> ping </label><br />"

h << <<MENU
	</div>
</form>
<div id="solution"></div>
</div>
MENU

h << '<div class="gridster"></div>'
h.add_script_file("solves.js")

h.out($cgi)
