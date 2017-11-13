#!/usr/bin/ruby


require_relative "html"
require_relative "../config_defaults"
require "csv"
require "cgi"
require 'cgi/session'
$cgi = CGI.new
$session = CGI::Session.new($cgi)

h = HTML.new("View File")
h.add_head_script("jquery-2.2.3.min.js")

h.add_html_head(<<STYLE
<style type='text/css'>
html {
height: 95%
}
body {
	height: 100%;
	margin: 0;
}
#file object {
	width:100%;
	height:100%;
}
</style>
STYLE
)
file = "files/#{$cgi["default"]}"
if File.exists?(file) && !File.directory?(file)
	object = "<object data=\"#{file}\"></object>"
else
	object = "Please choose a file."
end
h << <<CONTENT
<div id='file' style='text-align: center;height: 100%'>
#{object}
</div>
CONTENT

h.add_script <<LISTENER
function chooseFile(event){
	var file = event.data;
	if (typeof file === "string"){
		$("#file").text("");
		$("#file").append($("<object data='files/"+file+"'/>"));
	}
}
window.addEventListener("message", chooseFile);
LISTENER


h.out($cgi)
if ENV['HTTP_REFERER'] =~ /myhomepage.#{$conf.domain}/
	require_relative "../solved"
	Solution.new("dom_based_xss",1,"Viewed a Webpage at myhomepage which requests view.cgi")
end
