#!/usr/bin/ruby

require_relative "html"
require_relative "../config_defaults"
require "csv"
require "cgi"
require 'cgi/session'
require "json"
$cgi = CGI.new
$session = CGI::Session.new($cgi)

h = HTML.new("Dashboard")

require_relative "../solved"
if $cgi.include?("ping")
	if $cgi["ping"] == ""
		num = `grep ",1,Ping" #{$conf.solutiondb} |wc -l`.chomp
		Solution.new("ping",2,"Ping #{num}")
	else
		Solution.new("ping",10,"Pinged with message #{$cgi['ping']}")
	end
	h.header["status"] = "REDIRECT"
	h.header["Cache-Control"] = "no-cache"
	h.header["Location"] = "/"
	h << "Pong"
	h.out($cgi)
else
	Solution.new("ping",1,"Accessed the Dashboard")
end

h.add_css("dashboard.css")

h << <<HEAD
<div id="top">
<div id="tabs">
<img src='mgm-sp-logo.png' alt='mgm security partners' id="logo" />
<div id="welcome">&nbsp;</div>
<ul>
<li class="nonactive_tab gridnav" style='display:none'>Custom Layout:</li>
<li class="nonactive_tab gridnav" style='display:none'><a href="javascript:revert_grid_layout_to_server()">Reset</a></li>
<li class="nonactive_tab gridnav" style='display:none'><a href="javascript:grid_layout_from_server(true)">Cancel</a></li>
<li class="nonactive_tab gridnav" style='display:none'><a href="javascript:save_grid_layout_to_localstorage()">Save</a></li>
<li class="nonactive_tab gridnav" style='display:none'>&nbsp;</li>
<li class="nonactive_tab">Dashboard</li>
</ul>
</div></div>

<div id='content'>
<div class='gridster'>
HEAD

Dir.glob("../dashboard-widgets/*.html").each{|htmlfile|
	h << File.open(htmlfile).read
}

if File.exists?("#{$conf.dbdir_absolute}/weather.json")
	oWeather = JSON.parse(File.read("#{$conf.dbdir_absolute}/weather.json"))
else
	# set default configuration if weather was not defined yet
	oWeather = {"title"=>"Weather not configured", "locationcode"=>"razupaltuff"}
end

h << <<WEATHERWIDGET
<!-- BEGIN WEATHER WIDGET -->
<div id='weatherwidget' class='widget' data-row="4" data-col="2" data-sizex="2" data-sizey="1">
<div>
<h1>#{oWeather["title"]}</h1>
WEATHERWIDGET
if oWeather.has_key?("imageurl")
	h << "<div id='weather_background' style=\"background-image: url('#{oWeather["imageurl"]}');\">"
end
h << "<div id='weather'></div>"
if oWeather.has_key?("imageurl")
	h << "</div>"
end
h << "</div>"
h << "</div>"
h.add_script <<JS
function unix2human(unixtime){
	var date = new Date(unixtime*1000);
	return date.getHours()+':'+("0"+date.getMinutes()).substr(-2);
}
function updateWeather (){
	$.ajax({
		url: "https://api.openweathermap.org/data/2.5/weather?q=#{oWeather["locationcode"]}&APPID=5d969b625e6133c5ad26588ff570566b&units=metric",
		type: "get",
		success: function(result) {
			var html = '<h2>'+Math.round(result.main.temp)+'&deg;C <img style="vertical-align:middle; display:inline-block; height:3em; margin-left: 0.3em" src="https://openweathermap.org/img/w/' + result.weather[0].icon + '.png"></img></h2>';

			html += '<ul>';
			html += '<li>'+result.weather[0].description+'</li>';
			html += '<li>Wind: '+result.wind.deg+'&deg; '+Math.round(result.wind.speed)+'&nbsp;m/s</li>';
			html += '<li>Sun: '+unix2human(result.sys.sunrise)+'-'+unix2human(result.sys.sunset)+'</li>';
			html += '</ul>';

			$("#weather").html(html);
		},
		error: function(error) {
			$("#weather").html('<p>'+error+'</p>');
			window.setTimeout(updateWeather,1000);
		}
	});
}
$(document).ready(updateWeather);
JS
h << "<!-- END WEATHER WIDGET -->"


h << <<CALENDARWIDGET


<!-- BEGIN CALENDAR WIDGET -->
CALENDARWIDGET


if File.exists?("#{$conf.dbdir_absolute}/calendarconf.json")
	oCalendarConf = JSON.parse(File.read("#{$conf.dbdir_absolute}/calendarconf.json"))
else
	oCalendarConf = {}
end
# set default configuration if json is not existent
[["dayStart","08:00"],["slotDuration","00:30:00"]].each{|conf,value|
	oCalendarConf[conf] = value if oCalendarConf[conf].to_s == ""
}


