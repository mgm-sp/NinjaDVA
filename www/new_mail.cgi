#!/usr/bin/ruby
#
require_relative "../config_defaults"

$:.push(".")
require "dvmail.rb"
dvm = Dvmail.new

if $cgi.include?("newmail")
	dvm << "<div class='green'>Your message has been sent.</div>"
	maildb = SQLite3::Database.new($conf.maildb);
	user = dvm.user[:name] || $session["username"];
	maildb.query("INSERT INTO 'mail'('sender','recipient','subject','body') VALUES (?,?,?,?)", user,$cgi["to"],$cgi["subject"],$cgi["body"]);

	# session fixation
	userid = "siggi"
	pass = dvm.userdb.get_first_row("SELECT password FROM users WHERE id = ?",userid)[0]
	if $cgi["to"] == userid
		$cgi["body"].scan(/http:\/\/\S+/).each{|url|
			cookiefile = `mktemp`.chomp
			`curl --user-agent "Siggi Sorglos" "#{url}" -L --cookie-jar "#{cookiefile}" --stderr /dev/null -o /dev/null`
			`curl 'http://#{$cgi.server_name}/login.cgi' --cookie "#{cookiefile}" -H 'Content-Type: application/x-www-form-urlencoded' --data "username=#{userid}&password=#{pass}" --stderr /dev/null -o /dev/null`
			`rm #{cookiefile}`
		}
	end

else # show compose-form
	dvm << "
<div>
	<form method='POST' id='mail'>
		<table>
			<tr>
				<td class='header'>From:</td><td>#{dvm.user[:name] == "" ? $session["username"] : dvm.user[:name]}</td>
			</tr><tr>
				<td class='header'>To:</td>
				<td>
				<select name='to'>"

		users = dvm.userdb.execute("SELECT id FROM users").collect{|u| u[0]}.sort
		users.each{|u| 
			dvm << "<option value=\"#{u}\">#{u}</option>" unless $session["username"] == u
		}
		dvm << "</select>
				</td>
			</tr><tr>
				<td class='header'>Subject:</td><td><input type='text' name='subject' /></td>
			</tr><tr>
				<td></td>
				<td>
					<textarea name='body' form='mail' rows='4' cols='50'></textarea>
				</td>
			</tr><tr>
				<td></td>
				<td><input name='newmail' type='submit' /></td>
			</tr>
		</table>
	</form>
</div>
"
end

dvm.out
