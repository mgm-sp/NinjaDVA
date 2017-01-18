function chooseMaterial(slide){
	$("#slides iframe")[0].contentWindow.postMessage(slide,"*")
}
function toggleMaximize(){
	var e = "expand-256.png";
	var c = "collapse-256.png";
	var i = $("#fslink");
	i.attr("src", i.attr("src") === e ? c : e);
	$("#slides").toggleClass("fullscreen");
}
