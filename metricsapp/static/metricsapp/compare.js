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
		new Chart(compare_ctx).Line(line_data, compare_options);
	}
	catch (e) {
		console.error('Failed to draw chart.', e);
	}

	/* Team comparison radar chart */
	$radar_canvas = $("#compare-radar");
	var radar_options = {
		maintainAspectRatio: false,
		responsive: true,
		scaleBeginAtZero : false,
		angleLineWidth : 2,
		angleLineColor : "rgba(0,0,0,.2)",
	}
	try {
		var radar_ctx = $radar_canvas.get(0).getContext("2d");
		//radar_data is filled in the template
		new Chart(radar_ctx).Radar(radar_data, radar_options);
	}
	catch (e) {
		console.error('Failed to draw chart.', e);
	}

	/* Bootstrap multiselect */
	// http://davidstutz.github.io/bootstrap-multiselect/
	$('#team-select').multiselect({
		buttonWidth: '100%',
		nonSelectedText: 'No teams selected',
		nSelectedText: ' teams selected',
		allSelectedText: 'All teams selected',
		selectAllText: 'Select all teams',
		includeSelectAllOption: true,
		numberDisplayed: 10,
		enableFiltering: true,
		enableCaseInsensitiveFiltering: true
	});
});