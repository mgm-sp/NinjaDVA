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
			resize: { enabled: true }
	}).data('gridster').enable();
	load_grid_layout();
});

function save_grid_layout(){
	$(".widget").each(function(i,u){
		window.localStorage.setItem('gridster-'+u.id, JSON.stringify({
			"col" : $(u).attr("data-col"),
			"row" : $(u).attr("data-row"),
			"sizex" : $(u).attr("data-sizex"),
			"sizey" : $(u).attr("data-sizey"),
		}));
	});
	$(".gridnav").hide();
}

function load_grid_layout(){
	$(".widget").each(function(i,u){
		layout = JSON.parse(window.localStorage.getItem('gridster-'+u.id));
		if (layout){
			gridster.move_widget($("#"+u.id), parseInt(layout["col"]), parseInt(layout["row"]));
			gridster.resize_widget($("#"+u.id), parseInt(layout["sizex"]), parseInt(layout["sizey"]));
		}
	});
	$(".gridnav").hide();
}
