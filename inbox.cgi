#!/usr/bin/ruby

$:.push(".")
require "dvmail.rb"
m = Dvmail.new


if m.user[:groups].include?("admin")
	m << <<MAIL
<div>
<table>
<tr>
<td class='header'>From:</td><td>Peter</td>
</tr><tr>
<td class='header'>To:</td><td>All Administrators</td>
</tr><tr>
<td class='header'>Subject:</td><td>Backdoor Password for all Clients</td>
</tr><tr>
<td colspan='2'>
<p>Dear Colleagues</p>
<p>Please do not forget our local administrator password which is valid<br />
for all our Windows client computers: »Start123«</p>
<p>Best, Peter</p>
</td>
</tr>
</table>
</div>
MAIL
else
	m << "<div>Your INBOX is empty!</div>"
end

m.out
