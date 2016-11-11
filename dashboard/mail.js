function updateMail(mail_ary){
	var mailtable = $("<table />");
	mailtable.append($("<tr />")
			.append($("<td />").text('From'))
			.append($("<td />").text('Subject'))
			);
	$(mail_ary).each(function(i,e){
		mailtable.append($("<tr />")
			.append($("<td />").text(e.sender))
			.append($("<td />").text(e.subject))
			);
		

	});
	if (mail_ary.length > 0) {
		$("#inbox").text("");
		console.log($("#inbox"));
		$("#inbox").append(mailtable);
	};
}

// Thanks to CORS, the old JSONP Interface
// api/mail.cgi?jsonp=updateMail is obsolete now
$(document).ready(function () {
	var domain = window.location.host.match(/^dashboard\.(.*)$/)[1];
	$.ajax({
		url: "http://mail."+domain+"/api/mail.cgi",
		xhrFields: {
			withCredentials: true
		},

		type: "get",
		success: updateMail,
		error: function (error){ console.log(error) }
	});
});


