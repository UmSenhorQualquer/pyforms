

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
	var html = 	"<div id='"+this.place_id()+"' class='field ControlSlider' title='"+this.properties.help+"' >";
	html += 	"<label>"+this.properties.label;
	html += 	" <div id='value"+this.control_id()+"' class='ui basic label'>"+this.properties.value+"</div>";
	html += 	"</label>";
	html += 	"<input style='width:100%;' type='range' name='"+this.name+"' value='"+this.properties.value+"' id='"+this.control_id()+"' min='"+this.properties.min+"' max='"+this.properties.max+"'>";
	html += 	"</div>";

	this.jquery_place().replaceWith(html);
	//this.jquery().on('input', function () {$(this).trigger('change');});
	var self = this;
	this.jquery().change(function(){ 
		$( "#value"+self.control_id() ).html( $(this).val() ); 
		self.basewidget.fire_event( self.name, 'changed' );
	});

	if(this.properties.visible) 
		this.jquery_place().show();
	else 
		this.jquery_place().hide();
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