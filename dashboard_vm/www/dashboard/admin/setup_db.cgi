#!/usr/bin/ruby
# coding: utf-8

out = ""

require "sqlite3"

$ignore_db_error = true
require_relative "../../config_defaults"

require "argon2"
def argon(pw)
	return Argon2::Password.new(secret: $conf.pepper).create(pw)
end

unless Dir.exists?($conf.dbdir_absolute)

chown = []

[
	File.dirname($conf.dbdir_absolute),
	$conf.dbdir_absolute,
	File.dirname($conf.userdb),
	$conf.myhomepagedb,
	$conf.cloudfiles
].each{|dir|
	Dir.mkdir(dir) unless Dir.exists?(dir)
	chown << dir
}


require "digest"
user = "admin"
realm = "Restricted Area"
File.open("#{INSTALLDIR}/config/htdigest","w"){|f|
	f << "#{user}:#{realm}:#{Digest::MD5.hexdigest("#{user}:#{realm}:#{$conf.default_userpw}")}\n"
}


##########################
# Clone Cloud users
clouduserdb = SQLite3::Database.new $conf.clouduserdb

# Create a table
clouduserdb.execute <<-SQL
  create table users (
    id TEXT,
    password TEXT
  );
SQL

# Execute a few inserts
{
	"susi" => [argon($conf.default_userpw)]
}.each do |name,data|
  clouduserdb.execute "insert into users VALUES ( ?, ? )", [name] + data
end
chown << $conf.clouduserdb

File.open($conf.cloudfiles+"/Wichtig-unbedingt-lesen-README","w") {|f|
	f << "Diese Cloud hat keinen Virenschutz!"
}

################################
# Solutions

File.open($conf.solutiondb, "w"){|f|
	f.puts 'challenge,ip,state,comment,time'
}
chown << $conf.solutiondb


require "fileutils"
FileUtils.chown("www-data","www-data", chown, :verbose => true)
#out << "chown www-data:www-data #{chown.join(" ")}"

else
	out << "Directory #{$conf.dbdir} already exists... Please delete it if you want to clean up the database!"
end

[
	[$conf.cloudfiles,"#{INSTALLDIR}/clonecloud/files"],
	#[$conf.dbdir,"#{INSTALLDIR}/db"]
].each{|a,b|
	File.unlink(b) if File.symlink?(b)
	File.symlink(a,b)
}

puts
if out != ""
	puts "Setup finished with the following output:"
	puts out
else
	puts "Setup finished successfully."
end
