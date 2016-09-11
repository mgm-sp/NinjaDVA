require "sqlite3"

# Open a database
db = SQLite3::Database.new "db/users.db"

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
"xaver" => ["Xaver Schmidt", "3AkdTJBm1", "Ask me, I will give you support!", "Support"]
}.each do |name,data|
  db.execute "insert into users VALUES ( ?, ?, ?, ?, ? )", [name] + data
end

puts "chown www-data:www-data db/users.db"
