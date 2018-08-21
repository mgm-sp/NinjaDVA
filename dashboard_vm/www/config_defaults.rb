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
	def myhomepagedb
		"#{self.dbdir_absolute}/myhomepage/"
	end
	def solutiondb
		"#{self.dbdir_absolute}/solves.csv"
	end
	def dbdir_absolute
		"#{INSTALLDIR}/#{self.dbdir}"
	end
	def load(file) #legacy
		self.dbdir = "config/#{File.dirname(file)}/db/"
	end
	def set_db_dir(dir)
		self.dbdir = "config/#{dir}/db/"
	end
	def remote_solution_handler_url
		"http://dashboard.#{$conf.domain}/solve_srv.cgi"
	end
end

$conf = Configuration.new
INSTALLDIR = "/var/www/"

$conf.domain = "mgmsp-lab.com"

$conf.dbdir = "db"

$conf.pepper = "Luiphoh3gooz9pai"
$conf.default_userpw = "shohseib9Phi6euL"




$conf.dashboard_grid_layout = '{"timewidget":{"col":"6","row":"1","sizex":"1","sizey":"1"},"customwidget":{"col":"3","row":"1","sizex":"3","sizey":"1"},"weatherwidget":{"col":"1","row":"5","sizex":"1","sizey":"2"},"calendarwidget":{"col":"1","row":"1","sizex":"2","sizey":"4"},"slides":{"col":"3","row":"2","sizex":"4","sizey":"5"},"linkwidget":{"col":"2","row":"5","sizex":"1","sizey":"2"}}'



require "yaml"
$conf.exercises = Dir.glob("#{INSTALLDIR}/challenge-descriptions/*.yaml").sort_by{|f|
	YAML::load_file(f)[:category]
}.collect{|f| File.basename(f,".yaml")}

if File.exists?("#{INSTALLDIR}/config/config.rb")
	load "#{INSTALLDIR}/config/config.rb"
else
	require "fileutils"
	FileUtils.cp("#{INSTALLDIR}/config_sample.rb","#{INSTALLDIR}/config/config.rb")
	puts
	puts "A default config was created. You may edit $YOURCONFIGDIR/config.rb"

	examplecustomer = "example"
	Dir.mkdir("#{INSTALLDIR}/config/#{examplecustomer}") unless Dir.exists?("#{INSTALLDIR}/config/#{examplecustomer}")
	unless File.exists?("#{INSTALLDIR}/config/htdigest")
		require "digest"
		user = "admin"
		realm = "Restricted Area"
		File.open("#{INSTALLDIR}/config/htdigest","w"){|f|
			f << "#{user}:#{realm}:#{Digest::MD5.hexdigest("#{user}:#{realm}:#{$conf.default_userpw}")}\n"
		}
		puts "A default password file was created at $YOURCONFIGDIR/htdigest with the default password in config.rb!"
		puts "You need this Password: after reloading the webpage: #{$conf.default_userpw} (username: admin)!"
	end
	puts "Reload this page when you finished customizing your config."
	exit
end

unless Dir.exists?($conf.dbdir_absolute) || (File.basename($0) == "setup_db.cgi")
	puts "Content-Type: text/html"
	puts
	puts "DB does not exist, you need to run <a href='http://dashboard.#{$conf.domain}/admin/setup_db.cgi'>dashboard/admin/setup_db.cgi</a>.<br/>"
	puts "You need the password from $YOURCONFIGDIR/config.rb for the first access to setup_db.cgi (username: admin)!"
	exit
end
