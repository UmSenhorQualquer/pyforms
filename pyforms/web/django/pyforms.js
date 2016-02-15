function sleep(ms) {
	var unixtime_ms = new Date().getTime();
	while(new Date().getTime() < unixtime_ms + ms) {}
}

function ControlButton( label, dom_id, help ){

	this.LABEL = label;
	this.DOMID = dom_id;
	var self = this;
	
	this.rawValue = function(value){};
	this.setValue = function(value){};
	this.getValue = function(){};
	this.load = function(){
		var html = "<div class='ControlButton' >";
		html +="<button title='"+help+"'  value='"+this.LABEL+"' id='"+self.app.control_id(dom_id)+"' class='btn' >";
		html += '<i class="glyphicon glyphicon-cog"></i> '+ this.LABEL;
		html += '</button>';
		html += '</div>';
		$( "#place-"+self.app.control_id(dom_id) ).html(html);

		$( "#"+self.app.control_id(dom_id) ).click(function(){
			self.app.FireEvent( dom_id, 'pressed' )
		});
	};
	
};


function ControlCheckBox( label, dom_id, value, help ){

	this.LABEL = label;
	this.DOMID = dom_id;
	var self = this;

	this.rawValue = function(value){ return $( "#"+self.app.control_id(dom_id) ).is(':checked'); };
	this.setValue = function(value){ $( "#"+self.app.control_id(dom_id) ).prop('checked', value);};
	this.getValue = function(){ return $( "#"+self.app.control_id(dom_id) ).is(':checked'); };
	this.load = function(){
		$( "#place-"+self.app.control_id(dom_id) ).replaceWith("<div title='"+help+"' class='ControlText' ><label for='"+self.app.control_id(dom_id)+"'>"+this.LABEL+"</label><input class='textfield' type='checkbox' name='"+dom_id+"' id='"+self.app.control_id(dom_id)+"' value='true' /></div>");
		$( "#"+self.app.control_id(dom_id) ).click(function(){ self.app.FireEvent( dom_id, 'changed' ); });

		if( value=='True') $( "#"+self.app.control_id(dom_id) ).prop('checked', true);
	};
	
};




function ControlCombo( label, dom_id, values, help ){

	this.LABEL = label;
	this.DOMID = dom_id;
	this.VALUES = values;
	
	this.rawValue = function(value){return $( "#"+self.app.control_id(dom_id) ).val();};
	this.setValue = function(value){$( "#"+self.app.control_id(dom_id) ).val(value)};
	this.getValue = function(){return $( "#"+self.app.control_id(dom_id) ).val();};
	this.load = function(){
		$( "#place-"+self.app.control_id(dom_id) ).replaceWith("<div title='"+help+"' class='ControlText' ><label title='"+help+"'  for='"+self.app.control_id(dom_id)+"'>"+this.LABEL+"</label><select type='button' id='"+self.app.control_id(dom_id)+"' ></select></div>")
		var select = document.getElementById(dom_id);
		var index;
		for (index = 0; index < this.VALUES.length; ++index) {
			var option = document.createElement("option");
			option.text = this.VALUES[index][0];
			option.value = this.VALUES[index][1];
			select.add( option );
		}
	};
};

function selectFile2Control(dom_id,filename, name){
	$( "#dialog"+dom_id ).dialog('destroy');
	$(  "#"+dom_id).val(filename);
	self.app.FireEvent( name, 'changed' )
}


