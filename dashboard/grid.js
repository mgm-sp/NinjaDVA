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

function get_grid_layout(){
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

function save_grid_layout(){
	window.localStorage.setItem('gridster-'+document.location.pathname,JSON.stringify(get_grid_layout()));
	$(".gridnav").hide();
}

function load_grid_layout(){
	gridlayout = JSON.parse(window.localStorage.getItem('gridster-'+document.location.pathname));
	if (gridlayout) {
		$(".widget").each(function(i,u){
			layout = gridlayout[u.id];
			if (layout){
				gridster.move_widget($("#"+u.id), parseInt(layout["col"]), parseInt(layout["row"]));
				gridster.resize_widget($("#"+u.id), parseInt(layout["sizex"]), parseInt(layout["sizey"]));
			}
		});
	}
}
