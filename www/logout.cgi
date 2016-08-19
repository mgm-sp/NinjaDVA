#!/usr/bin/ruby


$:.push(".")
require "dvmail.rb"
require "pp"
m = Dvmail.new
$session.delete
m.html.header["status"] = "REDIRECT"
m.html.header["Cache-Control"] = "no-cache"
m.html.header["Location"] = "/login.cgi"
m << "You sucessfully logged out!"
m.out
