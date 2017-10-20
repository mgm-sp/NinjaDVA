function save_grid_layout(){
	$(".user").each(function(i,u){
		window.localStorage.setItem('gridster-'+u.id, JSON.stringify({
			"col" : $(u).attr("data-col"),
			"row" : $(u).attr("data-row")
		}));
	});
}

function load_grid_layout(){
	$(".user").each(function(i,u){
		layout = JSON.parse(window.localStorage.getItem('gridster-'+u.id));
		if (layout){
			$("#"+u.id).attr("data-col",layout["col"]);
			$("#"+u.id).attr("data-row",layout["row"]);
		}
	});
}

function pad(s){
	var pad = "00";
	return pad.substring(0, pad.length - s.length) + s;
}
function human_readable_time_ago(time){
	var diff = new Date(Date.now() - Date.parse(time));

	if (diff.getMonth() != 0)
		return "long ago";
	else if (diff.getUTCDate() != 1)
		return diff.getUTCDate() == 2 ? "one day ago" : diff.getDate().toString() + " days ago";
	else if (diff.getUTCHours() != 0)
		return diff.getUTCHours().toString() + " hours ago";
	else
		return pad(diff.getMinutes().toString()) + ":" + pad(diff.getSeconds().toString()) + " ago";
}

function select_task(sel){
	$("input[type=button]").removeClass("active");
	sel.classList.add("active");

	window.localStorage.setItem('last-task',sel.value);
	for (ip in data){
		var id = $("#ip_"+ip.split(".")[3])[0];

		if (data[ip][sel.value]){
			var red=100-data[ip][sel.value]['state']*10-5;
			var green=100-data[ip][sel.value]['state']*10+5;
			id.style.backgroundImage="linear-gradient(to right,rgba(255,80,80,0.5) "+red+"%,rgba(34,139,34,0.5) "+green+"%)";
			var text = $("<span />",{
				title: data[ip][sel.value]['time']
			}).text(human_readable_time_ago(data[ip][sel.value]['time']));
			text.append($("<br />"));
			if (data[ip][sel.value]['comment']) {
				text.append($("<span />").text(data[ip][sel.value]['comment']));
			}
			$(id.lastElementChild).html(text);
		} else {
			id.style.backgroundImage="linear-gradient(to right,rgba(255,80,80,0.5) 95%,rgba(34,139,34,0.6) 105%)";
			id.lastElementChild.innerHTML="";
		}
	}

	if(tasks[sel.value]) {
		var solutionlist = $("<div />");
		solutionlist.append($("<h1 />").text(tasks[sel.value]["title"]));
		$(tasks[sel.value]["description"].split("\n\n")).each(function(i,s){
			solutionlist.append($("<p />").html(s.replace(/(https?:\/\/[a-zA-Z0-9\.-]*)/g,"<a href='$1'>$1</a>")));
		});
		$(tasks[sel.value]["solutions"]).each(function(i,s){
			var codearea = $("<textarea />",{ class: 'code' });
			codearea.text(s);
			solutionlist.append(codearea);
			var editor = CodeMirror.fromTextArea(codearea[0], {
				mode:  {
					name: sel.value.match(/sql/) ? "sql" : "htmlmixed",
				},
				readOnly: true,
			});
			setTimeout(function() {
				editor.refresh();
			},1);

		});
		$("#solution").html(solutionlist);
	} else
		$("#solution").text("");
}
var tasks;
$(document).ready(function(){
	$.ajax({
		url: "tasks.cgi",
		success: function(result) {
			tasks = result;
			update_data();
		},
	});
});

var data;
var gridster;
function update_data() {
	$.ajax({
		url: "solves.cgi",
		success: function (d) {
			data = d;
			for (ip in data){
				var id = 'ip_'+ip.split(".")[3];
				if (!$("#"+id).length) {
					$(".gridster").append('<fieldset id="'+id+'" data-row="1" data-col="1" data-sizex="1" data-sizey="1" class="user"><legend>'+ip+'</legend><div></div></fieldset>');
				}
			}

			gridster = $("div.gridster").gridster({
				widget_base_dimensions: [200, 100],
				widget_margins: [40, 30],
				widget_selector: ".user",
				min_cols: 5,
				min_rows: 30,
				shift_widgets_up: false,
				shift_larger_widgets_down: false,
				collision: {
					wait_for_mouseup: true
				}
			}).data('gridster');

			load_grid_layout();
			if (window.localStorage.getItem("last-task")){
				$("#"+window.localStorage.getItem("last-task")).click();
			}
		}
	});
}

