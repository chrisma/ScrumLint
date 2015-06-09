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
	/* Allow referencing metrics in the hash */
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

	/* Deactivate metrics */
	function remove_panel($panel) {
		//the panel we're referencing in the hash is being removed
		history.pushState(null, null, '#')
		animation_time = 800;
		$panel.slideUp(animation_time);
		var message = "'" + name + "'<br> deactivated";
		var notify = function(){
			//https://github.com/ifightcrime/bootstrap-growl/
			$.bootstrapGrowl(message, {
				type: 'success',
				width: 300,
				delay: 3000,
			});
		};
		//Show notification shortly before the animation ends
		setTimeout(notify, animation_time-200);
	}

	$('a.deactivate').click(function(event){
		// stops the href="#" from jumping to the top of the page
		event.preventDefault();
		$panel = $(this).closest('div.panel-default');
		name = $panel.find('.metric-name').text();
		var sure = confirm("This will deactivate the metric \n'" +
			name + "'. \n" +
			"It can be reactivated in the administrative view.\n" +
			"Are you sure?");
		if (!sure) {return}
		var metric_id = $(this).data('metric-id');
		$.ajax({
			type: "POST",
			url: '/deactivate',
			data: {metric_id: metric_id},
			success: function(){
				remove_panel($panel);
			},
			dataType: 'json'
		});
	});

});