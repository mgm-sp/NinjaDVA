#!/usr/bin/ruby


require "yaml"
require_relative "../../config_defaults"
require_relative "../html"
require "cgi"
$cgi = CGI.new

h = HTML.new("My Homepage -- admin")

Dir.glob("#{$conf.myhomepagedb}/*.yaml") {|f|
	hp = YAML::load_file(f)
	h << "<h1>#{File.basename(f).gsub(/.yaml$/,"")}</h1>"
	h << "<textarea class='code'>#{CGI.escapeHTML(hp[:html].body)}</textarea>	"
}

h.add_css("../codemirror/codemirror.css") # needs to be loaded before other css
h.add_css("../myhomepage.css")
h.add_script_file("../codemirror/codemirror.js")
h.add_script_file("../codemirror/css.js")
h.add_script_file("../codemirror/javascript.js")
h.add_script_file("../codemirror/vbscript.js")
h.add_script_file("../codemirror/xml.js")
h.add_script_file("../codemirror/htmlmixed.js")
h.add_script <<JS
var code_ary = document.getElementsByClassName("code");
for (i in code_ary) {
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
