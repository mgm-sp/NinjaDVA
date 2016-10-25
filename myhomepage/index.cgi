#!/usr/bin/ruby

require_relative "html"
require "cgi"
$cgi = CGI.new

h = HTML.new("My Homepage")

h.add_css("myhomepage.css")


h << <<NEW
<h1>Create New Homepage</h1>
<form action='new.cgi' method='POST'>
	<label for="url">http://#{$cgi.server_name}/</label><input id="url" size='16' type='text' name='url' value="" />
	<input type='submit'/>
	<div style='margin-top: 10px; font-size: small'>
	#{$cgi.include?("error") ? CGI.escapeHTML($cgi["error"]) : ""}
	</div>
</form>
NEW

h.out($cgi)
