#!/usr/bin/ruby
# encoding: utf-8


$:.push(".")
require "dvmail.rb"
m = Dvmail.new


if m.user[:groups].include?("Administrator")
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
				for all our Windows client computers: "Start123"</p>
				<p>Best, Peter</p>
			</td>
		</tr>
	</table>
</div>
MAIL
elsif $session['username'] == 'siggi'
	m << <<MAIL
<div>
	<table>
		<tr>
			<td class='header'>From:</td><td>Fr&auml;ulein M&uuml;ller-Wachtendonk</td>
		</tr><tr>
			<td class='header'>To:</td><td>Siggi Sorglos</td>
		</tr><tr>
			<td class='header'>Subject:</td><td>Der Mensch macht's!</td>
		</tr><tr>
			<td colspan='2'>
				<p>Sehr geehrter Herr Sorglos,</p>
				<p>vielen Dank für die vielen schönen Produktionen.<br />
				Ich hoffe Sie denken immer an unseren gemeinsamen Leitsatz:</p>
				<p>Der Mensch macht's!</p>
				<p>Viele Grüße,<br />
				M&uuml;ller-Wachtendonk</p>
			</td>
		</tr>
	</table>
</div>
MAIL
elsif $session['username'] == 'xaver'
	m << <<MAIL
<div>
	<table>
		<tr>
			<td class='header'>From:</td><td>Siggi Sorglos</td>
		</tr><tr>
			<td class='header'>To:</td><td>Xaver Sebastian Schmidt</td>
		</tr><tr>
			<td class='header'>Subject:</td><td>Grillen</td>
		</tr><tr>
			<td colspan='2'>
				<p>Hallo Xaver,</p>
				<p>bleibts beim grillen heute Abend?</p>
				<p>Ciao, Siggi</p>
			</td>
		</tr>
	</table>
</div>
MAIL
else
	m << "<div>Your INBOX is empty!</div>"
end

m.out
