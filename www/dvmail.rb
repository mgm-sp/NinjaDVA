require "cgi"
require 'cgi/session'
$cgi = CGI.new
$session = CGI::Session.new($cgi)
USERS = "../db/users/"

require_relative "html"
require "yaml"
require "pp"

class Dvmail
	attr_accessor :user, :html
	def initialize(username = $session['username'])
		@html = HTML.new("Dvmail")
		@html << "<body>"
		unless (File.basename($0) == "login.cgi" || File.basename($0) == "register.cgi" || $session['username'])
			# stop if unauthorized
			@html.header["status"] = "REDIRECT"
			@html.header["Cache-Control"] = "no-cache"
			@html.header["Location"] = "/login.cgi"
			@html << "</body>"
			out
			exit
		end

		@html << "<div id='head'>Your friendly Webmailer</div>"
		@username = username
		if @username
			raise @username.inspect unless @username =~ /\A[A-Za-z0-9]+\z/

			@user = YAML::load(File.open("#{USERS}/#{@username}.yaml"))

			@menu = ["Inbox", "New Mail", "Addressbook","Edit vCard","Logout"]
			@html << "<div id='tabs'>"
			@html << "<div style='padding-left:2em' class='green'>"
			@html << "Welcome #{@username}"
			@html << "</div>"

			@html << "<ul>"
			@menu.each{|item|
				currenttab= File.basename($0).chomp(".cgi")
				if item.downcase == currenttab
					@html << "<li id='active_tab' class='nonactive_tab'>"
				else
					@html << "<li class='nonactive_tab'>"
				end
				@html << "<a href='#{item.downcase.gsub(" ","_")}.cgi'>#{item}</a></li>"
			}
			@html << "</ul>"
		end
		@html << "</div>"


		@html.add_css("dvmail.css")
		@html << "<div id='content'>"
	end
	def save
		File.open("#{USERS}/#{@username}.yaml","w"){|f|
			f << @user.to_yaml
		}
	end
	def <<(htmlbodytext)
		@html << htmlbodytext
	end
	def out
		@html << "</div></body>"
		@html.out($cgi)
	end
end
