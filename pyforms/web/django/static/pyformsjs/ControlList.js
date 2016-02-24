

function ControlList(name, properties){
	ControlBase.call(this, name, properties);
	this.being_edited = false;
};
ControlList.prototype = Object.create(ControlBase.prototype);

////////////////////////////////////////////////////////////////////////////////

ControlList.prototype.init_control = function(){
	var html = 	"<div class='ControlList' title='"+this.properties.help+"' >";
	html += "<div id='"+this.control_id()+"' ></div>";
	html += "</div>";
	this.jquery_place().replaceWith(html);
	this.setValue( value );
};

////////////////////////////////////////////////////////////////////////////////

ControlList.prototype.get_value = function(){ 
	var res=[];
	$( "#"+this.control_id()+" tbody tr" ).each(function(i, row){
		var new_row=[]
		$(this).children('td').each(function(j, col){
			new_row.push($(col).html());
		});
		res.push(new_row);
	});
	var titles=[];
	$(  "#"+this.control_id()+" thead th" ).each(function(i, col){
		titles.push( $(col).html() );
	});

	var selected_index = $( "#"+this.control_id()+" tbody tr.selected" ).index();
	return [titles, res, this.select_entire_row, this.read_only, selected_index];
};

////////////////////////////////////////////////////////////////////////////////

ControlList.prototype.set_value = function(value){
	this.select_entire_row 	= value[2];
	this.read_only 			= value[3];
	this.load_table(value[0],value[1]);
	if(value[4]>=0){
		var selected_row = $( "#"+self.control_id()+" tbody tr:eq("+value[4]+")" );
		selected_row.addClass('selected');
		selected_row.find('td').addClass('selected');
	};
};

////////////////////////////////////////////////////////////////////////////////

ControlList.prototype.load_table = function(titles, data){
	var html = "<table id='"+this.control_id()+"' >";
	html += "<thead>";
	html += "<tr>";
	for(var i=0; i<titles.length; i++) html += "<th>"+titles[i]+"</th>";
	html += "</tr>";
	html += "</thead>";
	html += "<tbody>";
	for(var i=0; i<data.length; i++){
		html += "<tr>";
		for(var j=0; j<data[i].length; j++) html += "<td>"+data[i][j]+"</td>";
		if(data[i].length<titles.length) for(var j=data[i].length; j<titles.length; j++) html += "<td></td>";
		html += "</tr>";
	};
	html += "</tbody>";
	html += "</table>";
	html += "</div>";
	this.jquery_place().replaceWith(html);

	var self = this;
		
	if(!this.properties.read_only){
		$( "#"+this.control_id()+" tbody td" ).dblclick(function(){
			if( self.being_edited ) return false;

			self.being_edited = true;
			var cell = $(this);
			var value = cell.html();
			cell.html('<input type="text" value="'+value+'" />');
			cell.children('input').focus();
			cell.children('input').focusout(function(){
				cell.html($(this).val());
				this.being_edited = false;
				self.basewidget.fire_event( self.name, 'changed' );
			});
		});
	};

	$("#"+this.control_id()+" tbody td" ).click(function(){
		$("#"+self.control_id()+" tbody td" ).removeClass('selected');
		$("#"+self.control_id()+" tbody tr" ).removeClass('selected');			

		if( self.select_entire_row )
			$(this).parent().find('td').addClass('selected');
		else
			$(this).addClass('selected');

		$(this).parent().addClass('selected');
	});
};

////////////////////////////////////////////////////////////////////////////////
