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

h.add_css("http://myhomepage.#{$conf.domain}/codemirror/codemirror.css") # needs to be loaded before other css
h.add_head_script("http://myhomepage.#{$conf.domain}/codemirror/codemirror.js")
h.add_head_script("http://myhomepage.#{$conf.domain}/codemirror/css.js")
h.add_head_script("http://myhomepage.#{$conf.domain}/codemirror/javascript.js")
h.add_head_script("http://myhomepage.#{$conf.domain}/codemirror/vbscript.js")
h.add_head_script("http://myhomepage.#{$conf.domain}/codemirror/xml.js")
h.add_head_script("http://myhomepage.#{$conf.domain}/codemirror/htmlmixed.js")
h.add_script_file("sql.js")
h.add_css("solves.css")
h.add_css("../jquery.gridster.min.css")
h.add_html_head <<CSS
<style>
.CodeMirror {
	margin-top: 1em;
	border-width: 1px;
	border-style: solid;
  height: auto;
  width: 100%;
}
</style>
CSS

h.add_head_script("../jquery-2.2.3.min.js")
h.add_head_script("../jquery.gridster.min.js")

h << <<MENU
<div id="menu">
<div id="solution"></div>
<input type="button" value="Save" onclick="save_grid_layout()" />
<input type="button" value="Reload" onclick="update_data()" />
&nbsp;
MENU
ex = {}
$conf.exercises.each{|challenge_id|
	ex[challenge_id] = YAML::load_file("#{INSTALLDIR}/challenge-descriptions/#{challenge_id}.yaml")
}
ex.each{|challenge_id,challenge|
  h << "<input type='button' value='#{challenge_id}' onclick='select_task(this)' id='#{challenge_id}' />"
}
h << "<input type='button' value='ping' onclick='select_task(this)' id='ping' />"

h << <<MENU
</div>
MENU

h << '<div class="gridster"></div>'
h.add_script_file("solves.js")

h.out($cgi)
