



function ControlPlayer(name, properties){
	ControlBase.call(this, name, properties);
};
ControlPlayer.prototype = Object.create(ControlBase.prototype);

////////////////////////////////////////////////////////////////////////////////

ControlPlayer.prototype.get_value = function(){ 
	var pos = $( "#timeline"+this.control_id() ).slider("value");
	var res = { position: pos, filename: this.properties.filename };
	return res;
};

////////////////////////////////////////////////////////////////////////////////

ControlPlayer.prototype.set_value = function(value){
	$( "#timeline"+this.control_id() ).slider({min: value.min, max: value.max, value: value.position});
	this.properties.filename = value.filename;
	$( "#display"+this.control_id() ).attr("src", "data:image/png;base64,"+value.frame);
};

////////////////////////////////////////////////////////////////////////////////

ControlPlayer.prototype.init_control = function(){
	var html = "<div class='ControlPlayer' >";
	html += "<img style='width:100%;' class='image' src=' ' id='display"+this.control_id()+"' />";
	html += "<div class='slider' name='"+this.name+"' id='timeline"+this.control_id()+"' ></div>";
	html += "</div>";
	this.jquery_place().replaceWith(html);
	$( "#timeline"+this.control_id() ).slider( {stop: this.basewidget.update_controls() });
};

////////////////////////////////////////////////////////////////////////////////
