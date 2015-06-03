$(document).ready(function() {
	new PrettyJSON.view.Node({
		el:$('.field-formatted_results>div'),
		data:JSON.parse($('.field-formatted_results>div').text())
	});
});