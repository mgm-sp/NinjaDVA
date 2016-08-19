#!/usr/bin/ruby

$:.push(".")
require "dvmail.rb"
dvm = Dvmail.new

dvm << "<div style='width: 30em'>"
users = Dir["#{USERS}/*.yaml"].collect{|f| File.basename(f,".yaml")}.sort
users.each{|u|
	user = YAML::load_file("#{USERS}/#{u}.yaml")
	dvm << "<fieldset><legend>vCard user #{u}</legend>
<table>
	<tr>
   	<td>Name:   </td><td>#{CGI.escapeHTML(user[:name] == "" ? "<<not set yet>>" : user[:name])}</td>
	</tr><tr>
   	<td>Message:</td><td>#{CGI.escapeHTML(user[:message] == "" ? "<<not set yet>>" : user[:message])}</td>
	</tr><tr>
   	<td>Groups: </td><td>#{CGI.escapeHTML(user[:groups].join(', '))}</td>
	</tr>
</table>
  </fieldset>
	"
}
dvm << "</div>"
dvm.out
