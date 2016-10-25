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

