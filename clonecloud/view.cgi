#!/usr/bin/ruby


require_relative "html"
require_relative "../config_defaults"
require "csv"
require "cgi"
require 'cgi/session'
$cgi = CGI.new
$session = CGI::Session.new($cgi)

h = HTML.new("Current Lecture")
h.add_head_script("jquery-2.2.3.min.js")

h.add_html_head(<<STYLE
<style type='text/css'>
html {
height: 95%
}
body {
	height: 100%;
}
#current_slide object {
	width:100%;
	height:100%;
}
</style>
STYLE
)
h << <<CONTENT
<div id='current_slide' style='text-align: center;height: 100%'>
<object type="application/pdf" data="#{$conf.current_slide}" > </object>
</div>
CONTENT

h.add_script <<LISTENER
function chooseFile(event){
	var file = event.data;
	$("#current_slide").text("");
	$("#current_slide").append($("<object data='files/"+file+"'/>",{
		"type" : "application/pdf",
	}));
}
window.addEventListener("message", chooseFile);
LISTENER


h.out($cgi)
