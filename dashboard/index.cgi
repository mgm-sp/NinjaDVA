#!/usr/bin/ruby

require_relative "html"
require_relative "../config_defaults"
require "csv"
require "cgi"
require 'cgi/session'
$cgi = CGI.new
$session = CGI::Session.new($cgi)

h = HTML.new("Dashboard")

if $cgi.include?("ping")
	require_relative "../solved"
	if $cgi["ping"] == ""
		Solution.new("ping",1,"Pinged")
	else
		Solution.new("ping",10,"Pinged with message #{$cgi['ping']}")
	end
	h.header["status"] = "REDIRECT"
	h.header["Cache-Control"] = "no-cache"
	h.header["Location"] = "/"
	h << "Pong"
	h.out($cgi)
end

h.add_css("dashboard.css")

h << <<HEAD
<div id="top">
<div id="tabs">
<img src='mgm-sp-logo.png' alt='mgm security partners' id="logo" />
<div id="welcome">&nbsp;</div>
<ul>
<li class="nonactive_tab"><a href="?ping">Dashboard</a></li>
</ul>
</div></div>

<div id='content'>
<div class='gridster'>
HEAD


timewidget = <<CONTENT
<div class='widget' data-row="4" data-col="1" data-sizex="1" data-sizey="1">
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
<div class='widget' data-row="5" data-col="1" data-sizex="3" data-sizey="2">
<div>
<h1>New Mail</h1>
<div id='inbox'>Fetching new mail...</div>
</div>
</div>
MAILWIDGET
#h.add_script_file("http://mail#{$conf.domain}/api/mail.cgi?jsonp=updateMail")

h << "<!-- END MAIL WIDGET -->"

h << "\n"*3

h << <<WEATHERWIDGET
<!-- BEGIN WEATHER WIDGET -->
<div class='widget' data-row="4" data-col="2" data-sizex="2" data-sizey="1">
<div>
<h1>#{$conf.location}</h1>
WEATHERWIDGET
if File.exists?("#{$conf.location}.jpg")
	h << "<div id='weather_background' style=\"background-image: url('#{$conf.location}.jpg');\">"
end
h << "<div id='weather'></div>"
if File.exists?("#{$conf.location}.jpg")
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
<div class='widget' data-row="1" data-col="1" data-sizex="2" data-sizey="3">
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
			right: 'agendaWeek,agendaDay,listWeek'
		},
		height: 250,
		defaultView: 'agendaDay',
		navLinks: false, // can click day/week names to navigate views
		editable: false,
		eventLimit: true, // allow "more" link when too many events
		nowIndicator: true,
		scrollTime:  (new Date().getHours()-1) + ":00",
		slotDuration: '00:30:00',
		events: "events.cgi"
	});
});
JS

h << "<!-- END CALENDAR WIDGET -->"


if $conf.current_slide
h.add_script_file("slides.js")
h << <<SLIDES

<!-- BEGIN SLIDES WIDGET -->
<div id='slides' class='widget' data-row="1" data-col="4" data-sizex="3" data-sizey="6">
<div>
<h1 style='height:5%; margin:0; padding:0;display:flex;justify-content:space-between'>Lecture Material<img id='fslink' style='cursor:pointer;height:20px;width:20px' src='expand-256.png' onclick='toggleMaximize()'></h1>
<iframe style='border: none;width:100%; height:95%' src='http://clonecloud#{$conf.domain}/view.cgi'></iframe>
</div>
</div>
<!-- END SLIDES WIDGET -->
SLIDES
end


h << <<LINK

<!-- BEGIN LINK WIDGET -->
<div class='widget' data-row="1" data-col="3" data-sizex="1" data-sizey="3">
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

h.add_script <<GRID
$(function(){ //DOM Ready

        $("div.gridster").gridster({
            widget_base_dimensions: [170, 100],
            widget_margins: [12, 12],
						widget_selector: "div.widget",
            helper: 'clone',
            //resize: { enabled: true }
        }).data('gridster').disable();


});
GRID


h << <<FOOTER
<div id=footer>
<div id="ft_cont">
	<div> <a href="https://www.mgm-sp.com/impressum/">Imprint</a> </div>
	<div> (c) 2016 mgm security partners GmbH </div>
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
