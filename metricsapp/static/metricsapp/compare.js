$(document).ready(function() {
	/* Team comparison line chart */
	$compare_canvas = $("#compare");
	var compare_options = {
		datasetStrokeWidth : 4,
		maintainAspectRatio: false,
		responsive: true,
		bezierCurveTension : 0.2
	}
	try {
		var compare_ctx = $compare_canvas.get(0).getContext("2d");
		//compare_data is filled in the template
		new Chart(compare_ctx).Line(compare_data, compare_options);
	}
	catch (e) {
		console.error('Failed to draw chart.', e);
	}
});