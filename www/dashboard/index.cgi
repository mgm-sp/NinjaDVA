#!/usr/bin/ruby

require_relative "html"
require_relative "../config_defaults"
require "csv"
require "cgi"
require 'cgi/session'
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


timewidget = <<CONTENT
<div id='timewidget' class='widget' data-row="4" data-col="1" data-sizex="1" data-sizey="1">
<div>
<h1>Current Time</h1>
<div id="clock">
      <div id="clk_bg">88:88:88</div>
      <div id="txt">10:11:59</div>
</div>
</div>
</div>
CONTENT
h.add_script <<TIMEWIDGET
function startTime() {
    var today = new Date();
    var h = today.getHours();
    var m = today.getMinutes();
    var s = today.getSeconds();
    m = checkTime(m);
    s = checkTime(s);
    if ( h >= 10 ) {
	    document.getElementById('txt').innerHTML =
        h + ":" + m + ":" + s;
    } else {
        document.getElementById('txt').innerHTML =
        '&nbsp'+h + ":" + m + ":" + s;
	}
    var t = setTimeout(startTime, 500);
}
function checkTime(i) {
    if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
    return i;
}
$(document).ready(startTime);
TIMEWIDGET

h << timewidget



h << <<MAILWIDGET


<!-- BEGIN MAIL WIDGET -->
MAILWIDGET
h.add_script_file("mail.js")

h << <<MAILWIDGET
<div id='mailwidget' class='widget' data-row="5" data-col="1" data-sizex="3" data-sizey="2">
<div>
<h1>New Mail</h1>
<div id='inbox'>Fetching new mail...</div>
</div>
</div>
MAILWIDGET
#h.add_script_file("http://mail.#{$conf.domain}/api/mail.cgi?jsonp=updateMail")

h << "<!-- END MAIL WIDGET -->"

h << "\n"*3

h << <<WEATHERWIDGET
<!-- BEGIN WEATHER WIDGET -->
<div id='weatherwidget' class='widget' data-row="4" data-col="2" data-sizex="2" data-sizey="1">
<div>
<h1>#{$conf.location}</h1>
WEATHERWIDGET
if File.exists?("#{$conf.cloudfiles}/#{$conf.location}.jpg")
	h << "<div id='weather_background' style=\"background-image: url('http://clonecloud.#{$conf.domain}/files/#{$conf.location}.jpg');\">"
end
h << "<div id='weather'></div>"
if File.exists?("#{$conf.cloudfiles}/#{$conf.location}.jpg")
	h << "</div>"
end
h << "</div>"
h << "</div>"
h.add_script_file("jquery.simpleWeather.min.js")
h.add_script <<JS
function updateWeather (){
	$.simpleWeather({
		location: '#{$conf.location}',
		unit: 'c',
		success: function(weather) {
			html = '<h2><i class="icon-'+weather.code+'"></i> '+weather.temp+'&deg;'+weather.units.temp+'</h2>';
			html = '<h2><i class="icon-'+weather.code+'"></i>'+weather.temp+'&deg;'+weather.units.temp+'<img style="vertical-align:middle; display:inline-block; height:3em; margin-left: 0.3em" src="'+weather.forecast[0].image+'"></img></h2>';

			html += '<ul>';
			html += '<li>'+weather.city+', '+weather.region+'</li>';
			html += '<li class="currently">'+weather.currently+'</li>';
			html += '<li>'+weather.wind.direction+' '+weather.wind.speed+' '+weather.units.speed+'</li>';
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
h.add_script_file("fullcalendar/locale/de.js")
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
            buttonText: '2 Tage'
        },
        agendaThreeDays: {
            type: 'agenda',
            duration: { days: 3 },
            buttonText: '3 Tage'
        }
		},
		height: 250,
		defaultView: 'agendaDay',
		navLinks: false, // can click day/week names to navigate views
		editable: false,
		eventLimit: true, // allow "more" link when too many events
		nowIndicator: true,
		scrollTime:  "#{($conf.events.start-0.5/24).strftime('%H:%M')}",
		slotDuration: '00:30:00',
		events: "events.cgi"
	});
});
JS

h << "<!-- END CALENDAR WIDGET -->"


h.add_script_file("slides.js")
h << <<SLIDES

<!-- BEGIN SLIDES WIDGET -->
<div id='slides' class='widget' data-row="1" data-col="4" data-sizex="3" data-sizey="6">
<div>
<h1 style='height:5%; margin:0; padding:0;display:flex;justify-content:space-between'>Lecture Material<img id='fslink' style='cursor:pointer;height:20px;width:20px' src='expand-256.png' onclick='toggleMaximize()'></h1>
<iframe style='border: none;width:100%; height:95%' src='http://clonecloud.#{$conf.domain}/view.cgi?default=#{$conf.events.current_lecture_file ? $conf.events.current_lecture_file : $conf.default_slide}'></iframe>
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

$conf.links.each{|l|
	h << "<li><a href='#{l[:href]}'>"
	unless l[:noicon]
		h << "<img alt='#{l[:name]}' src='#{l[:icon] ? l[:icon] : l[:href]+"/favicon.ico"}' height='8' />&nbsp;"
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

h.add_head_script("jquery-2.2.3.min.js")
h.add_head_script("jquery.gridster.min.js")

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

h << <<FOOTER
<div id=footer>
<div id="ft_cont">
	<div> <a href="https://www.mgm-sp.com/impressum/">Imprint</a> </div>
	<div> <a href="?ping">(c)</a> 2016 mgm security partners GmbH </div>
	<div><ul id="icons">
FOOTER
$conf.links.each{|l|
	unless l[:noicon]
		h << "<li><a href='#{l[:href]}' title='#{l[:name]}'>"
		if l[:icon]
			h << "<img alt='#{l[:name]}' src='#{l[:icon]}' />"
		else
			h << "<img alt='#{l[:name]}' src='#{l[:href]}/favicon.ico' height='8' />"
		end
		h << "</a></li>"
	end
}
h << <<FOOTER
	</ul></div>
	</div>
</div>
FOOTER

h.out($cgi)
