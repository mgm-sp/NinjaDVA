#!/usr/bin/ruby

DB="../../db/myhomepage/"

require "yaml"
require_relative "../html"
require "cgi"
$cgi = CGI.new

h = HTML.new("My Homepage -- admin")

Dir.glob("#{DB}/*.yaml") {|f|
	hp = YAML::load_file(f)
	h << "<h1>#{File.basename(f).gsub(/.yaml$/,"")}</h1>"
	h << "<pre><code>#{CGI.escapeHTML(hp[:html].body)}</code></pre>"
}

h.add_css("default.css")
h.add_script_file("highlight.pack.js")
h.add_script("hljs.initHighlightingOnLoad();")

h.out($cgi)
