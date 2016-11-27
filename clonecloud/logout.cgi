#!/usr/bin/ruby


$:.push(".")
require "clonecloud.rb"
require "pp"
m = CloneCloud.new
$session.delete
m.html.header["status"] = "REDIRECT"
m.html.header["Cache-Control"] = "no-cache"
m.html.header["Location"] = "/"
m << "You sucessfully logged out!"
m.out
