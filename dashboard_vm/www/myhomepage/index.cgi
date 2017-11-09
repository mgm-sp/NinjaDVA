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
<form action='new.cgi' method='post'>
<div>
	<label for="url">http://#{$cgi.server_name}/</label><input autofocus='autofocus' id="url" size='16' type='text' name='url' value="" />
	<input type='submit' value='Create' />
	<div style='margin-top: 10px; font-size: small'>
	#{$cgi.include?("error") ? CGI.escapeHTML($cgi["error"]) : ""}
	</div>
	</div>
</form>
</div>
<table id='explaination'>
	<tr>
		<td>
			<img alt="Step 1" src="1.png" />
			<div>
			<h3>Step 1:</h3>
			Choose a name and create your own homepage
			</div>
		</td>
		<td>
			<img alt="Step 2" src="2.png" />
			<div>
			<h3>Step 2:</h3>
			Edit the source code of your homepage and save it
			</div>
		</td>
	</tr>
	<tr>
		<td>
			<img alt="Step 3" src="3.png" />
			<div>
				<h3>Step 3:</h3>
				Click to view your homepage
			</div>
		</td>
		<td>
			<img alt="Step 4" src="4.png" />
			<div>
			<h3>Step 4:</h3>
			Admire your creation
			</div>
		</td>
	</tr>
</table>
</div>
NEW

h.out($cgi)
