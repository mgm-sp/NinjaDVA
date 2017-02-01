require "ostruct"

class Configuration < OpenStruct
	def clouduserdb
		"#{self.dbdir_absolute}/cloudusers.db"
	end
	def cloudfiles
		"#{self.dbdir_absolute}/../files/"
	end
	def userdb
		"#{self.dbdir_absolute}/users.db"
	end
	def maildb
		"#{self.dbdir_absolute}/mail.db"
	end
	def chatdb
		"#{self.dbdir_absolute}/chat"
	end
	def funnypicscsv
		"#{self.dbdir_absolute}/funny-pics/pics.csv"
	end
	def funnypicsdeletecsv
		"#{self.dbdir_absolute}/funny-pics/delete.csv"
	end
	def myhomepagedb
		"#{self.dbdir_absolute}/myhomepage/"
	end
	def solutiondb
		"#{self.dbdir_absolute}/solves.csv"
	end
	def dbdir_absolute
		"#{INSTALLDIR}/#{self.dbdir}"
	end
	def load(file)
		self.dbdir = "config/#{File.dirname(file)}/db/"
		require_relative "#{INSTALLDIR}/config/#{file}"
	end
end

$conf = Configuration.new
INSTALLDIR = "/var/www/dvmail/"
require_relative "#{INSTALLDIR}/seminar"

$conf.domain = ".mgmsp-lab.com"

$conf.dbdir = "db"

$conf.pepper = "ayethielu4pheZai"
$conf.default_userpw = "Kooviufeicae0goo"


$conf.location = "Dresden, Germany"

$conf.links = [
	{ :href => "http://myhomepage#{$conf.domain}", :name => "My Homepage" },
	{ :href => "http://funny-pics#{$conf.domain}", :name => "Funny Pictures" },
	{ :href => "http://scoreboard#{$conf.domain}", :name => "Scoreboard" },
	{ :href => "http://mail#{$conf.domain}",       :name => "Mail" }
]

$conf.dashboard_grid_layout = '{"timewidget":{"col":"1","row":"4","sizex":"1","sizey":"1"},"mailwidget":{"col":"1","row":"5","sizex":"3","sizey":"2"},"weatherwidget":{"col":"2","row":"4","sizex":"2","sizey":"1"},"calendarwidget":{"col":"1","row":"1","sizex":"2","sizey":"3"},"slides":{"col":"4","row":"1","sizex":"3","sizey":"6"},"linkwidget":{"col":"3","row":"1","sizex":"1","sizey":"3"}}'

require "yaml"
$conf.exercises = Dir.glob("#{INSTALLDIR}/challenge-descriptions/*.yaml").sort_by{|f|
	YAML::load_file(f)[:category]
}.collect{|f| File.basename(f,".yaml")}

if File.exists?("#{INSTALLDIR}/config/config.rb")
	load "#{INSTALLDIR}/config/config.rb"
else
	puts
	puts "You need to configure the server. Please copy config_sample.rb to config/config.rb."
	exit
end
