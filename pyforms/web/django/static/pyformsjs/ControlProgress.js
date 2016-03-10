


function ControlProgress(name, properties){
	ControlBase.call(this, name, properties);
};
ControlProgress.prototype = Object.create(ControlBase.prototype);


////////////////////////////////////////////////////////////////////////////////

ControlProgress.prototype.init_control = function(){
	this.jquery_place().replaceWith("<div title='"+this.properties.help+"' id='"+this.control_id()+"' class='progressbar' ></div>");
};

////////////////////////////////////////////////////////////////////////////////