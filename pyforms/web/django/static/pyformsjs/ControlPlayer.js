



function ControlPlayer(name, properties){
	ControlBase.call(this, name, properties);
};
ControlPlayer.prototype = Object.create(ControlBase.prototype);

////////////////////////////////////////////////////////////////////////////////

ControlPlayer.prototype.get_value = function(){ return ''; };

////////////////////////////////////////////////////////////////////////////////

ControlPlayer.prototype.set_value = function(value){};

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
