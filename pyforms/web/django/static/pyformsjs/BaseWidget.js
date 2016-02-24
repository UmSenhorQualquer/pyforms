

function BaseWidget(widget_id, widget_name, controls){
	this.name 		= widget_name;
	this.widget_id 	= widget_id;
	this.controls 	= controls;
	this.events_queue = [];

	for(var index = 0; index < controls.length; index++){
		controls[index].basewidget = this;
		controls[index].init_control();
	};
	$('.application-tabs').tabs()
}

////////////////////////////////////////////////////////////

BaseWidget.prototype.control_id = function(name){
	return this.widget_id+'-'+name;
}

////////////////////////////////////////////////////////////

BaseWidget.prototype.current_folder = function(){
	try {
    	var currentfolder = $('#files-browser-div').dataviewer('path');
		if(currentfolder==undefined) currentfolder = '/';
	}
	catch(err) {
	    currentfolder = '/';
	}	
	return currentfolder;
}

////////////////////////////////////////////////////////////

BaseWidget.prototype.fire_event = function(dom_in, event){
	data = {event: {control:dom_in, event: event}, userpath: this.current_folder() };
	this.events_queue.push(data)
	this.update_data( this.events_queue.pop(0) );
}

////////////////////////////////////////////////////////////

BaseWidget.prototype.update_controls = function(){	
	this.update_data({ userpath: this.current_folder() }); 
};

////////////////////////////////////////////////////////////

BaseWidget.prototype.serialize_data = function(data){
	for (index = 0; index <  this.controls.length; index++) {
		var name 	= this.controls[index].name;
		data[name] 	= this.controls[index].serialize();
	};
	return data;
};

////////////////////////////////////////////////////////////

BaseWidget.prototype.update_data = function(data2send){	
	loading();
	
	data2send = this.serialize_data(data2send);

	var self = this;
	var jsondata =  $.toJSON(data2send);
	$.ajax({
		method: 'post',
		cache: false,
		dataType: "json",
		url: '/pyforms/update/'+ this.name+'/?nocache='+$.now(),
		data: jsondata,
		contentType: "application/json; charset=utf-8",
		success: function(res){
			if( res.result=='error' ){
				error(res.msg);
			}else{
				for (var index = 0; index < self.controls.length; index++) {
					var name 		= self.controls[index].name;
					if(res[name])  	  self.controls[index].deserialize( res[name] );
				};
			}
		}
	}).fail(function(xhr){
		error(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
	}).always(function(){
		not_loading();
	});
	
	if(  this.events_queue.length>0 )  this.update_data(  this.events_queue.pop(0) );
}

////////////////////////////////////////////////////////////

BaseWidget.prototype.update_controls = function(){	
	this.update_data({ userpath: this.current_folder() }); 
};
