function updateMail(mail_ary){
	var inbox = $("<div />");
	$(JSON.parse(mail_ary)).each(function(i,e){
		var mailtable = $("<table />");
		mailtable.append($("<tr />")
			.append($("<td />",{class : 'header'}).text("From:"))
			.append($("<td />").text(e.sender))
			);
		
		mailtable.append($("<tr />")
			.append($("<td />",{class : 'header'}).text("Subject:"))
			.append($("<td />").text(e.subject))
			);

		mailtable.append($("<tr />")
			.append($("<td />",{ colspan : 2 }).append($("<plaintext />").text(e.body)))
			);
		mailtable.append($("<tr />",{border:1}));
		inbox.append(mailtable);
		inbox.append($("<br />"));
	});
	if (JSON.parse(mail_ary).length > 0) {
		$("#inbox").text("");
		$("#inbox").append(inbox);
	};
}

$(document).ready(function () {
	$.ajax({
		url: "mail.cgi",
		type: "get",
		success: updateMail,
		error: function (error){ console.log(error) }
	});
});
