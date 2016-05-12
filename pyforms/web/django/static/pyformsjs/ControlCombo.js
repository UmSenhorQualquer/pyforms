

function ControlCombo(name, properties){
	ControlBase.call(this, name, properties);
};
ControlCombo.prototype = Object.create(ControlBase.prototype);

////////////////////////////////////////////////////////////////////////////////

ControlCombo.prototype.init_control = function(){
	var html = "<div id='"+this.place_id()+"' class='ui labeled input ControlCombo' ><div class='ui label'>"+this.properties.label+"</div>";
	html += "<select class='ui dropdown' id='"+this.control_id()+"' ></select></div>";

	this.jquery_place().replaceWith(html);
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

ControlCombo.prototype.set_value = function(value){
	console.log("set: "+value);
	this.jquery().val(value); 
};

////////////////////////////////////////////////////////////////////////////////

ControlCombo.prototype.get_value = function(){ 
	console.log('get: '+ this.jquery().find('option:selected').val());
	return this.jquery().find('option:selected').val(); 
};