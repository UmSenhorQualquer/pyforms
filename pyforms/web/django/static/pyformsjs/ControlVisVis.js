

function ControlVisVis(name, properties){
	ControlBase.call(this, name, properties);
};
ControlVisVis.prototype = Object.create(ControlBase.prototype);

////////////////////////////////////////////////////////////////////////////////

ControlVisVis.prototype.get_value = function(){ 
	return this.jquery().data('chart_data');
};

////////////////////////////////////////////////////////////////////////////////

ControlVisVis.prototype.set_value = function(value){
	var chart = this.jquery().data('chart');
	this.jquery().data('chart_data', value);

	var options = {
		data:value.data,
		legend: {
			show: value.legend.length>0,
			labels: value.legend,
			showLabels: true,
			showSwatch: true
		}
	};
	chart.replot(options);
};

////////////////////////////////////////////////////////////////////////////////