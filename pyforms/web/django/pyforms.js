function sleep(ms) {
	var unixtime_ms = new Date().getTime();
	while(new Date().getTime() < unixtime_ms + ms) {}
}

function ControlButton( label, dom_id, help ){

	this.LABEL = label;
	this.DOMID = dom_id;
	
	this.rawValue = function(value){};
	this.setValue = function(value){};
	this.getValue = function(){};
	this.load = function(){
		var html = "<div class='ControlButton' >";
		html +="<button title='"+help+"'  value='"+this.LABEL+"' id='"+dom_id+"' class='btn' >";
		html += '<i class="glyphicon glyphicon-cog"></i> '+ this.LABEL;
		html += '</button>';
		html += '</div>';
		$( "#place"+this.DOMID ).html(html);

		$( "#"+this.DOMID ).click(function(){
			FireEvent( dom_id, 'pressed' )
		});
	};
	
};


function ControlCheckBox( label, dom_id, value, help ){

	this.LABEL = label;
	this.DOMID = dom_id;
	var self = this;

	this.rawValue = function(value){ return $( "#"+this.DOMID ).is(':checked'); };
	this.setValue = function(value){ $( "#"+this.DOMID ).prop('checked', value);};
	this.getValue = function(){ return $( "#"+this.DOMID ).is(':checked'); };
	this.load = function(){
		$( "#place"+this.DOMID ).replaceWith("<div title='"+help+"' class='ControlText' ><label for='"+this.DOMID+"'>"+this.LABEL+"</label><input class='textfield' type='checkbox' name='"+dom_id+"' id='"+dom_id+"' value='true' /></div>");
		$( "#"+this.DOMID ).click(function(){ FireEvent( dom_id, 'changed' ); });

		if( value=='True') $("#"+this.DOMID ).prop('checked', true);
	};
	
};




