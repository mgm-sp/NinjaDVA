#!/usr/bin/ruby
# encoding: utf-8
MAILDB = "../db/mail.db"
$:.push(".")
require "pp"
require "json"
require "dvmail.rb"
m = Dvmail.new

ret = []
maildb = SQLite3::Database.new(MAILDB)
maildb.query("SELECT * FROM mail WHERE recipient = ?" + " OR recipient = ?"*m.user[:groups].size,
						 [m.username] + m.user[:groups].collect{|g| "group:#{g}"}){|result|
	result.reverse_each{|mail|
		ret << {
			:sender => mail[0],
			:recipient => mail[1],
			:subject => mail[2],
			:body => mail[3]
		}
	}
}

if $cgi.include?("jsonp") && $cgi["jsonp"] =~ /\A[A-Za-z0-9]+\z/
	$cgi.out{"#{$cgi["jsonp"]}(#{ret.to_json})"}
else
	$cgi.out{ret.to_json}
end

