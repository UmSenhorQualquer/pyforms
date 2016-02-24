

function ControlCheckBox(name, properties){
	ControlBase.call(this, name, properties);
};
ControlCheckBox.prototype = Object.create(ControlBase.prototype);

////////////////////////////////////////////////////////////////////////////////

ControlCheckBox.prototype.set_value = function(value){
	this.jquery().prop('checked', value);
};

////////////////////////////////////////////////////////////////////////////////

ControlCheckBox.prototype.get_value = function(){
	return this.jquery().is(':checked');
};

////////////////////////////////////////////////////////////////////////////////

ControlCheckBox.prototype.init_control = function(){
	this.jquery_place().replaceWith("<div title='"+this.properties.help+"' class='ControlCheckBox' ><label for='"+this.control_id()+"'>"+this.properties.label+"</label><input class='textfield' type='checkbox' name='"+this.name+"' id='"+this.control_id()+"' value='true' /></div>");
	if( this.properties.value=='True') this.jquery().prop('checked', true);

	var self = this;
	this.jquery().click(function(){ self.basewidget.fire_event( self.name, 'changed' ); });
};

////////////////////////////////////////////////////////////////////////////////