function ControlCombo( label, dom_id, values, help ){

	this.LABEL = label;
	this.DOMID = dom_id;
	this.VALUES = values;
	
	this.rawValue = function(value){return $( "#"+this.DOMID ).val();};
	this.setValue = function(value){$( "#"+this.DOMID ).val(value)};
	this.getValue = function(){return $( "#"+this.DOMID ).val();};
	this.load = function(){
		$( "#place"+this.DOMID ).replaceWith("<div title='"+help+"'   class='ControlText' ><label title='"+help+"'  for='"+this.DOMID+"'>"+this.LABEL+"</label><select type='button' id='"+dom_id+"' ></select></div>")
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


function selectFile2Control(dom_id, filename){
	$("#dialog"+dom_id ).dialog('destroy');
	$( "#"+dom_id).val(filename);
	FireEvent( dom_id, 'changed' )
}

function FileRowEvent(row, dom){
	var dom_id = $(dom).attr('dom-id');
	row.values[0] = "<a class='file2select' href='javascript:selectFile2Control(\""+dom_id+"\",\""+row.file+"\")' >"+row.filename+"</a>";
	row.values.pop();
	return row;
}

function ControlDir( label, dom_id, value, help ){
	this.LABEL = label;
	this.DOMID = dom_id;
	var self = this;

	this.setValue = function(value){
		$( "#"+this.DOMID ).val(value)
	};
	this.getValue = function(){ return $( "#"+this.DOMID ).val(); };
	this.rawValue = function(value){ return $( "#"+this.DOMID ).val(); };
	this.load = function(){
		var html = "<div class='ControlFile' ><label for='"+this.DOMID+"' title='"+help+"' >"+this.LABEL+"</label>";
		html += "<input type='text' class='filename' name='"+dom_id+"' id='"+dom_id+"' value='"+value+"' />";
		//html += "<input class='choose-file-button' type='image' src='/static/upload.png' id='button"+dom_id+"' />";
		html += '<button id="button'+dom_id+'" class="btn "><i class="glyphicon glyphicon-folder-open icon-white"></i></button>';
		html += "<div id='dialog"+this.DOMID+"' dom-id='"+this.DOMID+"' class='dialog' style='display:none;' title='Pick a file'></div>";
		
		function reloadFolder(){
			var folder = $('#files-browser-div').dataviewer('path');
			if(folder==undefined) folder = '/';
			$("#dialog"+self.DOMID).dataviewer( {url: '/browsefiles/?backfolder=false&p='+folder, path:folder } );
			$("#dialog"+self.DOMID).dataviewer();
		}
		
		$("#place"+this.DOMID ).replaceWith(html);
		$("#dialog"+this.DOMID).dataviewer({ 
			titles: ['File name','Size', 'Created on',''],
			sizes: 	['auto','120px','220px','50px'],
			sortingColumns: [0,1,2],
			updateRowFunction: FileRowEvent,
			extra_buttons: [{
				btnId:'reload-folder', 
				btnLabel:'Reload', 
				btnAction: reloadFolder
			}]
		});

		$( "#button"+this.DOMID ).unbind('click');
		$( "#button"+this.DOMID ).click(function(){
			$("#dialog"+dom_id ).dialog({ show: 'slideDown',width: 900, height: 600, position: { at: "top" }, draggable: false });
			reloadFolder();
		});
	};
	
};


function ControlFile( label, dom_id, value, help ){
	this.LABEL = label;
	this.DOMID = dom_id;
	var self = this;

	this.setValue = function(value){
		$( "#"+this.DOMID ).val(value)
	};
	this.getValue = function(){ return $( "#"+this.DOMID ).val(); };
	this.rawValue = function(value){ return $( "#"+this.DOMID ).val(); };
	this.load = function(){
		var html = "<div class='ControlFile' ><label for='"+this.DOMID+"' title='"+help+"' >"+this.LABEL+"</label>";
		html += "<input type='text' class='filename' name='"+dom_id+"' id='"+dom_id+"' value='"+value+"' />";
		//html += "<input class='choose-file-button' type='image' src='/static/upload.png' id='button"+dom_id+"' />";
		html += '<button id="button'+dom_id+'" class="btn "><i class="glyphicon glyphicon-folder-open icon-white"></i></button>';
		html += "<div id='dialog"+this.DOMID+"' dom-id='"+this.DOMID+"' class='dialog' style='display:none;' title='Pick a file'></div>";
		
		function reloadFolder(){
			var folder = $('#files-browser-div').dataviewer('path');
			if(folder==undefined) folder = '/';
			$("#dialog"+self.DOMID).dataviewer( {url: '/browsefiles/?backfolder=false&p='+folder, path:folder } );
			$("#dialog"+self.DOMID).dataviewer();
		}
		
		$("#place"+this.DOMID ).replaceWith(html);
		$("#dialog"+this.DOMID).dataviewer({ 
			titles: ['File name','Size', 'Created on',''],
			sizes: 	['auto','120px','220px','50px'],
			sortingColumns: [0,1,2],
			updateRowFunction: FileRowEvent,
			extra_buttons: [{
				btnId:'reload-folder', 
				btnLabel:'Reload', 
				btnAction: reloadFolder
			}]
		});

		$( "#button"+this.DOMID ).unbind('click');
		$( "#button"+this.DOMID ).click(function(){
			$("#dialog"+dom_id ).dialog({ show: 'slideDown',width: 900, height: 600, position: { at: "top" }, draggable: false });
			reloadFolder();
		});
	};
	
};

function ControlImage( dom_id , help ){

	this.DOMID = dom_id;
	this.FILENAME = '';
	
	this.rawValue = function(value){ return $( "#"+this.DOMID ).attr('src'); };
	this.setValue = function(value){
		$("#"+this.DOMID + " .image" ).attr("src", "data:image/png;base64,"+value.image);
		this.FILENAME   = value.filename;
	};
	this.getValue = function(){
		return { filename: this.FILENAME }
	};
	this.load = function(){
		var html = "<div class='ControlImage' >";
		html += "<img style='width:100%;' class='image' src='' id='"+this.DOMID+"' />";
		html += "</div>";
		$( "#place"+this.DOMID ).replaceWith(html);
		
	};
	
};

function ControlPlayer( dom_id, help ){
	this.DOMID = dom_id;
	this.FILENAME = '';
	
	this.rawValue = function(value){};
	this.setValue = function(value){
		$( "#timeline"+this.DOMID ).slider({min: value.min, max: value.max, value: value.position});
		this.FILENAME = value.filename;
		$("#display"+this.DOMID ).attr("src", "data:image/png;base64,"+value.frame);
	};
	this.getValue = function(){
		var pos = $( "#timeline"+this.DOMID ).slider("value");
		var res = { position: pos, filename: this.FILENAME };
		return res;
	};
	this.load = function(){
		var html = "<div class='ControlPlayer' >";
		html += "<img style='width:100%;' class='image' src=' ' id='display"+this.DOMID+"' />";
		html += "<div class='slider' name='"+this.DOMID+"' id='timeline"+this.DOMID+"' ></div>";
		html += "</div>";
		$( "#place"+this.DOMID ).replaceWith(html);
		$( "#timeline"+this.DOMID ).slider( {stop: UpdateControls });
	};
	
};

function ControlProgress( dom_id , help ){

	this.DOMID = dom_id;
	
	this.rawValue = function(value){};
	this.setValue = function(value){};
	this.getValue = function(){};
	this.load = function(){
		$( "#place"+this.DOMID ).replaceWith("<div title='"+help+"'   id='"+this.DOMID+"' class='progressbar' ></div>");
	};	
};

function ControlSlider( label, dom_id, value, min, max, help  ){

	this.LABEL = label;
	this.DOMID = dom_id;
	this.VALUE = value
	this.MIN = min;
	this.MAX = max;
	
	this.setValue = function(val){
		$( "#"+this.DOMID ).slider({value:val})
		$( "#value"+dom_id ).html(  val );
	};
	this.getValue = function(){
		return { position: $( "#"+this.DOMID ).slider("value") }
	};
	this.rawValue = function(value){ return $( "#"+this.DOMID ).slider("value")  };
	this.load = function(){
		var html = 	"<div class='ControlSlider' title='"+help+"'   >";
		html += 	"<label style='margin-right: 20px;' for='"+this.DOMID+"'>"+this.LABEL+": <small id='value"+this.DOMID+"' style='color:red' >"+this.VALUE+"</small></label>";
		html += 	"<div class='slider' name='"+this.DOMID+"' id='"+this.DOMID+"' ></div>";
		html += 	"</div>";
		$( "#place"+this.DOMID ).replaceWith(html);
		$( "#"+this.DOMID ).slider({ 
			slide: function( event, ui ) {
				$( "#value"+dom_id ).html(  ui.value );
			},
			stop: function(){ FireEvent( dom_id, 'changed' )}, min: this.MIN, max: this.MAX,  value: this.VALUE });
	};
	
};


function ControlBoundingSlider( label, dom_id, value, min, max, horizontal, help  ){

	this.LABEL = label;
	this.DOMID = dom_id;
	this.VALUE = value;
	this.MIN = min;
	this.MAX = max;
	
	this.setValue = function(val){
		$( "#"+this.DOMID ).slider({values:val})
		$( "#value"+dom_id ).html(  val );
	};
	this.getValue = function(){
		return { position: $( "#"+this.DOMID ).slider("values") }
	};
	this.rawValue = function(value){ return $( "#"+this.DOMID ).slider("values")  };
	this.load = function(){
		var html = 	"<div class='ControlSlider' title='"+help+"'   >";
		html += 	"<label style='margin-right: 20px;' for='"+this.DOMID+"'>"+this.LABEL+": <small id='value"+this.DOMID+"' style='color:red' >"+this.VALUE+"</small></label>";
		html += 	"<div class='slider' name='"+this.DOMID+"' id='"+this.DOMID+"' ></div>";
		html += 	"</div>";
		$( "#place"+this.DOMID ).replaceWith(html);
		$( "#"+this.DOMID ).slider({ 
			range: true,
			slide: function( event, ui ) {
				$( "#value"+dom_id ).html(  ui.value );
			},
			stop: function(){ FireEvent( dom_id, 'changed' )}, 
			min: this.MIN, max: this.MAX, values: this.VALUE });
	};
	
};

function ControlText( label, dom_id, value, help ){

	this.LABEL = label;
	this.DOMID = dom_id;

	this.rawValue = function(value){ return $( "#"+this.DOMID ).val(); };
	this.setValue = function(value){
		$( "#"+this.DOMID ).val(value)
	};
	this.getValue = function(){ return $( "#"+this.DOMID ).val(); };
	this.load = function(){
		if(!value) value = '';
		$( "#place"+this.DOMID ).replaceWith("<div title='"+help+"'   class='ControlText' ><label for='"+this.DOMID+"'>"+this.LABEL+"</label><input class='textfield' type='text' name='"+dom_id+"' id='"+dom_id+"' value=\""+value+"\" /></div>");

		$( "#"+this.DOMID ).change(function(){
			FireEvent( dom_id, 'changed' );
		});
	};
	
};

function ControlDate( label, dom_id, value, help ){

	this.LABEL = label;
	this.DOMID = dom_id;

	this.rawValue = function(value){ return $( "#"+this.DOMID ).val(); };
	this.setValue = function(value){
		$( "#"+this.DOMID ).val(value)
	};
	this.getValue = function(){ return $( "#"+this.DOMID ).val(); };
	this.load = function(){
		if(!value) value = '';
		$( "#place"+this.DOMID ).replaceWith("<div title='"+help+"' class='ControlDate' ><label for='"+this.DOMID+"'>"+this.LABEL+"</label><input class='textfield' type='text' name='"+dom_id+"' id='"+dom_id+"' value=\""+value+"\" /></div>");

		$( "#"+this.DOMID ).datepicker({dateFormat: "yy-mm-dd"});

		$( "#"+this.DOMID ).change(function(){
			FireEvent( dom_id, 'changed' );
		});
	};
	
};

function ControlList( label, dom_id, value, help ){

	this.LABEL = label;
	this.DOMID = dom_id;
	var being_edited = false;


	this.load_table = function(titles, data){
		var html = "<table id='"+this.DOMID+"' >";
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
		$( "#"+this.DOMID ).replaceWith(html);

		$( "#"+this.DOMID+" tbody td" ).dblclick(function(){
			if( being_edited ) return false;

			being_edited = true;
			var cell = $(this);
			var value = cell.html();
			cell.html('<input type="text" value="'+value+'" />');
			cell.children('input').focus();
			cell.children('input').focusout(function(){
				cell.html($(this).val());
				being_edited = false;
				FireEvent( dom_id, 'changed' );
			});
		});
	};

	this.rawValue = function(value){ return undefined; };
	this.setValue = function(value){ this.load_table(value[0],value[1]); };
	this.getValue = function(){ 
		var res=[];
		$( "#"+this.DOMID+" tbody tr" ).each(function(i, row){
			var new_row=[]
			$(this).children('td').each(function(j, col){
				new_row.push($(col).html());
			});
			res.push(new_row);
		});
		var titles=[];
		$( "#"+this.DOMID+" thead th" ).each(function(i, col){
			titles.push( $(col).html() );
		});
		return [titles, res];
	};
	this.load = function(){

		var html = 	"<div class='ControlList' title='"+help+"' >";
		html += "<div id='"+this.DOMID+"' ></div>";
		html += "</div>";
		$( "#place"+this.DOMID ).replaceWith(html);

		this.load_table( value[0], value[1] );
	};
	
};





function ControlVisVis( label, dom_id, value, help){

	this.LABEL = label;
	this.DOMID = dom_id;

	this.rawValue = function(value){ return undefined; };
	this.setValue = function(value){
		var chart = $('#'+this.DOMID).data('chart');
		$('#'+this.DOMID).data('chart_data', value);

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
		return $('#'+this.DOMID).data('chart_data');
	};
	this.load = function(){
		var html = 	"<div class='ControlVisVis' id='chart-container-"+this.DOMID+"' title='"+help+"'   >";
		html += 	"<div id='"+this.DOMID+"' ></div>";
		html += 	"</div>";
		$( "#place"+this.DOMID ).replaceWith(html);

		legend = value.legend;
		data   = value.data;

		if(data.length==0){ data = [[[0,0]]] }
		var chart = $.jqplot(this.DOMID, data, {
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

		$('#'+this.DOMID).data('chart', chart);
		$('#'+this.DOMID).data('chart_data', value);

		//$("#chart-container-"+this.DOMID).resizable({delay:20});
		//$("#chart-container-"+this.DOMID).bind("resize", function(event, ui) {chart.replot();});

	};
	
};


////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////

var pyforms_events_queue = [];

function FireEvent(dom_in, event){
	var currentfolder = $('#files-browser-div').dataviewer('path');
	if(currentfolder==undefined) currentfolder = '/';
	
	data = {event: {control:dom_in, event: event}, userpath: currentfolder};
	pyforms_events_queue.push(data)
	//SendUpdateData(data);

	SendUpdateData( pyforms_events_queue.pop(0) );
}

function UpdateControls(){	
	var currentfolder = $('#files-browser-div').dataviewer('path');
	if(currentfolder==undefined) currentfolder = '/';
	
	SendUpdateData({ userpath: currentfolder }); 
};

function SendUpdateData(data2send){	
	loading();
	for (index = 0; index < controls.length; index++) {
		var name = controls[index].DOMID;
		data2send[name] = controls[index].getValue();

	}

	var jsondata =  $.toJSON( data2send);
	$.ajax({
		method: 'post',
		cache: false,
		dataType: "json",
		url: '/pyforms/update/'+APPLICATION+'/?nocache='+Math.random(),
		data: jsondata,
		contentType: "application/json; charset=utf-8",
		success: function(res){
			if( res.result=='error' ){
				error(res.msg);
			}else{
				for (index = 0; index < controls.length; index++) {
					var name = controls[index].DOMID;
					if(res[name]) controls[index].setValue( res[name] );
				}
			}
		}
	}).fail(function(xhr){
		error(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
	}).always(function(){
		not_loading();
	});
	
	if( pyforms_events_queue.length>0 ) SendUpdateData( pyforms_events_queue.pop(0) );
}