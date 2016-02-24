

function ControlText(name, properties){
	ControlBase.call(this, name, properties);
};
ControlText.prototype = Object.create(ControlBase.prototype);


////////////////////////////////////////////////////////////////////////////////

ControlText.prototype.init_control = function(){
	var html = "<div title='"+this.properties.help+"' id='"+this.place_id()+"' class='ControlText' ><label for='"+this.control_id()+"'>"+this.properties.label+"</label><input class='textfield' type='text' name='"+this.name+"' id='"+this.control_id()+"' value=\""+this.properties.value+"\" /></div>";
	this.jquery_place().replaceWith(html);

	var self = this;
	this.jquery().change(function(){
		self.basewidget.fire_event( this.name, 'changed' );
	});
};

////////////////////////////////////////////////////////////////////////////////


