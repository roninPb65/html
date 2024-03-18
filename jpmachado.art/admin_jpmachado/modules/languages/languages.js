//Parsleyjs
$(document).ready(function() {
	$("#language-selector-input").change(function() {
	  var language = $("#language-selector-input option:selected").val();
	  window.location.href = language;
	});
});
//Parsleyjs