

function ControlTimeout(name, properties){
	ControlBase.call(this, name, properties);
};
ControlTimeout.prototype = Object.create(ControlBase.prototype);


////////////////////////////////////////////////////////////////////////////////

ControlTimeout.prototype.init_control = function(){
	var html = "<div id='"+this.place_id()+"' class='field ControlTimeout' ><label>"+this.properties.label+"</label>";
	html += "<div id='"+this.control_id()+"' data-percent='0' class='ui tiny progress'><div class='bar'></div></div>";
	html += '</div>'
	this.jquery_place().replaceWith(html);

	var self = this;
	
	this.jquery().progress({total: self.properties.total_seconds, value:0 });
	this.update_progress_bar();
	
	this.jquery().change(function(){
		self.basewidget.fire_event( this.name, 'trigger' );
	});

	if(this.properties.visible) 
		this.jquery_place().show();
	else 
		this.jquery_place().hide();
};

////////////////////////////////////////////////////////////////////////////////

ControlTimeout.prototype.update_progress_bar = function(){
	this.jquery().progress('increment');

	if( parseInt(this.jquery().attr('data-percent'))<100 ){
		var self = this;
		setTimeout(function(){ self.update_progress_bar(); }, 1000);
	}
	console.log('passou aqui', this.jquery().attr('data-percent'));
};

////////////////////////////////////////////////////////////////////////////////