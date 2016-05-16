

function ControlDate(name, properties){
	ControlBase.call(this, name, properties);
};
ControlDate.prototype = Object.create(ControlBase.prototype);

////////////////////////////////////////////////////////////////////////////////

ControlDate.prototype.init_control = function(){
	var html = "<div id='"+this.place_id()+"' class='field ControlDate' ><label>"+this.properties.label+"</label><input placeholder='"+this.properties.label+"' type='text' name='"+this.name+"' id='"+this.control_id()+"' value=\""+this.properties.value+"\" /></div>";
	this.jquery_place().replaceWith(html);
	this.jquery().datepicker({dateFormat: "yy-mm-dd"});

	var self = this;
	this.jquery().change(function(){
		self.basewidget.fire_event( self.name, 'changed' );
	});
};

////////////////////////////////////////////////////////////////////////////////