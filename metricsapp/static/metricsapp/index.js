$(document).ready(function() {
	/*
	 + Helpers
	  */

	//Turn a string in the form "['foo', 'bar']"
	//into a JS array of strings
	function toStrArray(str){
		str = str.replace("['",'');
		str = str.replace("']",'');
		return str.split("', '")
	}

	/*
	 * Draw charts
	 */

	/* Radar chart */
	$radar_canvas = $("#radar");
	var radar_data = {
		labels: toStrArray($radar_canvas.data('labels')),
		datasets: [
			{
				fillColor: "rgba(151,151,151,0.2)",
				strokeColor: $radar_canvas.data('color'),
				pointColor: $radar_canvas.data('color'),
				pointStrokeColor: "#fff",
				pointHighlightFill: "#fff",
				pointHighlightStroke: "rgba(151,187,205,1)",
				data: $radar_canvas.data('scores')
			}
		]
	};
	var radar_options = {
		maintainAspectRatio: false,
		responsive: true,
	}
	try {
		var radar_ctx = $radar_canvas.get(0).getContext("2d");
		new Chart(radar_ctx).Radar(radar_data, radar_options);
	}
	catch (e) {
		console.error('Failed to draw chart.', e);
	}


	/* Overall line chart */
	$overall_canvas = $("#overall");
	//These are also used by the individual metric charts
	var sprint_labels = toStrArray($overall_canvas.data('labels'))
	var overall_data = {
		labels: sprint_labels,
		datasets: [
			{
				fillColor: "rgba(151,151,151,0.2)",
				strokeColor: $overall_canvas.data('color'),
				pointColor: $overall_canvas.data('color'),
				pointStrokeColor: "#fff",
				pointHighlightFill: "#fff",
				pointHighlightStroke: "rgba(151,187,205,1)",
				data: $overall_canvas.data('scores')
			}
		]
	};
	var overall_options = {
		datasetStrokeWidth : 4,
		maintainAspectRatio: false,
		responsive: true,
		bezierCurveTension : 0.2
	}
	var overall_ctx = $overall_canvas.get(0).getContext("2d");
	new Chart(overall_ctx).Line(overall_data, overall_options);

	/* Individual metrics line charts */
	//Show the chart when a panel is fully opened
	//shown.bs.collapse waits for CSS transitions to complete
	$('.collapse').on('shown.bs.collapse', function () {
		var $canvas = $(this).find('.metric-chart');
		var chart_data = {
			labels: sprint_labels,
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
	function deactivate(metric_id, $panel) {
		//Callback on successfull POST
		function remove_panel($panel) {
			//the panel we're referencing in the hash is being removed
			history.pushState(null, null, '#')
			animation_time = 800;
			$panel.slideUp(animation_time);
			name = $panel.find('.metric-name').text();
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
		//AJAJ call
		$.ajax({
			type: "POST",
			url: '/deactivate',
			data: {metric_id: metric_id},
			success: function(){
				remove_panel($panel);
			},
			dataType: 'json'
		});
	}

	$('#deactive-metric-modal').on('show.bs.modal', function (event) {
		var $button = $(event.relatedTarget); // Button that triggered the modal
		var metric_id = $button.data('metric-id');
		var metric_name = $button.data('metric-name');
		var $modal = $(this);
		$modal.find('#modal-metric-name').text(metric_name);
		$panel = $button.closest('div.panel-default');
		$modal.find('#deactivate-btn').one('click', function(e){
			$modal.modal('hide');
			deactivate(metric_id, $panel);
		});
	});

});