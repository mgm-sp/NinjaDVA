require "ostruct"

class Configuration < OpenStruct
	def clouduserdb
		"#{self.dbdir_absolute}/cloudusers.db"
	end
	def clouduserfiles
		"#{INSTALLDIR}/clonecloud/files"
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
end

$conf = Configuration.new
INSTALLDIR = "/var/www/dvmail/"

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

require "yaml"
$conf.exercises = Dir.glob("#{INSTALLDIR}/challenge-descriptions/*.yaml").sort_by{|f|
	YAML::load_file(f)[:category]
}.collect{|f| File.basename(f,".yaml")}

if File.exists?("#{INSTALLDIR}/config.rb")
	load "#{INSTALLDIR}/config.rb"
end
