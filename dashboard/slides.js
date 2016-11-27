function chooseMaterial(slide){
	$("#slides iframe")[0].contentWindow.postMessage(slide,"*")
}
