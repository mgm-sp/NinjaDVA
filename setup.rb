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
