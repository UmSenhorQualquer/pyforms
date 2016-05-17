(function($) {
  $.getStylesheet = function (href) {
    var $d = $.Deferred();
    var $link = $('<link/>', {
       rel: 'stylesheet',
       type: 'text/css',
       href: href
    }).appendTo('head');
    $d.resolve($link);
    return $d.promise();
  };

  
})(jQuery);


$.ajaxSetup({cache:true});
if(typeof(loading)!="function") var loading = function(){};
if(typeof(not_loading)!="function") var not_loading = function(){};



function PyformsManager(){
	
	this.applications = [];
	$.ajaxSetup({async: false, cache: true});

	$.getScript("/static/jquery.json-2.4.min.js");

	$.getScript("/static/pyformsjs/ControlBase.js");
	$.getScript("/static/pyformsjs/ControlText.js");
	$.getScript("/static/pyformsjs/ControlButton.js");
	$.getScript("/static/pyformsjs/ControlFile.js");
	$.getScript("/static/pyformsjs/ControlDir.js");
	$.getScript("/static/pyformsjs/ControlSlider.js");
	$.getScript("/static/pyformsjs/ControlCheckBox.js");
	$.getScript("/static/pyformsjs/ControlCombo.js");
	$.getScript("/static/pyformsjs/ControlDate.js");
	$.getScript("/static/pyformsjs/ControlImage.js");
	$.getScript("/static/pyformsjs/ControlList.js");
	$.getScript("/static/pyformsjs/ControlPlayer.js");
	$.getScript("/static/pyformsjs/ControlProgress.js");
	$.getScript("/static/pyformsjs/ControlBoundingSlider.js");
	$.getScript("/static/pyformsjs/ControlVisVis.js");
	$.getScript("/static/pyformsjs/ControlLabel.js");
	$.getScript("/static/pyformsjs/ControlTimeout.js");
	
	$.getScript("/static/pyformsjs/BaseWidget.js");


	$.getScript("/static/jqplot/jquery.jqplot.min.js");
	$.getScript("/static/jqplot/plugins/jqplot.cursor.js");
	$.getScript("/static/jqplot/plugins/jqplot.logAxisRenderer.min.js");
	$.getScript("/static/jqplot/plugins/jqplot.canvasTextRenderer.min.js");
	$.getScript("/static/jqplot/plugins/jqplot.canvasAxisLabelRenderer.min.js");
	$.getScript("/static/jqplot/plugins/jqplot.blockRenderer.min.js");
	$.getScript("/static/jqplot/plugins/jqplot.enhancedLegendRenderer.min.js");
	$.getScript("/static/jqplot/plugins/jqplot.logAxisRenderer.min.js");
	$.getScript("/static/jqplot/plugins/jqplot.dateAxisRenderer.min.js");
	$.getScript("/static/jqplot/plugins/jqplot.categoryAxisRenderer.min.js");
	$.getScript("/static/jqplot/plugins/jqplot.barRenderer.min.js");
	$.getScript("/static/jqplot/plugins/jqplot.pointLabels.min.js");
	$.getStylesheet("/static/jqplot/jquery.jqplot.min.css");


	$.ajaxSetup({async: true, cache: false});
}

////////////////////////////////////////////////////////////

PyformsManager.prototype.add_app = function(app){	
	this.applications.push(app);
};

////////////////////////////////////////////////////////////

PyformsManager.prototype.find_app = function(app_id){	
	for(var i=0; i<this.applications.length; i++){
		if( this.applications[i].widget_id==app_id ) return this.applications[i]
	}
	return undefined;
};

PyformsManager.prototype.find_control = function(control_id){	
	var ids 			= this.split_id(control_id);
	var widget_id 		= ids[0];
	var control_name 	= ids[1];

	var widget = this.find_app(widget_id);
	return widget.find_control(control_name);
};


PyformsManager.prototype.split_id = function(control_id){	
	var split_in 		= control_id.lastIndexOf("-");
	var widget_id 		= control_id.substring(0, split_in);
	var control_name 	= control_id.substring(split_in+1);

	return [widget_id, control_name];
};








////////////////////////////////////////////////////////////
if(pyforms==undefined) var pyforms = new PyformsManager()
////////////////////////////////////////////////////////////