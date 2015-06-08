$(document).ready(function() {
	/*
	 * Draw charts
	 */

	/* Radar chart */
	try {
		var radar_ctx = $("#radar").get(0).getContext("2d");
		// radar_data is filled in the template
		var myRadarChart = new Chart(radar_ctx).Radar(radar_data);
	}
	catch (e) {
		console.error('Failed to draw radar chart.');
		console.error(e);
	}


	/* Line chart */
	var line_options = {
		bezierCurve : true,
		datasetFill : true,
		datasetStrokeWidth : 4,
		maintainAspectRatio: false,
		responsive: true
	}
	var line_ctx = $("#overall").get(0).getContext("2d");
	//line_options is filled in the template
	var myLineChart = new Chart(line_ctx).Line(line_data, line_options);

	/*
	 * Metrics
	 */
	//open the metric selected in the hash and scroll to it
	var hash = window.location.hash;
	if (hash) {
		$(hash).addClass('in');
		$(hash)[0].scrollIntoView(true);
	}
	//update hash if metric is opened
	$('.collapse').on('show.bs.collapse', function () {
		history.pushState(null, null, '#' + $(this).attr('id'));
	});
});