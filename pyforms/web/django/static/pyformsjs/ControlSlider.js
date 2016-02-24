

function ControlSlider(name, properties){
	ControlBase.call(this, name, properties);
};
ControlSlider .prototype = Object.create(ControlBase.prototype);

////////////////////////////////////////////////////////////////////////////////

ControlSlider.prototype.get_value = function(){ 
	return this.jquery().slider('value');
};

////////////////////////////////////////////////////////////////////////////////

ControlSlider.prototype.set_value = function(value){
	this.jquery().slider({value:value});
	$( "#value"+this.name ).html( value );
};

////////////////////////////////////////////////////////////////////////////////

ControlSlider.prototype.init_control = function(){
	var html = 	"<div class='ControlSlider' title='"+this.properties.help+"' >";
	html += 	"<label style='margin-right: 20px;' for='"+this.control_id()+"'>"+this.properties.label+": <small id='value"+this.control_id()+"' style='color:red' >"+this.properties.value+"</small></label>";
	html += 	"<div class='slider' name='"+this.name+"' id='"+this.control_id()+"' ></div>";
	html += 	"</div>";
	this.jquery_place().replaceWith(html);
	var self = this;
	this.jquery().slider({ 
		slide: function( event, ui ) { $( "#value"+self.control_id() ).html( ui.value ); },
		stop:  function(){ self.basewidget.fire_event( self.name, 'changed' )}, 
		min: this.properties.min, 
		max: this.properties.max,
		value: this.properties.value 
	});
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