function ControlDir( label, dom_id, value, help ){
	this.LABEL = label;
	this.DOMID = dom_id;
	var self = this;


	this.FileRowEvent = function(row, dom){
		//var trow_id = $(dom).attr('dom-id');

		row.values[0] = "<a class='file2select' href='javascript:selectFile2Control(\""+self.app.control_id(dom_id)+"\",\""+row.file+"\", \""+dom_id+"\")' >"+row.filename+"</a>";
		row.values.pop();
		return row;
	}
	this.setValue = function(value){
		$( "#"+self.app.control_id(dom_id) ).val(value)
	};
	this.getValue = function(){ return $( "#"+self.app.control_id(dom_id) ).val(); };
	this.rawValue = function(value){ return $( "#"+self.app.control_id(dom_id) ).val(); };
	this.load = function(){
		var html = "<div class='ControlFile' ><label for='"+self.app.control_id(dom_id)+"' title='"+help+"' >"+this.LABEL+"</label>";
		html += "<input type='text' class='filename' name='"+dom_id+"' id='"+self.app.control_id(dom_id)+"' value='"+value+"' />";
		//html += "<input class='choose-file-button' type='image' src='/static/upload.png' id='button"+dom_id+"' />";
		html += '<button id="button'+self.app.control_id(dom_id)+'" class="btn "><i class="glyphicon glyphicon-folder-open icon-white"></i></button>';
		html += "<div id='dialog"+self.app.control_id(dom_id)+"' dom-id='"+self.app.control_id(dom_id)+"' class='dialog' style='display:none;' title='Pick a file'></div>";
		
		function reloadFolder(){
			if( $('#files-browser-div').size()>0 ){
				var folder = $('#files-browser-div').dataviewer('path');
				if(folder==undefined) folder = '/';
			}else folder = '/'
			$( "#dialog"+self.app.control_id(dom_id)).dataviewer( {url: '/browsefiles/?backfolder=false&p='+folder, path:folder } );
			$( "#dialog"+self.app.control_id(dom_id)).dataviewer();
		}
		
		$( "#place-"+self.app.control_id(dom_id) ).replaceWith(html);
		$( "#dialog"+self.app.control_id(dom_id)).dataviewer({ 
			titles: ['File name','Size', 'Created on',''],
			sizes: 	['auto','120px','220px','50px'],
			sortingColumns: [0,1,2],
			updateRowFunction: self.FileRowEvent,
			extra_buttons: [{
				btnId:'reload-folder', 
				btnLabel:'Reload', 
				btnAction: reloadFolder
			}]
		});

		$( "#button"+self.app.control_id(dom_id) ).unbind('click');
		$( "#button"+self.app.control_id(dom_id) ).click(function(){
			$( "#dialog"+self.app.control_id(dom_id) ).dialog({ show: 'slideDown',width: 900, height: 600, position: { at: "top" }, draggable: false });
			reloadFolder();
		});
	};
	
};


function ControlFile( label, dom_id, value, help ){
	this.LABEL = label;
	this.DOMID = dom_id;
	var self = this;

	this.FileRowEvent = function(row, dom){
		//var dom_id = $(dom).attr('dom-id');
		row.values[0] = "<a class='file2select' href='javascript:selectFile2Control(\""+self.app.control_id(dom_id)+"\",\""+row.file+"\", \""+dom_id+"\")' >"+row.filename+"</a>";
		row.values.pop();
		return row;
	}
	this.setValue = function(value){
		$( "#"+self.app.control_id(dom_id) ).val(value)
	};
	this.getValue = function(){ return $( "#"+self.app.control_id(dom_id) ).val(); };
	this.rawValue = function(value){ return $( "#"+self.app.control_id(dom_id) ).val(); };
	this.load = function(){
		var html = "<div class='ControlFile' ><label for='"+self.app.control_id(dom_id)+"' title='"+help+"' >"+this.LABEL+"</label>";
		html += "<input type='text' class='filename' name='"+dom_id+"' id='"+self.app.control_id(dom_id)+"' value='"+value+"' />";
		//html += "<input class='choose-file-button' type='image' src='/static/upload.png' id='button"+dom_id+"' />";
		html += '<button id="button'+self.app.control_id(dom_id)+'" class="btn "><i class="glyphicon glyphicon-folder-open icon-white"></i></button>';
		html += "<div id='dialog"+self.app.control_id(dom_id)+"' dom-id='"+self.app.control_id(dom_id)+"' class='dialog' style='display:none;' title='Pick a file'></div>";
		
		function reloadFolder(){
			if( $('#files-browser-div').size()>0 ){
				var folder = $('#files-browser-div').dataviewer('path');
				if(folder==undefined) folder = '/';
			}else folder = '/'
			$( "#dialog"+self.app.control_id(dom_id)).dataviewer( {url: '/browsefiles/?backfolder=false&p='+folder, path:folder } );
			$( "#dialog"+self.app.control_id(dom_id)).dataviewer();
		}
		
		$( "#place-"+self.app.control_id(dom_id) ).replaceWith(html);
		$( "#dialog"+self.app.control_id(dom_id)).dataviewer({ 
			titles: ['File name','Size', 'Created on',''],
			sizes: 	['auto','120px','220px','50px'],
			sortingColumns: [0,1,2],
			updateRowFunction: self.FileRowEvent,
			extra_buttons: [{
				btnId:'reload-folder', 
				btnLabel:'Reload', 
				btnAction: reloadFolder
			}]
		});

		$( "#button"+self.app.control_id(dom_id) ).unbind('click');
		$( "#button"+self.app.control_id(dom_id) ).click(function(){
			$( "#dialog"+self.app.control_id(dom_id) ).dialog({ show: 'slideDown',width: 900, height: 600, position: { at: "top" }, draggable: false });
			reloadFolder();
		});
	};
	
};

