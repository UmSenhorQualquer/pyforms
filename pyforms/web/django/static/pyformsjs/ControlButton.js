

function ControlButton(name, properties){
	ControlBase.call(this, name, properties);
};
ControlButton.prototype = Object.create(ControlBase.prototype);


////////////////////////////////////////////////////////////////////////////////

ControlButton.prototype.init_control = function(){
	var html = "<div class='field ControlButton' id='"+this.place_id()+"' ><label>&nbsp;</label>";
	html +="<button type='button' title='"+this.properties.help+"' id='"+this.control_id()+"' class='ui button' >";
	html += this.properties.label;
	html += '</button>';
	html += '</div>';
	
	this.jquery_place().replaceWith(html);

	var self = this;
	this.jquery().click(function(){
		self.basewidget.fire_event( self.name, 'pressed' )
	});

	if(this.properties.visible) 
		this.jquery_place().show();
	else 
		this.jquery_place().hide();
};

////////////////////////////////////////////////////////////////////////////////