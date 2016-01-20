#!/usr/bin/env phantomjs
"use strict";

var args = require('system').args;
var servername = args[1].toLowerCase();
var user = args[2];
var pass = args[3];
var id = args[4];
var time = args[5];

var page = require('webpage').create();
page.settings.resourceTimeout = 1000;


page.open('http://'+servername+'/login.cgi', function(status) {
	console.log(JSON.stringify(phantom.cookies));

	page.open('http://'+servername+'/login.cgi', 'POST', 'username='+user+'&password='+pass, function(status) {

		page.open('http://'+servername+'/admin/chat.cgi?support_id='+id+'&question_time='+time, function (status) {
			if (status !== 'success') {
				console.log('Unable to access network');
			}
			phantom.exit();
		});
	});
});
