#!/usr/bin/ruby

$:.push(".")
require "clonecloud.rb"
cc = CloneCloud.new

cc << <<FILES
<div class='files'>
<ul>
FILES
cc << Dir.entries("files/").select{|f| f != "." && f != ".."}.collect{|f|
	"<li><a href='files/#{f}'>#{f}</a></li>"
}.join("\n")
cc << "</ul></div>"


cc.out
