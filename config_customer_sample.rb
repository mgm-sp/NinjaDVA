######################################################################
# example contents of config/somecustomer/config.rb
# put all files into config/somecustomer/files/
# (including a file for the location, e.g. "Innsbruck, Austria.jpg")
#
$conf.default_slide = "bad_code.pdf"
$conf.links << {
	:href => 'javascript:chooseMaterial("bad_code.pdf")',
	:name => "Bad Code",
	:noicon => true
}

# get this in the debug console with JSON.stringify(get_current_grid_layout())
# A4 Slides example
#$conf.dashboard_grid_layout = '{"timewidget":{"col":"1","row":"4","sizex":"1","sizey":"1"},"mailwidget":{"col":"1","row":"5","sizex":"3","sizey":"2"},"weatherwidget":{"col":"2","row":"4","sizex":"2","sizey":"1"},"calendarwidget":{"col":"1","row":"1","sizex":"2","sizey":"3"},"slides":{"col":"4","row":"1","sizex":"3","sizey":"6"},"linkwidget":{"col":"3","row":"1","sizex":"1","sizey":"3"}}'
# Presentation Slides example
#$conf.dashboard_grid_layout = '{"timewidget":{"col":"6","row":"1","sizex":"1","sizey":"1"},"mailwidget":{"col":"3","row":"1","sizex":"3","sizey":"1"},"weatherwidget":{"col":"1","row":"5","sizex":"1","sizey":"2"},"calendarwidget":{"col":"1","row":"1","sizex":"2","sizey":"4"},"slides":{"col":"3","row":"2","sizex":"4","sizey":"5"},"linkwidget":{"col":"2","row":"5","sizex":"1","sizey":"2"}}'

$conf.events = Seminar.new(
	title: "Web Application Security",
	location: "Dresden, Germany",
	start: "#{Date.today} 09:30"
)
.add_lecture(
		title: "Einführung und System",# Einführung und HTTP-Grundlagen
		file: "03-Ebene 1 - System.pdf",
		duration: 100

	)
.add_break(duration: 5)
.add_break(
	visible: true,
	title: "Bäcker",
	duration: 15
)
.add_lecture(
		title: "Grundlagen", # bis CSRF
		file: "02-Grundlagen.pdf",
		duration: 105
	)
.add_break(
	title: "Mittagessen",
	visible: true,
	duration: 45
)
.add_lecture(
	title: "Grundlagen und Implementierung", # ab Clickjacking bis CORS/Webmessaging
	file: "02-Grundlagen.pdf",
	duration: 90
)
.add_break(duration:15)
.add_lecture(
	title: "Grundlagen und Implementierung",# System + Cryptography
	file: "04-Ebene 3 - Implementierung.pdf",
	duration: 75
)
.new_day(start:"9:00")
.add_lecture(
	title: "Cryptography",
	file: "04-Ebene 3 - Implementierung.pdf",
	duration: 30
)
.add_break(duration:10)
.add_lecture(
	title: "Cross Site Scripting",# Cross Site Scripting #Injection?
	file: "04-Ebene 3 - Implementierung.pdf",
	duration: 90
)
.add_break(duration:5)
.add_break(
	visible: true,
	title: "Bäcker",
	duration: 15
)
.add_lecture(
	title: "Implementierung",#Session Fixation, URL Rewrite, Unvalidated Redirects and Forwards
	file: "04-Ebene 3 - Implementierung.pdf",
	duration: 105
)
.add_break(
	title: "Mittagessen",
	visible: true,
	duration: 45
)
.add_lecture(
	title: "Technologie und Logik",#Injection
	file: "05-Ebene 2 - Technologie.pdf",
	duration: 60
)
.add_break
.add_lecture(
	title: "Semantik, SDLC",
	file: "06-Ebene 4 - Logik.pdf",
	duration: 60
)
