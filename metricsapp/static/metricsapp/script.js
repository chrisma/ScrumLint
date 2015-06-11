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
		datasetStrokeWidth : 4,
		maintainAspectRatio: false,
		responsive: true,
		bezierCurveTension : 0.2
	}
	var line_ctx = $("#overall").get(0).getContext("2d");
	//line_options is filled in the template
	var myLineChart = new Chart(line_ctx).Line(line_data, line_options);

	//Show the chart when a panel is fully opened
	//shown.bs.collapse waits for CSS transitions to complete
	$('.collapse').on('shown.bs.collapse', function () {
		var $canvas = $(this).find('.metric-chart');
		var chart_data = {
			labels: line_data.labels,
			datasets: [
				{
					fillColor: "rgba(151,151,151,0.2)",
					strokeColor: $canvas.data('color'),
					pointColor: $canvas.data('color'),
					pointStrokeColor: "#fff",
					pointHighlightFill: "#fff",
					pointHighlightStroke: "rgba(151,187,205,1)",
					data: $canvas.data('scores')
				}
			]
		};
		var chart_options = {
			datasetStrokeWidth : 3,
			maintainAspectRatio: false,
			responsive: true,
			bezierCurveTension : 0.2
		}
		var ctx = $canvas.get(0).getContext("2d");
		var chart = new Chart(ctx).Line(chart_data, chart_options);
	});


	/*
	 * Metrics
	 */
	/* Allow referencing metrics in the hash */
	//open the metric selected in the hash and scroll to it
	var hash = window.location.hash;
	if (hash) {
		//.collapse('show') has a lengthy animation
		$(hash).addClass('in');
		$(hash)[0].scrollIntoView(true);
		$(hash).trigger('shown.bs.collapse');
	}
	//update hash if metric is opened
	//show.bs.collapse fires immediately when the element opens
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