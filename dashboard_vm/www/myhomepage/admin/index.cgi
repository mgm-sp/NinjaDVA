#!/usr/bin/ruby


require "yaml"
require_relative "../../config_defaults"
require_relative "../html"
require "cgi"
$cgi = CGI.new

h = HTML.new("My Homepage -- admin")

Dir.glob("#{$conf.myhomepagedb}/*.yaml") {|f|
        url = File.basename(f).gsub(/.yaml$/,"")
        if !$cgi.include?("url") || $cgi["url"] == url
                hp = YAML::load_file(f)
                if $cgi.include?("url")
                        h << "<h1><a href='.'>#{url}</a></h1>"
                else
                        h << "<h1><a href='?url=#{url}'>#{url}</a></h1>"
                end
                h << "<textarea class='header'>#{CGI.escapeHTML(hp[:header])}</textarea>        "
                h << "<textarea class='code'>#{CGI.escapeHTML(hp[:contents])}</textarea>        "
        end
}

h.add_css("../codemirror/codemirror.css") # needs to be loaded before other css
h.add_css("../myhomepage.css")
h.add_script_file("../codemirror/codemirror.js")
h.add_script_file("../codemirror/css.js")
h.add_script_file("../codemirror/http.js")
h.add_script_file("../codemirror/javascript.js")
h.add_script_file("../codemirror/vbscript.js")
h.add_script_file("../codemirror/xml.js")
h.add_script_file("../codemirror/htmlmixed.js")
h.add_script <<JS
var header_ary = document.getElementsByClassName("header");
var i;
for (i=0; i< header_ary.length; i++) {
  var editor = CodeMirror.fromTextArea(header_ary[i], {
                mode:  {
                        name: "http",
                },
                lineNumbers: true,
        });
};
var code_ary = document.getElementsByClassName("code");
for (i=0; i< code_ary.length; i++) {
  var editor = CodeMirror.fromTextArea(code_ary[i], {
                mode:  {
                        name: "htmlmixed",
                        scriptTypes: [
                                {matches: /\\/x-handlebars-template|\\/x-mustache/i, mode: null},
        {matches: /(text|application)\\/(x-)?vb(a|script)/i, mode: "vbscript"}
      ]
    },
    readOnly: true,
    lineNumbers: true,
  });
};
JS

h.out($cgi)
