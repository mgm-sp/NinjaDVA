# coding: utf-8
require "sqlite3"
require_relative "config_defaults"

# Open a database
db = SQLite3::Database.new $conf.userdb

# Create a table
db.execute <<-SQL
  create table users (
  	id TEXT,
    name TEXT,
    password TEXT,
    message TEXT,
    groups TEXT
  );
SQL

# Execute a few inserts
{
"admin" => ["Andi Admin", "3AkdTJBm1", "Leave me alone if you don't want to have trouble.", "Administrator, Checker"],
"siggi" => ["Siggi Sorglos", "3AkdTJBm1", "Die Welt ist schön!", "Dummies"],
"susi" => ["Susi Sorglos", "3AkdTJBm1", "❤ Otto ❤", "Dummies"],
"heidi" => ["Heidi Heimlich", "3AkdTJBm1", "Bitte keine Werbung.", "Support, Hidden"],
"xaver" => ["Xaver Schmidt", "3AkdTJBm1", "Ask me, I will give you support!", "Support"]
}.each do |name,data|
  db.execute "insert into users VALUES ( ?, ?, ?, ?, ? )", [name] + data
end
puts "chown www-data:www-data #{$conf.userdb}"



db = SQLite3::Database.new $conf.maildb

# Create a table
db.execute <<-SQL
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
  db.execute "insert into users VALUES ( ?, ?, ?, ? )", data
end


puts "chown www-data:www-data #{$conf.maildb}"
