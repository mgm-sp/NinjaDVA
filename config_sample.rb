# rename this file to "config.rb"

$conf.domain = ".inf.tu-dresden.de"
$conf.pepper = "Luiphoh3gooz9pai"
$conf.default_userpw = "shohseib9Phi6euL"

# Dashboard
# Weather widget
$conf.location = "Dresden, Germany"

# dashboard-relative path
$conf.current_slide = "slides/01_Introduction.pdf"

# time schedule
$conf.events = [
	{
		:title => "Web Application Security",
		:start => "2016-11-18",
		:end   => "2016-09-18"
	},
	{
		:title => "Session 1",
		:start => "2016-11-18T09:00:00",
		:end   => "2016-11-18T11:10:00",
		:url => 'javascript:chooseMaterial("01-basics-handout.pdf")'
	},
	{
		:title => "Bäcker",
		:start => "2016-11-18T11:15:00",
		:end   => "2016-11-18T11:30:00",
		:backgroundColor => "#008006"
	},
	{
		:title => "Session 2",
		:start => "2016-11-18T11:30:00",
		:end   => "2016-11-18T13:15:00",
		:url => 'javascript:chooseMaterial("02-security_management-handout.pdf")'
	},
	{
		:title => "Mittagessen",
		:start => "2016-11-18T13:15:00",
		:end   => "2016-11-18T14:00:00",
		:backgroundColor => "#008006"
	},
	{
		:title => "Session 3",
		:start => "2016-11-18T14:00:00",
		:end   => "2016-11-18T15:30:00",
		:url => 'javascript:chooseMaterial("03-Bedrohungen-handout.pdf")'
	},
	{
		:title => "Session 4",
		:start => "2016-11-18T15:45:00",
		:end   => "2016-11-18T17:15:00",
		:url => 'javascript:chooseMaterial("04-Maßnahmen-handout.pdf")'
	}
]
