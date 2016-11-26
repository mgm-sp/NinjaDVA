function updateMail(mail_ary){
	var mailtable = $("<table />");
	mailtable.append($("<tr />")
			.append($("<th />").text('From'))
			.append($("<th />").text('Subject'))
			);
	$(mail_ary).each(function(i,e){
		mailtable.append($("<tr />")
			.append($("<td />").text(e.sender))
			.append($("<td />").text(e.subject))
			);
		

	});
	if (mail_ary.length > 0) {
		$("#inbox").text("");
		$("#inbox").append(mailtable);
	} else {
		$("#inbox").text("No new mail...");
	};
}

// Thanks to CORS, the old JSONP Interface
// api/mail.cgi?jsonp=<mycallbackfunction> is obsolete now
$(document).ready(function () {
	var mailhost, host;
	domain = window.location.host.match(/^[^\.]*(\..*)$/);
	if (domain) {
		domain = domain[1];
	} else {
		domain = "";
	}
	mailhost = "http://mail" + domain
	$.ajax({
		url: mailhost+"/api/mail.cgi",
		xhrFields: {
			withCredentials: true
		},

		type: "get",
		success: updateMail,
		error: function (error){
			if (error.status === 401) {
				$("#inbox").text("You need to sign in to your mail account first!");
				var logintable = $("<table />");
				logintable.append($("<tr />")
						.append($("<td />",{
							"class" : "description"
						}).text('Username:'))
						.append($("<td />",{
								"class" : "content"
							}).append($("<input />",{
							"type":"text",
							"name":"username"
						}))
						)
					);
				logintable.append($("<tr />")
						.append($("<td />",{
							"class" : "description"
						}).text('Password:'))
						.append($("<td />",{
							"class" : "content"
						}).append($("<input />",{
							"type":"password",
							"name":"password"
						}))
						)
					);
				logintable.append($("<tr />")
						.append($("<td />",{
							"class" : "description"
						}))
						.append($("<td />",{
							"class" : "content"
						}).append($("<input />",{"type":"submit"}))
						)
					);
				$("#inbox").append($("<form />",{
					"method" : "POST",
					"action" : mailhost
				}).append(logintable).append(
						$("<input />",{
							"type":"hidden",
							"name":"return_url",
							"value": "http://dashboard" + domain
						})
					));
			} else {
				console.log(error);
			}
		}
	});
});


