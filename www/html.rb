# coding: utf-8
############################################################################
# Copyright 2009,2010 Benjamin Kellermann                                  #
#                                                                          #
# This file is part of dudle.                                              #
#                                                                          #
# Dudle is free software: you can redistribute it and/or modify it under   #
# the terms of the GNU Affero General Public License as published by       #
# the Free Software Foundation, either version 3 of the License, or        #
# (at your option) any later version.                                      #
#                                                                          #
# Dudle is distributed in the hope that it will be useful, but WITHOUT ANY #
# WARRANTY; without even the implied warranty of MERCHANTABILITY or        #
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public     #
# License for more details.                                                #
#                                                                          #
# You should have received a copy of the GNU Affero General Public License #
# along with dudle.  If not, see <http://www.gnu.org/licenses/>.           #
############################################################################

class HTML
	attr_accessor :body, :header
	attr_reader :relative_dir
	def initialize(title, relative_dir = "")
		@title = title
		@relative_dir = relative_dir
		@header = {}
		@header["type"] = "text/html"
#		@header["type"] = "application/xhtml+xml"
		@header["charset"] = "utf-8"

		@body = ""
		@htmlheader = ''
		@css = []
		@atom = []
	end
	def head
		ret = <<HEAD
<head>
	<meta http-equiv="Content-Type" content="#{@header["type"]}; charset=#{@header["charset"]}" /> 
	<meta http-equiv="Content-Style-Type" content="text/css" />
	<title>#{@title}</title>
	<link rel="shortcut icon" href="/favicon.ico" type="image/vnd.microsoft.icon">
HEAD

		@css = [@css[0]] + @css[1..-1].sort unless @css.empty?
		@css.each{|title,href|
			titleattr = "title='#{title}'" if title != ""
			ret += "<link rel='stylesheet' type='text/css' href='#{@relative_dir}#{href}' #{titleattr} media='screen, projection, tv, handheld'/>\n"
			ret += "<link rel='stylesheet' type='text/css' href='#{@relative_dir}#{href}' media='print' />\n" if title == "print"
		}

		@atom.each{|href|
			ret += "<link rel='alternate'  type='application/atom+xml' href='#{@relative_dir}#{href}' />\n"
		}

		ret += @htmlheader

		ret += "</head>"
		ret
	end
	def add_css(href, title = "", default = false)
		if default
			@css.unshift([title,href])
		else
			@css << [title,href]
		end
	end
	def add_atom(href)
		@atom << href
	end
	def add_cookie(key,value,path,expiretime)
		c = CGI::Cookie.new(key, value)
		c.path = path
		c.expires = expiretime
		@header["cookie"] ||= []
		@header["cookie"] << c
	end
	def add_head_script(file)
		add_html_head("<script type='text/javascript' src='#{@relative_dir}#{file}'></script>")
	end
	def add_script_file(file)
		self << "<script type='text/javascript' src='#{@relative_dir}#{file}'></script>"
	end
	def add_script(script)
		self << <<SCRIPT
<script type="text/javascript">
// <![CDATA[
#{script}
// ]]>
</script>
SCRIPT
	end
	def << (bodycontent)
		@body += bodycontent.chomp + "\n"
	end
	def add_html_head(headercontent)
		@htmlheader += headercontent.chomp + "\n"
	end

	def out(cgi)
		#FIXME: quick and dirty fix for encoding problem
		{ 
			"ö" => "&ouml;",
			"ü" => "&uuml;",
			"ä" => "&auml;",
			"Ö" => "&Ouml;",
			"Ü" => "&Uuml;",
			"Ä" => "&Auml;",
			"ß" => "&szlig;",
			"–" => "&#8211;",
			"„" => "&#8222;",
			"“" => "&#8220;",
			"”" => "&#8221;",
			"✔" => "&#10004;",
			"✘" => "&#10008;",
			"◀" => "&#9664;",
			"▶" => "&#9654;",
			"✍" => "&#9997;",
			"✖" => "&#10006;",
			"•" => "&#8226;",
			"▾" => "&#9662;",
			"▴" => "&#9652;"
		}.each{|from,to|
			@body.gsub!(from,to)
		}
#		@body.gsub!(/./){|char|
#			 code = char[0]
#			 code > 127 ? "&##{code};" : char
#		}
		cgi.out(@header){
			<<HEAD
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
#{head}
#{@body}
</html>
HEAD
		}
	end
end

