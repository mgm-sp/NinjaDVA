#!/usr/bin/env ruby
#

require_relative "../../config_defaults"
require "cgi"

$cgi = CGI.new
out = ''
Dir.glob("../../dashboard-admin/*.html").each{|htmlfile|
	id = "admin_#{File.basename(htmlfile, ".html")}"
	out << "<div id='#{id}' class='widget adminwidget' data-row='1' data-col='1' data-sizex='1' data-sizey='1'>\n"
	out << File.open(htmlfile).read
	out << "\n</div>"
}
out << "<script type='text/javascript'>gridster.add_widget($('.adminwidget'));</script>"
$cgi.out(){out}
