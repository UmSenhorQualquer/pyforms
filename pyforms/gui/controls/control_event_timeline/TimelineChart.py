# !/usr/bin/python
# -*- coding: utf-8 -*-
from AnyQt.QtGui import QColor


class TimelineChart(object):
	"""
	"""

	def __init__(self, timeLineWidget, color=QColor(255, 0, 0), name='undefined'):
		"""		
		:param timeLineWidget: 
		:param color: 
		:param name: 
		"""
		self._data 		= []
		self._graph_max = None
		self._graph_min = None
		self._widget 	= timeLineWidget
		self._color 	= color
		self._zoom 		= 1.0
		self._top 		= 0
		self._name 		= name

		timeLineWidget += self

	def __unicode__(self): return self._name
	def __str__(self):     return self._name

	def __len__(self): 					 return len(self._data)
	def __getitem__(self, index): 		 return self._data[index] if index<len(self) else None
	def __setitem__(self, index, value): 
		if index >= len(self):
			for i in range(len(self), index + 1): self._data.append(None)

		if value is not None:
			if value > self._graph_max: self._graph_max = value
			if value < self._graph_min: self._graph_min = value
			

		if index is None or value is None: 
			self._data[index] = None
		else:
			self._data[index] = value
	
	
	def import_data(self, data):
		"""
		
		:param data: 
		:return: 
		"""
		self._graph_max = 0
		self._graph_min = 100000000000
		self._data 		= []
		for x, y in data:
			self[int(round(x))] = y

	def import_csv(self, csvfileobject):
		"""
		
		:param csvfileobject: 
		:return: 
		"""
		self.import_data([map(float, row) for row in csvfileobject])

	#####################################################################################
	###### PROPERTIES ###################################################################
	#####################################################################################

	@property
	def graph_min(self):
		return self._graph_min

	@graph_min.setter
	def graph_min(self, value):
		self._graph_min = value

	@property
	def graph_max(self):
		return self._graph_max

	@graph_max.setter
	def graph_max(self, value):
		self._graph_max = value

	@property
	def zoom(self):
		return self._zoom

	@zoom.setter
	def zoom(self, value):
		self._zoom = value

	@property
	def top(self):
		return self._top

	@top.setter
	def top(self, value):
		self._top = value

	#####################################################################################
	#####################################################################################
	#####################################################################################

	def draw(self, painter, left, right, top, bottom):
		"""
		
		:param painter: 
		:param left: 
		:param right: 
		:param top: 
		:param bottom: 
		:return: 
		"""
		painter.setPen(self._color)
		painter.setOpacity(0.7)

		fov_height 	 = (bottom - top) * self.zoom  #calculate the height visible 
		start 		 = self._widget.x2frame(left)  #calculate the start frame to draw
		end 		 = self._widget.x2frame(right) #calculate the end frame to draw
		end 		 = len(self) if end > len(self) else end #check if the end frame his higher than the available data
		diff_max_min = (self._graph_max - self._graph_min) #calculate the difference bettween the lower and higher value

		top = (-self._graph_min if self._graph_min > 0 else abs(self._graph_min)) * self._zoom

		if diff_max_min <= 0: diff_max_min = 1

		last_coordenate   = None
		last_real_x_coord = None

		for i, y in enumerate(self._data[start:end]):
			if y is not None:
				x = i + start
				if y == None: continue
				y = self._top + ((top + y) * fov_height) // diff_max_min
				if last_coordenate:
					diff_frames = abs(x - last_real_x_coord)
					draw_from_coord = last_coordenate if diff_frames == 1 else (self._widget.frame2x(x), fov_height - y)
					painter.drawLine(draw_from_coord[0], draw_from_coord[1], self._widget.frame2x(x), fov_height - y)

				last_coordenate = self._widget.frame2x(x), fov_height - y
				last_real_x_coord = x

		painter.setOpacity(1.0)

	@property
	def name(self): return self._name

	@name.setter
	def name(self, value):
		self._name = value

		i = self._widget.graphs.index(self)
		self._widget.rename_graph(i, value)
		

	def mouse_move_evt(self, event, top, bottom):
		"""
		:param event: 
		:param top: 
		:param bottom: 
		:return: 
		"""

		frame 			= self._widget.x2frame(event.x())
		fov_height 		= (bottom - top) * self._zoom
		top 			= (-self._graph_min if self._graph_min > 0 else abs(self._graph_min)) * self._zoom
		diff_max_min 	= (self._graph_max - self._graph_min)
		if diff_max_min <= 0: diff_max_min = 1

		# no value
		if self[frame] is None: 
			self._widget.graphs_properties.coordenate_text = None
		else:
			self._widget.graphs_properties.coordenate_text = "Frame: {0} Value: {1}".format(frame, self[frame])


	def export_2_file(self, filename):
		"""
		
		:param filename: 
		:return: 
		"""
		with open(filename, 'w') as outfile:
			outfile.write(';'.join(['frame', 'value']) + '\n')
			for x, y in enumerate(self._data):
				if y is not None: outfile.write(';'.join([str(x), str(y)]) + '\n')