function ControlImage( dom_id , help ){

	this.DOMID = dom_id;
	this.FILENAME = '';
	
	this.rawValue = function(value){ return $( "#"+self.app.control_id(dom_id) ).attr('src'); };
	this.setValue = function(value){
		$( "#"+self.app.control_id(dom_id) + " .image" ).attr("src", "data:image/png;base64,"+value.image);
		this.FILENAME   = value.filename;
	};
	this.getValue = function(){
		return { filename: this.FILENAME }
	};
	this.load = function(){
		var html = "<div class='ControlImage' >";
		html += "<img style='width:100%;' class='image' src='' id='"+self.app.control_id(dom_id)+"' />";
		html += "</div>";
		$( "#place-"+self.app.control_id(dom_id) ).replaceWith(html);
		
	};
	
};

function ControlPlayer( dom_id, help ){
	this.DOMID = dom_id;
	this.FILENAME = '';
	var self = this;
	
	this.rawValue = function(value){};
	this.setValue = function(value){
		$( "#timeline"+self.app.control_id(dom_id) ).slider({min: value.min, max: value.max, value: value.position});
		this.FILENAME = value.filename;
		$( "#display"+self.app.control_id(dom_id) ).attr("src", "data:image/png;base64,"+value.frame);
	};
	this.getValue = function(){
		var pos = $( "#timeline"+self.app.control_id(dom_id) ).slider("value");
		var res = { position: pos, filename: this.FILENAME };
		return res;
	};
	this.load = function(){
		var html = "<div class='ControlPlayer' >";
		html += "<img style='width:100%;' class='image' src=' ' id='display"+self.app.control_id(dom_id)+"' />";
		html += "<div class='slider' name='"+dom_id+"' id='timeline"+self.app.control_id(dom_id)+"' ></div>";
		html += "</div>";
		$( "#place-"+self.app.control_id(dom_id) ).replaceWith(html);
		$( "#timeline"+self.app.control_id(dom_id) ).slider( {stop: self.app.UpdateControls });
	};
	
};

function ControlProgress( dom_id , help ){

	this.DOMID = dom_id;
	
	this.rawValue = function(value){};
	this.setValue = function(value){};
	this.getValue = function(){};
	this.load = function(){
		$( "#place-"+self.app.control_id(dom_id) ).replaceWith("<div title='"+help+"'   id='"+self.app.control_id(dom_id)+"' class='progressbar' ></div>");
	};	
};

