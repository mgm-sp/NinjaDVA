require "ostruct"
$conf = OpenStruct.new

$conf.domain = "mgmsp-lab.com"
$conf.installdir = "/var/www/dvmail/"

dbdir = "#{$conf.installdir}/db"
$conf.userdb = "#{dbdir}/users.db"
$conf.maildb = "#{dbdir}/mail.db"

$conf.chatdb = "#{dbdir}/chat"

$conf.funnypicscsv = "#{dbdir}/funny-pics/pics.csv"
$conf.funnypicsdeletecsv = "#{dbdir}/funny-pics/delete.csv"

$conf.myhomepagedb = "#{dbdir}/myhomepage/"


if File.exists?("#{$conf.installdir}/config.rb")
	load "#{$conf.installdir}/config.rb"
end
