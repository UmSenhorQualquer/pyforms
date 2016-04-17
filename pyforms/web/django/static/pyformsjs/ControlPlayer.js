
function ControlPlayer(name, properties){
	ControlBase.call(this, name, properties);
};
ControlPlayer.prototype = Object.create(ControlBase.prototype);

////////////////////////////////////////////////////////////////////////////////

ControlPlayer.prototype.get_value = function(){ 
	this.properties.video_index = $( "#timeline"+this.control_id()).slider("value");
	return this.properties.value; 
};

////////////////////////////////////////////////////////////////////////////////

ControlPlayer.prototype.set_value = function(value){
	if(this.properties.base64content){
		$("#display"+this.control_id()).attr("src", "data:image/png;base64,"+this.properties.base64content);
		$( "#timeline"+this.control_id()).slider("option", "max", this.properties.endFrame);
	}
};

////////////////////////////////////////////////////////////////////////////////

ControlPlayer.prototype.init_control = function(){
	var html = "<div class='ControlPlayer' >";
	html += "<img style='width:100%;' class='image' src=' ' id='display"+this.control_id()+"' />";
	html += "<div class='slider' name='"+this.name+"' id='timeline"+this.control_id()+"' ></div>";
	html += "</div>";
	this.jquery_place().replaceWith(html);
	var self = this;
	$( "#timeline"+this.control_id() ).slider({
		stop: function(){ self.basewidget.fire_event( self.name, 'refresh' ); } ,
		max: self.properties.endFrame
	});
};

////////////////////////////////////////////////////////////////////////////////
