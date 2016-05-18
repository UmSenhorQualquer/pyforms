

function ControlImage(name, properties){
	ControlBase.call(this, name, properties);
};
ControlImage.prototype = Object.create(ControlBase.prototype);

////////////////////////////////////////////////////////////////////////////////

ControlImage.prototype.get_value = function(){ 
	return this.jquery().attr('src');
};

////////////////////////////////////////////////////////////////////////////////

ControlImage.prototype.set_value = function(value){
	if(value.image) this.jquery().attr("src", "data:image/png;base64,"+value.image);

	var width = this.jquery().width();
	this.jquery().css('width', width+"px");

};

////////////////////////////////////////////////////////////////////////////////

ControlImage.prototype.init_control = function(){
	var html = "<div id='"+this.place_id()+"' class='field ControlImage' >";
	html += "<div class='ui card' id='card"+this.control_id()+"' >";
	html += "<div class='image'>";
	html += "<img style='width:100%;' class='image' src='' id='"+this.control_id()+"' />";
	html += "</div>";
	html += "</div>";
	html += "</div>";
	this.jquery_place().replaceWith(html);

	if(this.properties.visible) 
		this.jquery_place().show();
	else 
		this.jquery_place().hide();
};

////////////////////////////////////////////////////////////////////////////////
