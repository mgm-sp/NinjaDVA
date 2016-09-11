#!/usr/bin/ruby

$:.push(".")
require "dvmail.rb"
dvm = Dvmail.new

dvm << "<div style='width: 30em'>"
begin
	dvm.userdb.execute( "SELECT id,name,message,groups FROM users" ){|userrow|
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
