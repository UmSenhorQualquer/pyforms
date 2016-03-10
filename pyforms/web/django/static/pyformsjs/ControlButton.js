

function ControlButton(name, properties){
	ControlBase.call(this, name, properties);
};
ControlButton.prototype = Object.create(ControlBase.prototype);


////////////////////////////////////////////////////////////////////////////////

ControlButton.prototype.init_control = function(){
	var html = "<div class='ControlButton' >";
	html +="<button title='"+this.properties.help+"'  value='"+this.properties.label+"' id='"+this.control_id()+"' class='btn' >";
	html += '<i class="glyphicon glyphicon-cog"></i> '+ this.properties.label;
	html += '</button>';
	html += '</div>';
	
	this.jquery_place().replaceWith(html);

	var self = this;
	this.jquery().click(function(){
		self.basewidget.fire_event( self.name, 'pressed' )
	});
};

////////////////////////////////////////////////////////////////////////////////