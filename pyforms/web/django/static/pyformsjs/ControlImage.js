

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
	this.jquery().attr("src", "data:image/png;base64,"+value.image);
};

////////////////////////////////////////////////////////////////////////////////

ControlImage.prototype.init_control = function(){
	var html = "<div class='ControlImage' >";
	html += "<img style='width:100%;' class='image' src='' id='"+this.control_id()+"' />";
	html += "</div>";
	$( "#place-"+this.control_id() ).replaceWith(html);
};

////////////////////////////////////////////////////////////////////////////////