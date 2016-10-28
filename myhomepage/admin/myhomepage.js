#!/usr/bin/env phantomjs
"use strict";

setTimeout(function(){

var args = require('system').args;
var domainname = args[1].toLowerCase();
var user = args[2];
var pass = args[3];
var attackerurl = args[4];

var page = require('webpage').create();
page.settings.resourceTimeout = 1000;

page.open('http://mail.'+domainname+'/login.cgi', function(status) {

	page.open('http://mail.'+domainname+'/login.cgi', 'POST', 'username='+user+'&password='+pass, function(status) {

		page.open('http://myhomepage.'+domainname+'/'+attackerurl, function (status) {
			if (status !== 'success') {
				console.log('Unable to access network');
			}
			setTimeout(function(){
				phantom.exit()
			}, 2000); // 2 Sekunden warten -> Studenten executen JavaScript was manchmal noch etwas Zeit zur Ausführung braucht!
		});
	});
});

}, 5000);
