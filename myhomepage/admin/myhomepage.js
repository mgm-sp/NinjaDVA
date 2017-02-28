#!/usr/bin/env phantomjs
"use strict";

setTimeout(function(){

var args = require('system').args;
var domainname = args[1].toLowerCase();
var user = args[2];
var pass = args[3];
var attackerurl = args[4];

phantom.injectJs('md5.js');
var mail_sid = md5("mail" + attackerurl + pass);
var cloud_sid = md5("cloud" + attackerurl + pass);

var page = require('webpage').create();
page.settings.resourceTimeout = 1000;

page.open('http://mail.'+domainname+'/login.cgi?_session_id='+mail_sid, function(status) {

	page.open('http://mail.'+domainname+'/login.cgi', 'POST', 'username='+user+'&password='+pass, function(status) {

		page.open('http://clonecloud.'+domainname+'/login.cgi?_session_id='+cloud_sid, function(status) {

			page.open('http://clonecloud.'+domainname+'/login.cgi', 'POST', 'username='+user+'&password='+pass, function(status) {

				page.open('http://myhomepage.'+domainname+'/'+attackerurl, function (status) {
					if (status !== 'success') {
						console.log('Unable to access network');
					}
					setTimeout(function(){
						phantom.exit()
					}, 5000); // 5 Sekunden warten -> Studenten executen JavaScript was manchmal noch etwas Zeit zur Ausführung braucht!
					});
				});
			});
	});
});

}, 5000);
