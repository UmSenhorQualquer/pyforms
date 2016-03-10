function selectFile2Control(dom_id,filename, name, widget_id){
	$( "#dialog"+dom_id ).dialog('destroy');
	$(  "#"+dom_id).val(filename);
	console.log(widget_id);
	console.log(pyforms.find_app(widget_id));
	pyforms.find_app(widget_id).fire_event( name, 'changed' )
}


function ControlFile(name, properties){
	ControlBase.call(this, name, properties);
};
ControlFile.prototype = Object.create(ControlBase.prototype);

////////////////////////////////////////////////////////////////////////////////

ControlFile.prototype.file_row_event = function(row, dom){
	var control_id = $(this).attr('id');
	var name = $(this).attr('name');
	var widget_id = $(this).attr('basewidget');
	row.values[0] = "<a class='file2select' href='javascript:selectFile2Control(\""+control_id+"\",\""+row.file+"\", \""+name+"\", \""+widget_id+"\")' >"+row.filename+"</a>";
	row.values.pop();
	return row;
};

////////////////////////////////////////////////////////////////////////////////

ControlFile.prototype.init_control = function(){
	var html = "<div class='ControlFile' ><label for='"+this.control_id()+"' title='"+this.properties.help+"' >"+this.properties.label+"</label>";
	html += "<input type='text' class='filename' basewidget='"+this.basewidget.widget_id+"' name='"+this.name+"' id='"+this.control_id()+"' value='"+this.properties.value+"' />";
	html += '<button id="button'+this.control_id()+'" class="btn "><i class="glyphicon glyphicon-folder-open icon-white"></i></button>';
	html += "<div id='dialog"+this.control_id()+"' dom-id='"+this.control_id()+"' class='dialog' style='display:none;' title='Pick a file'></div>";
	this.jquery_place().replaceWith(html);

	var self = this;
	function reload_folder(){
		if( $('#files-browser-div').size()>0 ){
			var folder = $('#files-browser-div').dataviewer('path');
			if(folder==undefined) folder = '/';
		}else folder = '/'
		$( "#dialog"+self.control_id()).dataviewer( {url: '/browsefiles/?backfolder=false&p='+folder, path:folder } );
		$( "#dialog"+self.control_id()).dataviewer();
	}
	
	$("#dialog"+this.control_id()).dataviewer({ 
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

	$( "#button"+this.control_id() ).unbind('click');
	$( "#button"+this.control_id() ).click(function(){
		$( "#dialog"+self.control_id() ).dialog({ show: 'slideDown',width: 900, height: 600, position: { at: "top" }, draggable: false });
		reload_folder();
	});
};

////////////////////////////////////////////////////////////////////////////////