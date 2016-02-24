

function ControlDate(name, properties){
	ControlBase.call(this, name, properties);
};
ControlDate.prototype = Object.create(ControlBase.prototype);

////////////////////////////////////////////////////////////////////////////////

ControlDate.prototype.init_control = function(){
	this.jquery_place().replaceWith("<div title='"+this.properties.help+"' class='ControlDate' ><label for='"+this.control_id()+"'>"+this.properties.label+"</label><input class='textfield' type='text' name='"+this.name+"' id='"+this.control_id()+"' value=\""+this.properties.value+"\" /></div>");
	this.jquery().datepicker({dateFormat: "yy-mm-dd"});

	var self = this;
	this.jquery().change(function(){
		self.basewidget.fire_event( self.name, 'changed' );
	});
};

////////////////////////////////////////////////////////////////////////////////