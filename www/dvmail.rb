require "cgi"
require 'cgi/session'
$cgi = CGI.new
$session = CGI::Session.new($cgi)


require_relative "../config_defaults"
require_relative "html"
require "sqlite3"
require "pp"

class Dvmail
	attr_accessor :user, :html, :userdb, :username
	def initialize(username = $session['username'])
		@html = HTML.new("Dvmail")
		@userdb = SQLite3::Database.new($conf.userdb)
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

			user_ary = @userdb.get_first_row("SELECT name,message,groups FROM users WHERE id = ?",@username)
			@user = {
				:name => user_ary[0],
				:message => user_ary[1],
				:groups => user_ary[2].split(", ")
			}


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
	def createuser(id,password)
		@userdb.execute("INSERT INTO users (id, name, password, message, groups)
										VALUES ( ?, ?, ?, ?, ? )", [id,"",password,"","Newbie"])
	end
	def save
		statement = @userdb.prepare("UPDATE users SET name=?,message=?,groups=? WHERE id = ?")
    statement.bind_param 1, @user[:name]
    statement.bind_param 2, @user[:message]
    statement.bind_param 3, @user[:groups].join(", ")
    statement.bind_param 4, @username
    statement.execute
	end
	def <<(htmlbodytext)
		@html << htmlbodytext
	end
	def out
		@html << "</div></body>"
		@html.out($cgi)
	end
end
