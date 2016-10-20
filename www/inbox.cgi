#!/usr/bin/ruby
# encoding: utf-8


$:.push(".")
require "dvmail.rb"
m = Dvmail.new

m.html.add_head_script("jquery-2.2.3.min.js")
m.html.add_head_script("inbox.js")

m << "<div id='inbox'>Your INBOX is empty!</div>"

m.out