function ControlSlider( label, dom_id, value, min, max, help  ){

	this.LABEL = label;
	this.DOMID = dom_id;
	this.VALUE = value
	this.MIN = min;
	this.MAX = max;
	var self = this;
	
	this.setValue = function(val){
		$( "#"+self.app.control_id(dom_id) ).slider({value:val})
		$( "#value"+dom_id ).html(  val );
	};
	this.getValue = function(){
		return { position: $( "#"+self.app.control_id(dom_id) ).slider("value") }
	};
	this.rawValue = function(value){ return $( "#"+self.app.control_id(dom_id) ).slider("value")  };
	this.load = function(){
		var html = 	"<div class='ControlSlider' title='"+help+"'   >";
		html += 	"<label style='margin-right: 20px;' for='"+self.app.control_id(dom_id)+"'>"+this.LABEL+": <small id='value"+self.app.control_id(dom_id)+"' style='color:red' >"+this.VALUE+"</small></label>";
		html += 	"<div class='slider' name='"+dom_id+"' id='"+self.app.control_id(dom_id)+"' ></div>";
		html += 	"</div>";
		$( "#place-"+self.app.control_id(dom_id) ).replaceWith(html);
		$( "#"+self.app.control_id(dom_id) ).slider({ 
			slide: function( event, ui ) {
				$( "#value"+dom_id ).html(  ui.value );
			},
			stop: function(){ self.app.FireEvent( dom_id, 'changed' )}, min: this.MIN, max: this.MAX,  value: this.VALUE });
	};
	
};


function ControlBoundingSlider( label, dom_id, value, min, max, horizontal, help  ){

	this.LABEL = label;
	this.DOMID = dom_id;
	this.VALUE = value;
	this.MIN = min;
	this.MAX = max;
	var self = this;
	
	this.setValue = function(val){
		$( "#"+self.app.control_id(dom_id) ).slider({values:val})
		$( "#value"+dom_id ).html(  val );
	};
	this.getValue = function(){
		return { position: $( "#"+self.app.control_id(dom_id) ).slider("values") }
	};
	this.rawValue = function(value){ return $( "#"+self.app.control_id(dom_id) ).slider("values")  };
	this.load = function(){
		var html = 	"<div class='ControlSlider' title='"+help+"'   >";
		html += 	"<label style='margin-right: 20px;' for='"+self.app.control_id(dom_id)+"'>"+this.LABEL+": <small id='value"+self.app.control_id(dom_id)+"' style='color:red' >"+this.VALUE+"</small></label>";
		html += 	"<div class='slider' name='"+dom_id+"' id='"+self.app.control_id(dom_id)+"' ></div>";
		html += 	"</div>";
		$( "#place-"+self.app.control_id(dom_id) ).replaceWith(html);
		$( "#"+self.app.control_id(dom_id) ).slider({ 
			range: true,
			slide: function( event, ui ) {
				$( "#value"+dom_id ).html(  ui.value );
			},
			stop: function(){ self.app.FireEvent( dom_id, 'changed' )}, 
			min: this.MIN, max: this.MAX, values: this.VALUE });
	};
	
};

function ControlText( label, dom_id, value, help ){

	this.LABEL = label;
	this.DOMID = dom_id;
	var self = this;

	this.rawValue = function(value){ return $( "#"+self.app.control_id(dom_id) ).val(); };
	this.setValue = function(value){
		$( "#"+self.app.control_id(dom_id) ).val(value)
	};
	this.getValue = function(){ return $( "#"+self.app.control_id(dom_id) ).val(); };
	this.load = function(){
		if(!value) value = '';

		$( "#place-"+self.app.control_id(dom_id) ).replaceWith("<div title='"+help+"' class='ControlText' ><label for='"+self.app.control_id(dom_id)+"'>"+this.LABEL+"</label><input class='textfield' type='text' name='"+dom_id+"' id='"+self.app.control_id(dom_id)+"' value=\""+value+"\" /></div>");

		$( "#"+self.app.control_id(dom_id) ).change(function(){
			self.app.FireEvent( dom_id, 'changed' );
		});
	};
	
};

