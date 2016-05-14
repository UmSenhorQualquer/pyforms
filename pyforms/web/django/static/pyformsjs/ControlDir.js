function add_dir2control(control_id, filename, name){
	$( "#dialog"+control_id ).modal('hide');
	$( "#"+control_id ).val(filename);
	
	var ids 			= pyforms.split_id(control_id);
	var widget_id 		= ids[0];
	var control_name 	= ids[1];

	pyforms.find_app(widget_id).fire_event( control_name, 'changed' )
}



function ControlDir(name, properties){
	ControlBase.call(this, name, properties);
};
ControlDir.prototype = Object.create(ControlBase.prototype);

////////////////////////////////////////////////////////////////////////////////

ControlDir.prototype.file_row_event = function(row, dom){
	var control = pyforms.find_control( (""+dom[0].id).substring(15)) ;
	row.values[0] = "<a class='file2select' href='javascript:add_dir2control(\""+control.control_id()+"\",\""+row.file+"\")' >"+row.filename+"</a>";
	row.values.pop();
	return row;
};

////////////////////////////////////////////////////////////////////////////////

ControlDir.prototype.init_control = function(){

	var html = "<div class='field ControlDir' id='"+this.place_id()+"' ><label>"+this.properties.label+"</label>";
	html += "<input type='text' class='filename' basewidget='"+this.basewidget.widget_id+"' name='"+this.name+"' id='"+this.control_id()+"' value='"+this.properties.value+"'  placeholder='"+this.properties.label+"' />";
	html += "<div class='ui modal' id='dialog"+this.control_id()+"' ><i class='close icon'></i><div class='header'>"+this.properties.label+"</div><div class='content' id='dialog-content-"+this.control_id()+"'  dom-id='"+this.control_id()+"' ></div></div>";
	
	this.jquery_place().replaceWith(html);

	var self = this;
	function reload_folder(){
		if( $('#files-browser-div').size()>0 ){
			var folder = $('#files-browser-div').dataviewer('path');
			if(folder==undefined) folder = '/';
		}else folder = '/'
		$( "#dialog-content-"+self.control_id()).dataviewer( {url: '/browsefiles/?backfolder=false&p='+folder, path:folder } );
		$( "#dialog-content-"+self.control_id()).dataviewer();
	}
	
	$("#dialog-content-"+this.control_id()).dataviewer({ 
		titles: ['File name','Size', 'Created on',''],
		sizes: 	['auto','120px','220px','50px'],
		sortingColumns: [0,1,2],
		updateRowFunction: this.file_row_event,
		extra_buttons: [{
			btnId:'reload-folder', 
			btnLabel:'Reload', 
			btnAction: reload_folder
		}]
	});

	this.jquery().unbind('click');
	this.jquery().click(function(){
		$( "#dialog"+self.control_id() ).modal('show');
		reload_folder();
	});
};

////////////////////////////////////////////////////////////////////////////////
