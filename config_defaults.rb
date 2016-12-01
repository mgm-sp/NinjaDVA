require "ostruct"
$conf = OpenStruct.new
INSTALLDIR = "/var/www/dvmail/"

$conf.domain = ".mgmsp-lab.com"

dbdir = "#{INSTALLDIR}/db"
$conf.userdb = "#{dbdir}/users.db"
$conf.maildb = "#{dbdir}/mail.db"

$conf.clouduserdb = "#{dbdir}/cloudusers.db"
$conf.clouduserfiles = "#{INSTALLDIR}/clonecloud/files"

$conf.pepper = "ayethielu4pheZai"
$conf.default_userpw = "Kooviufeicae0goo"

$conf.chatdb = "#{dbdir}/chat"

$conf.funnypicscsv = "#{dbdir}/funny-pics/pics.csv"
$conf.funnypicsdeletecsv = "#{dbdir}/funny-pics/delete.csv"

$conf.myhomepagedb = "#{dbdir}/myhomepage/"

$conf.location = "Dresden, Germany"

$conf.links = [
	{ :href => "http://myhomepage#{$conf.domain}", :name =>"My Homepage" },
	{ :href => "http://funny-pics#{$conf.domain}", :name => "Funny Pictures" },
	{ :href => "http://scoreboard#{$conf.domain}", :name => "Scoreboard" },
	{ :href => "http://mail#{$conf.domain}",       :name => "mgm-sp Mail" }
]

if File.exists?("#{INSTALLDIR}/config.rb")
	load "#{INSTALLDIR}/config.rb"
end
