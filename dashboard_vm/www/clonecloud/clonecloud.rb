require "cgi"
require 'cgi/session'
$cgi = CGI.new
$session = CGI::Session.new($cgi)


require_relative "../config_defaults"
require_relative "html"
require "sqlite3"
require "argon2"
require "pp"

class CloneCloud
	attr_accessor :user, :html, :userdb, :username
	def initialize(username = $session['username'])
		@html = HTML.new("CloneCloud")
		@userdb = SQLite3::Database.new($conf.clouduserdb)
		unless (File.basename($0) == "login.cgi" || $session['username'])
			# stop if unauthorized
			@html.header["status"] = "REDIRECT"
			@html.header["Cache-Control"] = "no-cache"
			@html.header["Location"] = "/login.cgi?return_url=#{File.basename($0)}"
			out
			exit
		end

		@username = username
		if @username
			raise @username.inspect unless @username =~ /\A[A-Za-z0-9]+\z/

			@html << "<div id='header'>"
			@html << '<img src="/clone.png" id="clone_s" />'
			@html << "<div id='clone'>cloneCloud</div>"
			welcomemessage = "Welcome #{@username}"

			@menu = ["Logout"]
		else
			@menu = []
			@html << "<div>"
			welcomemessage = "&nbsp;"
		end
		@html << "<div id='tabs'>"
		@html << "<div id='welcome'>"
		@html << welcomemessage
		@html << "</div>"

		@html << "<ul>"
		@menu.each{|item|
			currenttab= File.basename($0).chomp(".cgi")
			if item.downcase.gsub(" ","_") == currenttab
				@html << "<li id='active_tab'>"
			else
				@html << "<li class='nonactive_tab'>"
			end
			@html << "<a href='#{item.downcase.gsub(" ","_")}.cgi' #{'target="_blank"' if item=='Chat'}>#{item}</a></li>"
		}
		@html << "</ul>"
		@html << "</div>"
		@html << "</div>"


		@html.add_css("clonecloud.css")
		@html << "<div id='content'>"
	end
	def createuser(id,password)
		pwhash = Argon2::Password.new(secret: $conf.pepper).create(password)
		@userdb.execute("INSERT INTO users (id, name, password, message, groups)
										VALUES ( ?, ?, ?, ?, ? )", [id,"",pwhash,"","Newbie"])
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
		@html << "<div id='bg'>"
		@html << "</div>"
		@html << "</div>"
		@html.out($cgi)
	end
end
