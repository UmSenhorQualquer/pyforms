

function ControlCheckBox(name, properties){
	ControlBase.call(this, name, properties);
};
ControlCheckBox.prototype = Object.create(ControlBase.prototype);

////////////////////////////////////////////////////////////////////////////////

ControlCheckBox.prototype.set_value = function(value){
	if(value=='True')
		this.jquery().prop('checked', true);
	else
		this.jquery().prop('checked', false);

};

////////////////////////////////////////////////////////////////////////////////

ControlCheckBox.prototype.get_value = function(){
	return this.jquery().is(':checked');
};

////////////////////////////////////////////////////////////////////////////////

ControlCheckBox.prototype.init_control = function(){
	var html = "<div class='field ControlCheckBox' id='"+this.place_id()+"' >";
	html += "<div class='ui toggle checkbox' title='"+this.properties.help+"' >";
	html += "<input name='"+this.name+"' id='"+this.control_id()+"' type='checkbox' value='true' class='hidden' />";
	html += "<label for='"+this.control_id()+"'>"+this.properties.label+"</label>";
	html += "</div></div>";
	this.jquery_place().replaceWith(html);
	
	if( this.properties.value=='True')
		this.jquery().prop('checked', true);
	else
		this.jquery().prop('checked', false);

	var self = this;
	this.jquery().click(function(){ self.basewidget.fire_event( self.name, 'changed' ); });

	if(this.properties.visible) 
		this.jquery_place().show();
	else 
		this.jquery_place().hide();
};

////////////////////////////////////////////////////////////////////////////////
