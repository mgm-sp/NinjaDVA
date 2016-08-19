#!/usr/bin/ruby

require_relative "dvmail"
require "yaml"


m = Dvmail.new
if $cgi.include?("username") && 
		File.exists?("#{USERS}/#{$cgi["username"]}.yaml") && 
		$cgi["username"] =~ /\A[a-zA-Z0-9]+\z$/ &&
		YAML::load(File.open("#{USERS}/#{$cgi["username"]}.yaml"))[:password] == $cgi["password"]

	$session["username"] = $cgi["username"]
	m.html.header["status"] = "REDIRECT"
	m.html.header["Cache-Control"] = "no-cache"
	m.html.header["Location"] = "/inbox.cgi"
end

if $cgi.include?("register_redirect")
	m << "<div class='green'>Your Account was created successfully, please login now.</div>"
end

m << <<CONTENT
<div>
<form method="POST">
	<table>
	<tr><td>Username:</td><td><input type='text' name='username' value="#{CGI.escapeHTML($cgi["username"])}"/></td></tr>
	<tr><td>Password:</td><td><input type='password' name='password' /></td></tr>
	<tr><td></td><td><input type='submit' /></td></tr>
	<tr><td></td><td><a href='register.cgi' >Register new Account</a></td></tr>
	<tr><td></td><td><a target="_blank" href="chat.cgi">Open supportchat</a></td></tr>
	</table>
</form>
</div>
CONTENT
m.out
