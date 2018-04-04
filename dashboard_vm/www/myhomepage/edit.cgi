#!/usr/bin/ruby

require_relative "../config_defaults"
require_relative "html"
require "cgi"
$cgi = CGI.new

h = HTML.new("My Homepage")
h.add_css("codemirror/codemirror.css") # needs to be loaded before other css
h.add_css("myhomepage.css")
h.add_script_file("jquery-2.2.3.min.js")

h.add_script <<~JS
$( document ).ready(function() {
	var currentLog = {}
	var fnUpdateLogTable = function(){
		$.getJSON("getlog.cgi", {"url": "#{$cgi["url"]}", "password": "#{$cgi["password"]}"}, function(result){
			if (JSON.stringify(currentLog) !== JSON.stringify(result)){
				currentLog = result;
				$("#logtable > tbody > tr").slice(1).remove();
				result.forEach((e)=>{
					sTableLine = `<tr><td>${e["ADDR"]}</td><td>${e["TIME"]}</td><td>${e["METHOD"]}</td><td>${e["URI"]}</td><td>${e["USER_AGENT"]}</td><td>${(e["REFERER"] ? e["REFERER"] : "")}</td></tr>`;
					$("#logtable > tbody > tr:first").after(sTableLine);
				});
			}
		});
	};
	fnUpdateLogTable();
	setInterval(fnUpdateLogTable, 2000);
});
JS

if $cgi.include?("url") && $cgi["url"] =~ /\A[\w\-_]*\Z/ && File.exists?("#{$conf.myhomepagedb}/#{$cgi["url"]}.yaml")

	require "yaml"
	homepage = YAML::load_file("#{$conf.myhomepagedb}/#{$cgi["url"]}.yaml")
	if homepage[:password] == $cgi["password"]
		h << <<~LINK
			<div>
				The link to your <a href='#{$cgi["url"]}'>homepage</a>: <input value='http://#{$cgi.server_name}/#{$cgi["url"]}' type='text' readonly='readonly' style='width: 50%' />
			</div>
		LINK

		h << <<~EDIT
			<form style='margin-top:2ex; height: 100%' method='post' action='store.cgi'>
			<div>
		EDIT
		h << <<~EDIT
				<textarea id='headereditor' name='header' style='width: 100%; height:100%'>#{CGI.escapeHTML(homepage[:header])}</textarea>
				<input type='hidden' name='url' value='#{$cgi["url"]}' />
				<input type='hidden' name='password' value='#{$cgi["password"]}' />
				<textarea id='codeeditor' name='contents' style='width: 100%; height:100%'>#{CGI.escapeHTML(homepage[:contents])}</textarea>
				<input type='submit' value='Save' />
			</div>
			</form>
		EDIT
		h.add_script_file("codemirror/codemirror.js")
		h.add_script_file("codemirror/css.js")
		h.add_script_file("codemirror/javascript.js")
		h.add_script_file("codemirror/vbscript.js")
		h.add_script_file("codemirror/xml.js")
		h.add_script_file("codemirror/htmlmixed.js")
		h.add_script <<~JS
			var editor = CodeMirror.fromTextArea(document.getElementById("codeeditor"), {
				mode:  {
					name: "htmlmixed",
					scriptTypes: [
						{matches: /\\/x-handlebars-template|\\/x-mustache/i, mode: null},
						{matches: /(text|application)\\/(x-)?vb(a|script)/i, mode: "vbscript"}
					]
				},
				lineNumbers: true,
			});
		JS
		h.add_script_file("codemirror/http.js")
		h.add_script <<~JS
			var editor = CodeMirror.fromTextArea(document.getElementById("headereditor"), {
				mode:  {
					name: "http",
				},
				lineNumbers: true,
			});
		JS

		h << "<h1>Access Log</h1>"
		require "csv"
		fields = ["ADDR","TIME","METHOD","URI","USER_AGENT","REFERER"]
		h << "<table id='logtable' class='requestlog'><tr>#{fields.collect{|e| "<th>#{e}</th>"}.join("")}</tr></table>"

	else
		h.header["status"] = "REDIRECT"
		h.header["Cache-Control"] = "no-cache"
		h.header["Location"] = "/?error=#{CGI.escape("Wrong Password for page #{$cgi["url"]}!")}"
	end

else
	h.header["status"] = "REDIRECT"
	h.header["Cache-Control"] = "no-cache"
	h.header["Location"] = "/"
end

h.out($cgi)
