var showAdminInterface = function () {
	grid_store_suffix = "admin";
	toggleAdminInterface = hideAdminInterface;
	$.ajax("/admin/widgets.cgi").success(function(html){
		$(".gridster").append(html);
		grid_layout_from_server(true);
	});
}
var hideAdminInterface = function () {
	grid_store_suffix = "user";
	toggleAdminInterface = showAdminInterface;
	gridster.remove_widget($(".adminwidget"));
	grid_layout_from_server(true);
}
var toggleAdminInterface = showAdminInterface;
