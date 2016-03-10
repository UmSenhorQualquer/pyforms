

function ControlCombo(name, properties){
	ControlBase.call(this, name, properties);
};
ControlCombo.prototype = Object.create(ControlBase.prototype);

////////////////////////////////////////////////////////////////////////////////

ControlCombo.prototype.init_control = function(){
	this.jquery_place().replaceWith("<div title='"+this.properties.help+"' class='ControlCombo' ><label title='"+this.properties.help+"' for='"+this.control_id()+"'>"+this.properties.label+"</label><select type='button' id='"+this.control_id()+"' ></select></div>")
	var select = document.getElementById(this.control_id());
	var index;
	for (var index = 0; index < this.properties.items.length; ++index) {
		var option = document.createElement("option");
		option.text  = this.properties.items[index].label;
		option.value = this.properties.items[index].value;
		select.add( option );
	}
};

////////////////////////////////////////////////////////////////////////////////