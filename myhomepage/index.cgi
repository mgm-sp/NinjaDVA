#!/usr/bin/ruby

require_relative "html"
require "cgi"
$cgi = CGI.new

h = HTML.new("My Homepage")

h.add_css("myhomepage.css")


h << <<NEW
<div id="head">
	<h1>MyHomepage</h1>
	<h2>space for <span>your</span> spam</h2>
</div> 
<div id="content">
<div id="create">
<h1>Create New Homepage</h1>
<form action='new.cgi' method='POST'>
	<label for="url">http://#{$cgi.server_name}/</label><input id="url" size='16' type='text' name='url' value="" />
	<input type='submit' value='Create' />
	<div style='margin-top: 10px; font-size: small'>
	#{$cgi.include?("error") ? CGI.escapeHTML($cgi["error"]) : ""}
	</div>
</form>
</div>
<table>
	<tr>
		<td>
			<img src="1.png" />
			<div><p>
			<h3>Step 1:</h3>
			Choose a name and create your own homepage
			</p></div>
		</td>
		<td>
			<img src="2.png" />
			<div><p>
			<h3>Step 2:</h3>
			Edit the source code of your homepage and save it</p>
			</p></div>
		</td>
	</tr>
	<tr>
		<td>
			<img src="3.png" />
			<div><p>
				<h3>Step 3:</h3>
				Click to view your homepage
			</p></div>
		</td>
		<td>
			<img src="4.png" />
			<div><p>
			<h3>Step 4:</h3>
			Admire your creation
			</p></div>
		</td>
	</tr>
</table>
</div></div>
NEW

h.out($cgi)
