#!/usr/bin/ruby

$:.push(".")
require "dvmail.rb"
dvm = Dvmail.new

errormsg = ""

admin = ($session['username'] == 'admin' || dvm.user[:groups].include?("Administrator"))
if $cgi.include?("edit_user") && $session['username'] == $cgi['user']
	[:name, :message].each{|item|
		dvm.user[item] = $cgi[item.to_s]
	}
	if $cgi.include?("groups")
		if admin
			dvm.user[:groups] = $cgi["groups"].split(",").collect{|e| e.strip}
		else
			errormsg = "<div class='red'>You are not allowed to change the Groups!</div>"
		end
	end
	dvm.save
	dvm = Dvmail.new
end

dvm << errormsg

u = $session['username']
	dvm << "<fieldset><legend>vCard user #{u}</legend>
<form method='POST'>
<input type='hidden' name='user' value='#{$session['username']}' />
<table>
	<tr>
		<td>Name:</td><td><input type='text' name='name' value='#{CGI.escapeHTML(dvm.user[:name])}' size='50' /></td>
	</tr><tr>
    <td>Message:</td><td><input type='text' name='message' value='#{CGI.escapeHTML(dvm.user[:message])}' size='50' /></td>
	</tr><tr>
    <td>Groups:</td><td><input type='text' name='groups' #{admin ? "" : "disabled='disabled'"} value='#{CGI.escapeHTML(dvm.user[:groups].join(', '))}' size='50'/></td>
	</tr><tr>
    <td></td><td><input type='submit' name='edit_user' /></td>
	</tr>
</table>
</form>
</fieldset>
"

dvm.out
