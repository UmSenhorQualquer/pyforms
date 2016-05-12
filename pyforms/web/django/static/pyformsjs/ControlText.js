

function ControlText(name, properties){
	ControlBase.call(this, name, properties);
};
ControlText.prototype = Object.create(ControlBase.prototype);


////////////////////////////////////////////////////////////////////////////////

ControlText.prototype.init_control = function(){
	var html = "<div id='"+this.place_id()+"' class='ui labeled input ControlText' ><div class='ui label'>"+this.properties.label+"</div><input placeholder='"+this.properties.label+"' type='text' name='"+this.name+"' id='"+this.control_id()+"' value=\""+this.properties.value+"\" /></div>";
	this.jquery_place().replaceWith(html);

	var self = this;
	this.jquery().change(function(){
		self.basewidget.fire_event( this.name, 'changed' );
	});
};

////////////////////////////////////////////////////////////////////////////////
