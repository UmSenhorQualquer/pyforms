

function ControlSlider(name, properties){
	ControlBase.call(this, name, properties);
};
ControlSlider .prototype = Object.create(ControlBase.prototype);

////////////////////////////////////////////////////////////////////////////////

ControlSlider.prototype.get_value = function(){ 
	return this.jquery().val();
};

////////////////////////////////////////////////////////////////////////////////

ControlSlider.prototype.set_value = function(value){
	this.jquery().val(value);
	$( "#value"+this.name ).html( value );
};

////////////////////////////////////////////////////////////////////////////////

ControlSlider.prototype.init_control = function(){
	var html = 	"<div class='ui right labeled input ControlSlider' title='"+this.properties.help+"' >";
	html += 	"<div class='ui label'>"+this.properties.label+"</div>";
	html += 	"<input type='range' name='"+this.name+"' value='"+this.properties.value+"' id='"+this.control_id()+"' min='"+this.properties.min+"' max='"+this.properties.max+"'>";
	html += 	"<div id='value"+this.control_id()+"' class='ui basic label'>"+this.properties.value+"</div>";
	html += 	"</div>";

	this.jquery_place().replaceWith(html);
	var self = this;
	this.jquery().change(function(){ $( "#value"+self.control_id() ).html( $(this).val() ); });
};

////////////////////////////////////////////////////////////////////////////////

ControlSlider.prototype.deserialize = function(data){
	this.properties = $.extend(this.properties, data);
	this.set_value(this.properties.value);
};

////////////////////////////////////////////////////////////////////////////////

ControlSlider.prototype.serialize = function(){
	this.properties.value = this.get_value();
	return this.properties; 
};

////////////////////////////////////////////////////////////////////////////////