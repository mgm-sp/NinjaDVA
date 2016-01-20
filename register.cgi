#!/usr/bin/ruby

require_relative "dvmail"
require "yaml"


m = Dvmail.new
if $cgi.include?("username")
	if $cgi["username"] =~ /\A[a-zA-Z0-9]+\z/
		unless File.exists?("users/#{$cgi["username"]}.yaml")
			if $cgi["password"] == $cgi["password2"]
				user = {
					:name => "",
					:password => $cgi["password"],
					:message => "",
					:groups => ["Newbie"]
				}
				File.open("users/#{$cgi["username"]}.yaml","w"){|f|
					f << user.to_yaml
				}
				m.html.header["status"] = "REDIRECT"
				m.html.header["Cache-Control"] = "no-cache"
				m.html.header["Location"] = "/login.cgi?register_redirect"
			else
				m << "<div class='red'>Passwords do not match!</div>"
			end
		else
			m << "<div class='red'>Username already exists!</div>"
		end
	else
		m << "<div class='red'>Only [a-zA-Z0-9] is allowed in Username!</div>"
	end
end



m << <<CONTENT
<form method="POST">
	<table>
	<tr><td>Username:</td><td><input type='text' name='username' value="#{CGI.escapeHTML($cgi["username"])}"/></td></tr>
	<tr><td>Password:</td><td><input type='password' name='password' /></td></tr>
	<tr><td>Password (repeat):</td><td><input type='password' name='password2' /></td></tr>
	<tr><td></td><td><input type='submit' /></td></tr>
	</table>
</form>
CONTENT
m.out
