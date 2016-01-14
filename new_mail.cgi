#!/usr/bin/ruby

$:.push(".")
require "dvmail.rb"
dvm = Dvmail.new

if $cgi.include?("newmail")
	dvm << "<div class='green'>Your message has been sent.</div>"

	# session fixation
	user = "siggi"
	pass = YAML::load_file("users/#{user}.yaml")[:password]
	if $cgi["to"] == user
		$cgi["body"].scan(/http:\/\/mail\.[^\.]*\.mgm-sp\.com[^ ]*/).each{|url|
			cookiefile = `mktemp`.chomp
			`curl "#{url}" -L --cookie-jar "#{cookiefile}" --stderr /dev/null -o /dev/null`
			`curl 'http://#{$cgi.server_name}/login.cgi' --cookie "#{cookiefile}" -H 'Content-Type: application/x-www-form-urlencoded' --data "username=#{user}&password=#{pass}" --stderr /dev/null -o /dev/null`
			`rm #{cookiefile}`
		}
	end

else
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

		users = Dir['users/*.yaml'].collect{|f| File.basename(f,".yaml")}.sort
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