h << <<CALENDARWIDGET
<div id='calendarwidget' class='widget' data-row="1" data-col="1" data-sizex="2" data-sizey="3">
<div>
<h1>Seminar Schedule</h1>
<div id='calendar'></div>
</div>
</div>
CALENDARWIDGET
h.add_css("fullcalendar/fullcalendar.min.css")
h.add_script_file("fullcalendar/moment.min.js")
h.add_script_file("fullcalendar/fullcalendar.min.js")
h.add_script_file("fullcalendar/locale/de.js") if ENV["HTTP_ACCEPT_LANGUAGE"] =~ /^((?<!en).)*de/
h.add_script <<JS
$(document).ready(function() {
	$('#calendar').fullCalendar({
		header: {
			left: 'prev,next today',
			center: 'title',
			right: 'agendaDay,agendaTwoDays,agendaThreeDays,listWeek'
		},
		views: {
				agendaTwoDays: {
						type: 'agenda',
						duration: { days: 2 },
				},
				agendaThreeDays: {
						type: 'agenda',
						duration: { days: 3 },
				}
		},
		height: 250,
		defaultView: 'agendaDay',
		navLinks: false, // can click day/week names to navigate views
		editable: false,
		eventLimit: true, // allow "more" link when too many events
		nowIndicator: true,
		scrollTime: "#{oCalendarConf["dayStart"]}",
		slotDuration: '#{oCalendarConf["slotDuration"]}',
		events: "events.cgi"
	});
});
JS

h << "<!-- END CALENDAR WIDGET -->"


h << "\n\n<!-- BEGIN SLIDES WIDGET -->"
h.add_script <<SCRIPT
function chooseMaterial(slide){
	$("#slides iframe")[0].contentWindow.postMessage(slide,"*")
}
SCRIPT

# get default slide
if File.exists?("#{$conf.dbdir_absolute}/defaultslide.json")
oDefaultSlide = JSON.parse(File.read("#{$conf.dbdir_absolute}/defaultslide.json"))
else
# set default configuration if defaultslide was not defined yet
oDefaultSlide = {"defaultSlide"=>""}
end

h << <<SLIDES
<div id='slides' class='widget' data-row="1" data-col="4" data-sizex="3" data-sizey="6">
<div>
<h1 style='height:5%; margin: 0'>Lecture Material</h1>
<iframe style='border: none;width:100%; height:95%' src='//clonecloud.#{$conf.domain}/view.cgi?default=#{oDefaultSlide["defaultSlide"]}'></iframe>
</div>
</div>
<!-- END SLIDES WIDGET -->
SLIDES


h << <<LINK

<!-- BEGIN LINK WIDGET -->
<div id='linkwidget' class='widget' data-row="1" data-col="3" data-sizex="1" data-sizey="3">
<div>
<h1>Favourite Links</h1>
<ul id='fav' style='position: inline'>
LINK

#get links from json
links = []
if File.exists?("#{$conf.dbdir_absolute}/links.json")
	add_links = []
	json_links = JSON.parse(File.read("#{$conf.dbdir_absolute}/links.json"), :symbolize_names => true)
	json_links.each{|linkhash|
		if linkhash[:active] == true
			add_links.push(linkhash)
		end
	}
	links += add_links
end

links.each{|l|
	h << "<li><a href='#{l[:href]}'>"
	if l[:icon] != ""
		h << "<img alt='#{l[:name][0]}' src='#{l[:icon]}' height='8' />&nbsp;"
	end
	h << "#{l[:name]}</a></li>"
}
h << "</ul>"

h << <<LINK
</div>
</div>
<!-- END LINK WIDGET -->
LINK


h << "</div>"
h << "</div>"
h.add_css("jquery.gridster.min.css")
h.add_css("wickedpicker.min.css")

h.add_head_script("jquery-2.2.3.min.js")
h.add_head_script("jquery.gridster.min.js")
h.add_head_script("wickedpicker.min.js")


h.add_script_file("grid.js")
h << <<CSS
<style>
.gridster .preview-holder{
	background: #bbbbbb;
	border: medium none;
	border-radius: 0;
}
.widget h1 {
	cursor: move;
}
</style>
CSS

h.add_script_file("admin.js")
h << <<FOOTER
<div id=footer>
<div id="ft_cont">
	<div> <a href="https://www.mgm-sp.com/impressum/">Imprint</a> </div>
	<div> <a href="?ping">(c)</a> 2018 mgm security p<a id='toggleAdminInterface' href='javascript:toggleAdminInterface()'>a</a>rtners GmbH </div>
	<div><ul id="icons">
FOOTER
links.each{|l|
	if l[:icon] != ""
		h << "<li><a href='#{l[:href]}' title='#{l[:name]}'>"
		h << "<img alt='#{l[:name][0]}' src='#{l[:icon]}' />"
		h << "</a></li>"
	end
}
h << <<FOOTER
	</ul></div>
	</div>
</div>
FOOTER

h.out($cgi)
