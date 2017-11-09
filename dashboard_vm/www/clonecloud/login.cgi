#!/usr/bin/ruby
# coding: utf-8
#
require_relative "clonecloud.rb"
require "argon2"

m = CloneCloud.new
if $session["username"]
	m.html.header["status"] = "REDIRECT"
	m.html.header["Cache-Control"] = "no-cache"
	if $cgi.include?("return_url")
		m.html.header["Location"] = $cgi["return_url"]
	else
		m.html.header["Location"] = "/files.cgi"
	end
end
if $cgi.include?("username")
	pw = m.userdb.get_first_row("SELECT password FROM users WHERE id = ?",$cgi["username"])
	if pw
		if (pw[0] == Digest::MD5.hexdigest($cgi["password"])) ||
		   (pw[0] =~ /^\$argon2/ && Argon2::Password.verify_password($cgi["password"],pw[0],$conf.pepper))
			$session["username"] = $cgi["username"]
			m.html.header["status"] = "REDIRECT"
			m.html.header["Cache-Control"] = "no-cache"
			if $cgi.params.include?("return_url")
				m.html.header["Location"] = $cgi["return_url"]
			else
				m.html.header["Location"] = "/files.cgi"
			end
		end
	end
	m << "<div class='error'>Wrong password or username does not exist.</div>"
end

m << <<CONTENT
<div id='loginmasq'>
<div id='head'>
<img src='clone.png' alt='Clone Helmet' />
</div>
<div id='login'>
<form method="post">
	<p id='top'>
	<input type='text' placeholder='Username' name='username' value="#{CGI.escapeHTML($cgi["username"])}"/>
	</p>
	<p id='bottom'>
	<input type='password' placeholder='Password' name='password' />
	<input type='submit' value='' />
	</p>
CONTENT
	if $cgi.include?("return_url")
		m << "<input type='hidden' name='return_url' value='#{CGI.escapeHTML($cgi["return_url"])}' />"
	end
m << <<CONTENT
</form>
</div>
</div>
<div id='footer'>
<a href='/' >cloneCloud</a> – web services under no control
</div>
CONTENT
m.out
