

function ControlLabel(name, properties){
	ControlBase.call(this, name, properties);
};
ControlLabel.prototype = Object.create(ControlBase.prototype);


////////////////////////////////////////////////////////////////////////////////

ControlLabel.prototype.init_control = function(){
	var html = '<div class="ui '+this.properties.css+' message" id="'+this.place_id()+'"  >';
	   html += '<div class="header">';
	   html += this.properties.label;
	   html += '</div>';
	   html += '<p id="'+this.control_id()+'" >';
	   html += this.properties.value;
	   html += '</p>';
	   html += '</div>';
	this.jquery_place().replaceWith(html);

	if(this.properties.visible) 
		this.jquery_place().show();
	else 
		this.jquery_place().hide();
};

////////////////////////////////////////////////////////////////////////////////

ControlLabel.prototype.set_value = function(value){
	this.init_control();
};

////////////////////////////////////////////////////////////////////////////////