$(document).ready(function() {
	/*
	 * Draw charts
	 */

	/* Radar chart */
	var radar_ctx = $("#radar").get(0).getContext("2d");
	// radar_data is filled in the template
	var myRadarChart = new Chart(radar_ctx).Radar(radar_data);

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
});