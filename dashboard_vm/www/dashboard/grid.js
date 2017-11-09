var gridster;
$(function(){ //DOM Ready
	gridster = $("div.gridster").gridster({
			widget_base_dimensions: [170, 100],
			widget_margins: [12, 12],
			widget_selector: "div.widget",
			draggable: {
				handle: 'h1',
				start: function(){
					gridster.empty_cells_player_occupies ();
				},
				stop: function () {
					$(".gridnav").show();
				}
			},
			shift_widgets_up: false,
			shift_larger_widgets_down: true,
			collision: {
				wait_for_mouseup: true
			},
			resize: {
				enabled: true,
				stop: function(){
					adjust_calendar();
					$(".gridnav").show();
				},
				resize: adjust_calendar
			}
	}).data('gridster').enable();
	grid_layout_from_server(true);
});

function adjust_calendar(){
	$('#calendar').fullCalendar('option','height',$('#calendarwidget').height()-53);
}

function grid_layout_from_server(load_layout_from_localstorage){
	$.ajax({
		url: "/grid_layout.cgi",
		type: "get",
		success: function(gridlayout){
			set_grid_layout(gridlayout);
			if (load_layout_from_localstorage) {
				grid_layout_from_localstorage();
			}
			$(".gridnav").hide();
		}
	});
}

function get_current_grid_layout(){
	var layout = {};
	$(".widget").each(function(i,u){

		layout[u.id] = {
			"col" : $(u).attr("data-col"),
			"row" : $(u).attr("data-row"),
			"sizex" : $(u).attr("data-sizex"),
			"sizey" : $(u).attr("data-sizey"),
		};
	});
	return(layout);
}

function save_grid_layout_to_localstorage(){
	window.localStorage.setItem('gridster-'+document.location.pathname,JSON.stringify(get_current_grid_layout()));
	$(".gridnav").hide();
}

function revert_grid_layout_to_server(){
	window.localStorage.removeItem('gridster-'+document.location.pathname);
	$(".gridnav").hide();
	grid_layout_from_server(true);
}

function grid_layout_from_localstorage(){
	gridlayout = JSON.parse(window.localStorage.getItem('gridster-'+document.location.pathname));
	if (gridlayout) {
		set_grid_layout(gridlayout);
	}
	$(".gridnav").hide();
}

function set_grid_layout(gridlayout){
	$(".widget").each(function(i,u){
		layout = gridlayout[u.id];
		if (layout){
			gridster.move_widget($("#"+u.id), parseInt(layout["col"]), parseInt(layout["row"]));
			gridster.resize_widget($("#"+u.id), parseInt(layout["sizex"]), parseInt(layout["sizey"]));
		}
	});
	window.setTimeout(adjust_calendar,500);
}
