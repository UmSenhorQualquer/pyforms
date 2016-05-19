

function ControlTimeout(name, properties){
	ControlBase.call(this, name, properties);
	this.timer = undefined;
	
};
ControlTimeout.prototype = Object.create(ControlBase.prototype);


////////////////////////////////////////////////////////////////////////////////

ControlTimeout.prototype.init_control = function(){
	var html = "<div id='"+this.place_id()+"' class='field ControlTimeout' ><label>"+this.properties.label+"</label>";
	html 	+= "<div id='"+this.control_id()+"' data-percent='0' class='ui tiny progress'><div class='bar'></div></div>";
	html 	+= '</div>'
	this.jquery_place().replaceWith(html);

	if(this.properties.visible) 
		this.jquery_place().show();
	else 
		this.jquery_place().hide();

	this.set_value(this.properties.value);
	if (this.properties.play=='True') this.update_progress_bar(true);
};

////////////////////////////////////////////////////////////////////////////////

ControlTimeout.prototype.update_progress_bar = function(firsttime){
	if(!firsttime) this.jquery().progress('increment',this.properties.update_interval);

	if( parseInt(this.jquery().attr('data-percent'))<100 ){
		var self = this;
		this.timer = setTimeout(function(){ self.update_progress_bar(false); }, self.properties.update_interval);
	}else{
		this.basewidget.fire_event( this.name, 'trigger_event' );
	}
};

////////////////////////////////////////////////////////////////////////////////

ControlTimeout.prototype.get_value = function(){ 
	return this.properties.value;
};

////////////////////////////////////////////////////////////////////////////////

ControlTimeout.prototype.set_value = function(value){
	this.jquery().progress({total: value, value:0});
};

////////////////////////////////////////////////////////////////////////////////

ControlTimeout.prototype.deserialize = function(data){
	data.play 		= 'True'==data.play
	last_play_value = this.properties.play
	$.extend(this.properties, data);

	if(this.properties.play==false || data.value !== undefined)
		if(this.timer!=undefined){ 
			clearTimeout(this.timer);
			this.timer=undefined;
		}

	if (data.value !== undefined){
		this.set_value(this.properties.value);
		if (this.properties.play) this.update_progress_bar(false);
	}
	
	if (last_play_value==false && this.properties.play)
		this.update_progress_bar(false);

	if(this.properties.visible) 
		this.jquery_place().show();
	else 
		this.jquery_place().hide();
};
