# coding: utf-8
require "sqlite3"
require_relative "config_defaults"

chown = []

[
	File.dirname($conf.userdb),
	$conf.chatdb,
	File.dirname($conf.funnypicscsv),
	$conf.myhomepagedb
].each{|dir|
	Dir.mkdir(dir) unless Dir.exists?(dir)
	chown << dir
}

# Open a database
userdb = SQLite3::Database.new $conf.userdb

# Create a table
userdb.execute <<-SQL
  create table users (
  	id TEXT,
    name TEXT,
    password TEXT,
    message TEXT,
    groups TEXT
  );
SQL

require "argon2"
def argon(pw)
	return Argon2::Password.new(secret: $conf.pepper).create(pw)
end
# Execute a few inserts
{
"alice" => ["Alice Wonder",   Digest::MD5.hexdigest("Password1"), "Follow the white Rabbit", "Newbies"],
"bob"   => ["Bob Builder",    Digest::MD5.hexdigest("Password1"), "Yes we can", "Newbies"],
"wolle" => ["W. S.",          Digest::MD5.hexdigest("Gewinner"), "Das muss alles sicherer werden!", "Sicherheitsverantwortlich"],
"admin" => ["Andi Admin",     argon($conf.default_userpw), "Leave me alone if you don't want to have trouble.", "Administrator, Checker"],
"siggi" => ["Siggi Sorglos",  argon($conf.default_userpw), "Die Welt ist schön!", "Dummies"],
"susi"  => ["Susi Sorglos",   argon($conf.default_userpw), "❤ Otto ❤", "Dummies"],
"heidi" => ["Heidi Heimlich", argon($conf.default_userpw), "Bitte keine Werbung.", "Support, Hidden"],
"xaver" => ["Xaver Schmidt",  argon($conf.default_userpw), "Ask me, I will give you support!", "Support"]
}.each do |name,data|
  userdb.execute "insert into users VALUES ( ?, ?, ?, ?, ? )", [name] + data
end
chown << $conf.userdb



maildb = SQLite3::Database.new $conf.maildb

# Create a table
maildb.execute <<-SQL
  create table mail (
  	sender TEXT,
    recipient TEXT,
    subject TEXT,
    body TEXT
  );
SQL
[
	["Siggi Sorglos",              "group:Administrator","Backdoor Password for all Clients", 
	'Dear Colleagues

Please do not forget our local administrator password which is valid for
all our Windows client computers: "Start123"

Best, Siggi'],
	["Siggi Sorglos",              "xaver","Grillen",
"Hallo Xaver Sebastian,

bleibts beim Grillen heute Abend?

Ciao, Siggi"
],
	["Fräulein Müller-Wachtendonk","siggi","Der Mensch macht's!",
	"Sehr geehrter Herr Sorglos,

vielen Dank für die vielen schönen Produktionen. Ich hoffe Sie denken
immer an unseren gemeinsamen Leitsatz:

Der Mensch macht's!

Viele Grüße,
Müller-Wachtendonk"
],
	["Fön",                        "susi", "Küss mich, ich bin ein verzauberter Königssohn!",
"Hallo Susi, ich bin es, dein Fön…

…und ich liebe dein goldenes Haar…"]

].each do |data|
  maildb.execute "insert into mail VALUES ( ?, ?, ?, ? )", data
end

chown << $conf.maildb



##### funny-pics
File.open($conf.funnypicscsv, "w"){|f|
	f.puts '"sid","url"'
	f.puts '"example","http://cdn.meme.am/instances/250x/64647060.jpg"'
	f.puts '"example","http://cdn.meme.am/instances/250x/41586830.jpg"'
}
File.open($conf.funnypicsdeletecsv, "w"){|f|
	f.puts '"sid","url"'
}

chown << $conf.funnypicscsv
chown << $conf.funnypicsdeletecsv

puts "chown www-data:www-data #{chown.join(" ")}"
