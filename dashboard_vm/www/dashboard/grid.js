var gridster;
$(function () {
    //DOM Ready
    gridster = $("div.gridster")
        .gridster({
            widget_base_dimensions: [170, 100],
            widget_margins: [12, 12],
            widget_selector: "div.widget",
            avoid_overlapped_widgets: true,
            draggable: {
                handle: "h1",
                start: function () {
                    gridster.empty_cells_player_occupies();
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
                stop: function (e, ui, $widget) {
                    adjust_calendar();
                    $(".gridnav").show();
                    $widget.resize();
                },
                resize: adjust_calendar
            }
        })
        .data("gridster")
        .enable();
    grid_layout_from_server(true);
});

function adjust_calendar() {
    $("#calendar").fullCalendar("option", "height", $("#calendarwidget").height() - 53);
}

function grid_layout_from_server(load_layout_from_localstorage) {
    $.ajax({
        url: "/grid_layout.cgi",
        type: "get",
        success: function (gridlayout) {
            //set user grid layout
            if (grid_store_suffix === "user") {
              set_grid_layout(gridlayout.user);
            } else {
              set_grid_layout(gridlayout.admin);
            }
            if (load_layout_from_localstorage) {
                grid_layout_from_localstorage();
            }
            $(".gridnav").hide();
        }
    });
}

function get_current_grid_layout() {
    var layout = {};
    $(".widget").each(function (i, u) {
        layout[u.id] = {
            col: $(u).attr("data-col"),
            row: $(u).attr("data-row"),
            sizex: $(u).attr("data-sizex"),
            sizey: $(u).attr("data-sizey")
        };
    });
    return layout;
}

// this global variable should be in sync with the current state
// if user or admin view is shown
var grid_store_suffix = "user";

function save_grid_layout_to_localstorage(sLocation = null, sGrindStoreSuffix = null, sCustomDesign = null) {
    window.localStorage.setItem(
        "gridster-" +
        (sLocation ? sLocation : document.location.pathname) +
        (sGrindStoreSuffix ? sGrindStoreSuffix : grid_store_suffix),
        JSON.stringify(sCustomDesign ? sCustomDesign : get_current_grid_layout())
    );
    $(".gridnav").hide();
}

function revert_grid_layout_to_server() {
    window.localStorage.removeItem("gridster-" + document.location.pathname);
    $(".gridnav").hide();
    grid_layout_from_server(true);
}

function grid_layout_from_localstorage() {
    gridlayout = JSON.parse(window.localStorage.getItem("gridster-" + document.location.pathname + grid_store_suffix));
    if (gridlayout) {
        set_grid_layout(gridlayout);
    }
    $(".gridnav").hide();
}

function set_grid_layout(gridlayout) {
    $(".widget").each(function (i, u) {
        layout = gridlayout[u.id];
        if (layout) {
            gridster.move_widget($("#" + u.id), parseInt(layout["col"]), parseInt(layout["row"]));
            gridster.resize_widget($("#" + u.id), parseInt(layout["sizex"]), parseInt(layout["sizey"]));
        }
    });
    window.setTimeout(adjust_calendar, 500);
}

// zoom button for all widgets
$(function () {
    //DOM Ready
    var zoomButton =
        "<img class='zoomButton' style='cursor:pointer;height:2ex;width:2ex' src='expand-256.png' onclick='toggleMaximize()'>";
    $("div.widget h1").append(zoomButton);
});

function toggleMaximize() {
    var e = "expand-256.png";
    var c = "collapse-256.png";
    var i = $(".zoomButton");
    i.attr("src", i.attr("src") === e ? c : e);
    //call resize to trigger all resize handlers
    var toggledWidget = $("div.widget:hover");
    toggledWidget.toggleClass("fullscreen").one('transitionend webkitTransitionEnd oTransitionEnd otransitionend MSTransitionEnd', function () {
        toggledWidget.resize();
    });
}
