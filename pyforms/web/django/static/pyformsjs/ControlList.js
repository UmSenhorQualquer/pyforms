

function ControlList(name, properties){
	ControlBase.call(this, name, properties);
	this.being_edited = false;
};
ControlList.prototype = Object.create(ControlBase.prototype);

////////////////////////////////////////////////////////////////////////////////

ControlList.prototype.init_control = function(){
	this.set_value(this.properties.value);
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
	return res
};


////////////////////////////////////////////////////////////////////////////////

ControlList.prototype.set_value = function(value){
	this.load_table();
};

////////////////////////////////////////////////////////////////////////////////

ControlList.prototype.load_table = function(){
	var html = "<div id='"+this.place_id()+"' class='field'><table class='ui selectable celled table ControlList' id='"+this.control_id()+"' >";
	html += "<thead>";
	html += "<tr>";
	var titles = this.properties.horizontal_headers;
	for(var i=0; i<titles.length; i++) html += "<th>"+titles[i]+"</th>";
	html += "</tr>";
	html += "</thead>";
	html += "<tbody>";
	var data = this.properties.value;
	
	for(var i=0; i<data.length; i++){
		var selected = this.properties.selected_index==i;

		html += selected?"<tr class='selected' >":"<tr>";
		var length = 0;
		if(data[i]) length = data[i].length;
		for(var j=0; j<length; j++) 
			html += selected?"<td class='selected' >"+data[i][j]+"</td>":"<td>"+data[i][j]+"</td>";
		if(length<titles.length) 
			for(var j=length; j<titles.length; j++) 
				html += selected?"<td class='selected' ></td>":"<td></td>";
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
			cell.html('<div class="ui input"><input type="text" value="'+value+'" /></div>');
			cell.find('input').focus();
			cell.find('input').focusout(function(){
				cell.html($(this).val());
				self.being_edited = false;
				self.basewidget.fire_event( self.name, 'changed' );
			});
		});
	};

	$("#"+this.control_id()+" tbody td" ).click(function(){
		if( !$(this).hasClass('selected') ){
			$("#"+self.control_id()+" tbody td" ).removeClass('selected');
			$("#"+self.control_id()+" tbody tr" ).removeClass('selected');			

			if( self.properties.select_entire_row )
				$(this).parent().find('td').addClass('selected');
			else
				$(this).addClass('selected');

			$(this).parent().addClass('selected');

			self.properties.selected_index = $("#"+self.control_id()+" tbody tr" ).index($(this).parent());

			self.basewidget.fire_event( self.name, 'itemSelectionChanged' );
		}
	});
};

////////////////////////////////////////////////////////////////////////////////


