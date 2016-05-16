

function ControlBase(name, properties){
	var self = this;

	this.name 			= name;
	this.properties 	= properties;
	this.basewidget 	= undefined; //Will be set in runtime by the parent BaseWidget object.
};

////////////////////////////////////////////////////////////////////////////////

ControlBase.prototype.control_id = function(){ 
	return this.basewidget.control_id(this.name); 
};

////////////////////////////////////////////////////////////////////////////////

ControlBase.prototype.jquery = function(){ 
	return $("#"+this.control_id()); 
};

////////////////////////////////////////////////////////////////////////////////

ControlBase.prototype.place_id = function(){ 
	return "place-"+this.control_id(); 
};

////////////////////////////////////////////////////////////////////////////////

ControlBase.prototype.jquery_place = function(){ 
	return $( "#"+this.place_id() ); 
};

////////////////////////////////////////////////////////////////////////////////

ControlBase.prototype.get_value = function(){ 
	return this.jquery().val(); 
};

////////////////////////////////////////////////////////////////////////////////

ControlBase.prototype.set_value = function(value){
	this.jquery().val(value); 
};

////////////////////////////////////////////////////////////////////////////////

ControlBase.prototype.deserialize = function(data){
	$.extend(this.properties, data);
	this.set_value(this.properties.value);
	if(this.properties.visible) 
		this.jquery_place().show();
	else 
		this.jquery_place().hide();
};

////////////////////////////////////////////////////////////////////////////////

ControlBase.prototype.serialize = function(){
	this.properties.value = this.get_value();
	return this.properties; 
};

////////////////////////////////////////////////////////////////////////////////

ControlBase.prototype.init_control = function(){
	if(this.properties.visible) 
		this.jquery_place().show();
	else 
		this.jquery_place().hide();
};