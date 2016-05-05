

function ControlVisVis(name, properties){
	ControlBase.call(this, name, properties);
};
ControlVisVis.prototype = Object.create(ControlBase.prototype);

////////////////////////////////////////////////////////////////////////////////

ControlVisVis.prototype.init_control = function(){
	var html = 	"<div class='ControlVisVis' id='chart-container-"+this.control_id()+"' title='"+this.properties.help+"'   >";
	html += 	"<div id='"+this.control_id()+"' ></div>";
	html += 	"</div>";
	this.jquery_place().replaceWith(html);
	var self = this;
	var legend = self.properties.legend;
	var data   = self.properties.value;

	if(data.length==0){ data = [[[0,0]]] }
	var chart = $.jqplot(this.control_id(), data, {
		title:self.label,
		seriesDefaults:{
			showMarker:true, showLine:true, lineWidth:0.5,
			markerOptions:{ size: 6 }
		},
		legend: {
			show: legend.length>0,				
			labels: legend,
			placement: "outside",
			location: 'e'
		},
		axes:{
			xaxis:{
				renderer: 		$.jqplot.DateAxisRenderer, 
				labelRenderer: 	$.jqplot.CanvasAxisLabelRenderer,
				tickRenderer: 	$.jqplot.CanvasAxisTickRenderer,
				tickOptions: {angle: -45}
			}
		},
		cursor:{
			show: true, 
			zoom: true
		}
	});

	this.chart = chart;
};


////////////////////////////////////////////////////////////////////////////////

ControlVisVis.prototype.set_value = function(value){
	var self = this;
	var options = {
		data: value,
		legend: {
			show: self.properties.legend.length>0,
			labels: self.properties.legend,
			showLabels: true,
			showSwatch: true
		}
	};
	this.chart.replot(options);
};

////////////////////////////////////////////////////////////////////////////////

ControlVisVis.prototype.get_value = function(){ 
	return this.properties.value; 
};

////////////////////////////////////////////////////////////////////////////////

ControlVisVis.prototype.deserialize = function(data){
	this.properties = $.extend(this.properties, data);
	this.set_value(this.properties.value);
};

////////////////////////////////////////////////////////////////////////////////

ControlVisVis.prototype.serialize = function(){
	this.properties.value = this.get_value();
	return this.properties; 
};
