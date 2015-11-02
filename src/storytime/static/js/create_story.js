$(document).ready(function() {
	var position = 1;
	$("#addimage").click(function(event){
		var string = "onchange = \"$('#preview" + position + "')[0].src = window.URL.createObjectURL(this.files[0])\"";
		$("<div class = \"col-lg-3\"> <img id=\"preview" + position + "\" alt=\"your image\" width=\"100\" height=\"100\" /> <label for=\"id_source\">Image:</label><input id=\"id_source\" name=\"source\" type=\"file\" " + string +  " ><input id=\"id_position\" name=\"position\" type=\"hidden\" value = " + position + "></div>").insertBefore("#choice");
		position++;
	});
	
	$("#addtext").click(function(event){
		$( "<div class = \"col-lg-3\" > <label for=\"id_text\">Text:</label><textarea class=\"form-control\" rows=\"10\" id=\"id_text\" maxlength=\"200\" name=\"text\" type=\"text\"></textarea><input id=\"id_text_position\" name=\"text_position\" type=\"hidden\" value = " + position +"> </div>" ).insertBefore("#choice");
		position++;
	});
});