function ControlDate( label, dom_id, value, help ){

	this.LABEL = label;
	this.DOMID = dom_id;
	var self = this;

	this.rawValue = function(value){ return $( "#"+self.app.control_id(dom_id) ).val(); };
	this.setValue = function(value){
		$( "#"+self.app.control_id(dom_id) ).val(value)
	};
	this.getValue = function(){ return $( "#"+self.app.control_id(dom_id) ).val(); };
	this.load = function(){
		if(!value) value = '';
		$( "#place-"+self.app.control_id(dom_id) ).replaceWith("<div title='"+help+"' class='ControlDate' ><label for='"+self.app.control_id(dom_id)+"'>"+this.LABEL+"</label><input class='textfield' type='text' name='"+dom_id+"' id='"+self.app.control_id(dom_id)+"' value=\""+value+"\" /></div>");

		$( "#"+self.app.control_id(dom_id) ).datepicker({dateFormat: "yy-mm-dd"});

		$( "#"+self.app.control_id(dom_id) ).change(function(){
			self.app.FireEvent( dom_id, 'changed' );
		});
	};
	
};

function ControlList( label, dom_id, value, help ){

	this.LABEL = label;
	this.DOMID = dom_id;
	var self = this;
	var being_edited = false;


	this.load_table = function(titles, data){
		var html = "<table id='"+self.app.control_id(dom_id)+"' >";
		html += "<thead>";
		html += "<tr>";
		for(var i=0; i<titles.length; i++){
			html += "<th>"+titles[i]+"</th>";
		};
		html += "</tr>";
		html += "</thead>";
		html += "<tbody>";
		for(var i=0; i<data.length; i++){
			html += "<tr>";
			for(var j=0; j<data[i].length; j++)
				html += "<td>"+data[i][j]+"</td>";
			if(data[i].length<titles.length)
				for(var j=data[i].length; j<titles.length; j++) html += "<td></td>";
			html += "</tr>";
		};
		html += "</tbody>";
		html += "</table>";
		html += "</div>";
		$( "#"+self.app.control_id(dom_id) ).replaceWith(html);

		$( "#"+self.app.control_id(dom_id)+" tbody td" ).dblclick(function(){
			if( being_edited ) return false;

			being_edited = true;
			var cell = $(this);
			var value = cell.html();
			cell.html('<input type="text" value="'+value+'" />');
			cell.children('input').focus();
			cell.children('input').focusout(function(){
				cell.html($(this).val());
				being_edited = false;
				self.app.FireEvent( dom_id, 'changed' );
			});
		});
	};

	this.rawValue = function(value){ return undefined; };
	this.setValue = function(value){ this.load_table(value[0],value[1]); };
	this.getValue = function(){ 
		var res=[];
		$(  "#"+self.app.control_id(dom_id)+" tbody tr" ).each(function(i, row){
			var new_row=[]
			$(this).children('td').each(function(j, col){
				new_row.push($(col).html());
			});
			res.push(new_row);
		});
		var titles=[];
		$(  "#"+self.app.control_id(dom_id)+" thead th" ).each(function(i, col){
			titles.push( $(col).html() );
		});
		return [titles, res];
	};
	this.load = function(){

		var html = 	"<div class='ControlList' title='"+help+"' >";
		html += "<div id='"+self.app.control_id(dom_id)+"' ></div>";
		html += "</div>";
		$(  "#place-"+self.app.control_id(dom_id) ).replaceWith(html);

		this.load_table( value[0], value[1] );
	};
	
};





