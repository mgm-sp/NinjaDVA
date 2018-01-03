#!/usr/bin/env ruby
#

require_relative "../../config_defaults"
require "cgi"

$cgi = CGI.new
out = ''
Dir.glob("../../dashboard-admin/*.html").each{|htmlfile|
	id = "admin_#{File.basename(htmlfile, ".html")}"
	out << "<div id='#{id}' class='widget adminwidget'>\n"
	out << File.open(htmlfile).read
	out << "\n</div>"
}
out << "<script type='text/javascript'>$('.adminwidget').each(function(){gridster.add_widget($(this), 2,2);});</script>"
$cgi.out(){out}
