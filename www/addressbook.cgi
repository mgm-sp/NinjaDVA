#!/usr/bin/ruby

$:.push(".")
require "dvmail.rb"
dvm = Dvmail.new
groups = dvm.userdb.execute("SELECT groups FROM users").collect{|g| g[0].split(", ") }.flatten.uniq

show = $cgi["group"]

dvm << "<div style='width: 30em'>"
dvm << <<FORM
<form method='GET' id='mail' action=''>
Gruppe:
<select name='group'>
	<option value=''>Alle</option>
FORM
groups.each{|g|
	unless g == "Hidden"
		dvm << "<option value='#{CGI.escapeHTML(g)}'"
		dvm << " selected='selected' " if g == show
		dvm << ">#{CGI.escapeHTML(g)}</option>"
	end
}
dvm << <<FORM
</select>
<input type='submit' value='Zeigen' />
</form>
FORM
begin
	dvm.userdb.execute("SELECT id,name,message,groups FROM users WHERE groups LIKE '%#{show}%' AND groups NOT LIKE '%Hidden%'"){|userrow|
		dvm << "<fieldset><legend>vCard user #{userrow[0]}</legend>
<table>
	<tr>
		<td>Name:   </td><td>#{CGI.escapeHTML(userrow[1] == nil ? "<<not set yet>>" : userrow[1])}</td>
	</tr><tr>
		<td>Message:</td><td>#{CGI.escapeHTML(userrow[2] == nil ? "<<not set yet>>" : userrow[2])}</td>
	</tr><tr>
		<td>Groups: </td><td>#{CGI.escapeHTML(userrow[3])}</td>
	</tr>
</table>
	</fieldset>
		"
	}
rescue SQLite3::Exception => e
	dvm << "<div class='error'>Error: #{e}</div>"
end
dvm << "</div>"
dvm.out
