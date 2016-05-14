
function ControlPlayer(name, properties){
	ControlBase.call(this, name, properties);
};
ControlPlayer.prototype = Object.create(ControlBase.prototype);

////////////////////////////////////////////////////////////////////////////////

ControlPlayer.prototype.get_value = function(){ 
	this.properties.video_index = $( "#timeline"+this.control_id()).val();
	return this.properties.value; 
};

////////////////////////////////////////////////////////////////////////////////

ControlPlayer.prototype.set_value = function(value){
	if(this.properties.base64content){
		$("#display"+this.control_id()).attr("src", "data:image/png;base64,"+this.properties.base64content);

		var width = $( "#display"+this.control_id()).width();
		$( "#card"+this.control_id()).css('width', width+"px");

		$( "#timeline"+this.control_id()).val(this.properties.video_index);
		$( "#timeline"+this.control_id()).attr("min", 0);
		$( "#timeline"+this.control_id()).attr("max", this.properties.endFrame);
	}
};

////////////////////////////////////////////////////////////////////////////////

ControlPlayer.prototype.init_control = function(){

	var html = "<div class='field ControlPlayer' >";
	html += "<div class='ui card' id='card"+this.control_id()+"' >";
	html += "<div class='image'>";
	html += "<img style='width:100%;' class='image' src='' id='display"+this.control_id()+"' />";
	html += "</div>";
	html += "<div class='content'>";
	html += "<input style='width:100%;' type='range' name='"+this.name+"' value='"+this.properties.value+"' id='timeline"+this.control_id()+"' max='"+this.properties.endFrame+"'>";
	html += "</div>";
	html += "</div>";
	html += "</div>";

	this.jquery_place().replaceWith(html);

	
	var self = this;
	$( "#timeline"+this.control_id() ).change(
		function(){ self.basewidget.fire_event( self.name, 'refresh' ); }
	);
};

////////////////////////////////////////////////////////////////////////////////