function ControlVisVis( label, dom_id, value, help){

	this.LABEL = label;
	this.DOMID = dom_id;
	var self = this;

	this.rawValue = function(value){ return undefined; };
	this.setValue = function(value){
		var chart = $( '#'+self.app.control_id(dom_id)).data('chart');
		$( '#'+self.app.control_id(dom_id)).data('chart_data', value);

		var options = {
			data:value.data,
			legend: {
				show: value.legend.length>0,
				labels: value.legend,
				showLabels: true,
				showSwatch: true
			}
		};
		chart.replot(options);
	};
	this.getValue = function(){ 
		return $( '#'+self.app.control_id(dom_id)).data('chart_data');
	};
	this.load = function(){
		var html = 	"<div class='ControlVisVis' id='chart-container-"+self.app.control_id(dom_id)+"' title='"+help+"'   >";
		html += 	"<div id='"+self.app.control_id(dom_id)+"' ></div>";
		html += 	"</div>";
		$( "#place-"+self.app.control_id(dom_id) ).replaceWith(html);

		legend = value.legend;
		data   = value.data;

		if(data.length==0){ data = [[[0,0]]] }
		var chart = $.jqplot(self.app.control_id(dom_id), data, {
			title:this.LABEL,
			seriesDefaults:{
				showMarker:true, showLine:true, lineWidth:0.5,
				markerOptions:{ size: 6 }
			},
			legend: {
				show: legend.length>0,				
				labels: legend,
				placement: "outside",
				location: 'e'
			},
			axes:{
				xaxis:{
					renderer:$.jqplot.DateAxisRenderer, 
					labelRenderer: 	$.jqplot.CanvasAxisLabelRenderer,
					tickRenderer: 	$.jqplot.CanvasAxisTickRenderer,
					tickOptions: {angle: -45}
				}
			},
			cursor:{
				show: true, 
				zoom: true
			}
		});

		$( '#'+self.app.control_id(dom_id)).data('chart', chart);
		$( '#'+self.app.control_id(dom_id)).data('chart_data', value);

		//$("#chart-container-"+self.app.control_id(dom_id)).resizable({delay:20});
		//$("#chart-container-"+self.app.control_id(dom_id)).bind("resize", function(event, ui) {chart.replot();});

	};
	
};


////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////

$.ajaxSetup({ cache: false });
function PyFormsApp(app_name, app_id, controls){
	this.application 	= app_name;
	this.application_id = app_id;
	this.controls 		= controls;
	this.events_queue 	= [];

	for(var index = 0; index < controls.length; index++){
		controls[index].app = this;
		controls[index].load();
	}
	$('.application-tabs').tabs()
}

////////////////////////////////////////////////////////////

PyFormsApp.prototype.control_id = function(name){
	return this.application_id+'-'+name;
}

////////////////////////////////////////////////////////////

PyFormsApp.prototype.jquery_selector = function(){
	return '';//'#'+this.application_id+' ';
}

////////////////////////////////////////////////////////////

PyFormsApp.prototype.current_folder = function(){
	var currentfolder = $('#files-browser-div').dataviewer('path');
	if(currentfolder==undefined) currentfolder = '/';
	return currentfolder;
}

////////////////////////////////////////////////////////////

PyFormsApp.prototype.FireEvent = function(dom_in, event){
	data = {event: {control:dom_in, event: event}, userpath: this.current_folder() };
	this.events_queue.push(data)
	this.SendUpdateData( this.events_queue.pop(0) );
}

////////////////////////////////////////////////////////////

PyFormsApp.prototype.UpdateControls = function(){	
	this.SendUpdateData({ userpath: this.current_folder() }); 
};

////////////////////////////////////////////////////////////

PyFormsApp.prototype.SendUpdateData = function(data2send){	
	loading();
	for (index = 0; index <  this.controls.length; index++) {
		var name = this.controls[index].DOMID;
		data2send[name] =  this.controls[index].getValue();

	}

	var self = this;

	var jsondata =  $.toJSON(data2send);
	$.ajax({
		method: 'post',
		cache: false,
		dataType: "json",
		url: '/pyforms/update/'+ this.application+'/?nocache='+Math.random(),
		data: jsondata,
		contentType: "application/json; charset=utf-8",
		success: function(res){
			if( res.result=='error' ){
				error(res.msg);
			}else{
				for (index = 0; index <  self.controls.length; index++) {
					var name =  self.controls[index].DOMID;
					if(res[name])  self.controls[index].setValue( res[name] );
				}
			}
		}
	}).fail(function(xhr){
		error(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
	}).always(function(){
		not_loading();
	});
	
	if(  this.events_queue.length>0 )  this.SendUpdateData(  this.events_queue.pop(0) );
}