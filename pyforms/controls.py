from confapp import conf

if conf.PYFORMS_MODE=='GUI':
	import logging, traceback; logger=logging.getLogger(__file__)

	from pyforms.gui.controls.ControlBase 			import ControlBase
	from pyforms.gui.controls.ControlText 			import ControlText
	from pyforms.gui.controls.ControlBoundingSlider import ControlBoundingSlider
	from pyforms.gui.controls.ControlButton 		import ControlButton
	from pyforms.gui.controls.ControlToolButton 	import ControlToolButton
	from pyforms.gui.controls.ControlCheckBoxList 	import ControlCheckBoxList
	from pyforms.gui.controls.ControlCheckBox 		import ControlCheckBox
	from pyforms.gui.controls.ControlCombo 			import ControlCombo
	from pyforms.gui.controls.ControlDir 			import ControlDir
	from pyforms.gui.controls.ControlDockWidget 	import ControlDockWidget
	from pyforms.gui.controls.ControlEmptyWidget 	import ControlEmptyWidget
	from pyforms.gui.controls.ControlFile 			import ControlFile
	from pyforms.gui.controls.ControlFilesTree 		import ControlFilesTree
	from pyforms.gui.controls.ControlLabel 			import ControlLabel
	from pyforms.gui.controls.ControlList 			import ControlList
	from pyforms.gui.controls.ControlMdiArea 		import ControlMdiArea
	from pyforms.gui.controls.ControlNumber 		import ControlNumber
	from pyforms.gui.controls.ControlProgress 		import ControlProgress
	from pyforms.gui.controls.ControlSlider 		import ControlSlider
	from pyforms.gui.controls.ControlTextArea 		import ControlTextArea
	from pyforms.gui.controls.ControlToolBox 		import ControlToolBox
	from pyforms.gui.controls.ControlTableView 		import ControlTableView
	from pyforms.gui.controls.ControlTree 			import ControlTree
	from pyforms.gui.controls.ControlTreeView 		import ControlTreeView
	from pyforms.gui.controls.control_event_timeline.ControlEventTimeline 	import ControlEventTimeline
	from pyforms.gui.controls.control_events_graph.ControlEventsGraph 		import ControlEventsGraph

	if conf.PYFORMS_MATPLOTLIB_ENABLED:
		try:
			from pyforms.gui.controls.ControlMatplotlib import ControlMatplotlib
		except Exception as e:
			logger.warning("Matplot lib not installed or not working properly")
			logger.error(e, exc_info=True)

	if conf.PYFORMS_WEB_ENABLED:
		try:
			from pyforms.gui.controls.ControlWeb import ControlWeb
		except Exception as e:
			logger.warning("QtWebKit lib not installed or not working properly")
			logger.error(e, exc_info=True)

	if conf.PYFORMS_GL_ENABLED:
		try:
			from pyforms.gui.controls.ControlOpenGL 				import ControlOpenGL
			from pyforms.gui.controls.ControlImage 					import ControlImage
			from pyforms.gui.controls.control_player.ControlPlayer 	import ControlPlayer
		except Exception as e:
			logger.warning("GL widgets or Opencv is not installed")
			logger.error(e, exc_info=True)
	
	if conf.PYFORMS_VISVIS_ENABLED:
		try:
			from pyforms.gui.controls.ControlVisVis 		import ControlVisVis
			from pyforms.gui.controls.ControlVisVisVolume 	import ControlVisVisVolume
		except Exception as e:
			logger.warning("VisVis not installed")
			logger.error(e, exc_info=True)

	if conf.PYFORMS_QSCINTILLA_ENABLED:
		try:
			from pyforms.gui.controls.ControlCodeEditor import ControlCodeEditor
		except Exception as e:
			logger.warning("QScintilla2 not installed")
			logger.error(e, exc_info=True)

	
elif conf.PYFORMS_MODE=='TERMINAL':

	from pyforms.terminal.controls.ControlBase 		import ControlBase
	from pyforms.terminal.controls.ControlBoundingSlider 	import ControlBoundingSlider
	from pyforms.terminal.controls.ControlText 		import ControlText
	from pyforms.terminal.controls.ControlButton 	import ControlButton
	from pyforms.terminal.controls.ControlCheckBox 	import ControlCheckBox
	from pyforms.terminal.controls.ControlCombo		import ControlCombo
	from pyforms.terminal.controls.ControlFile 		import ControlFile
	from pyforms.terminal.controls.ControlDir 		import ControlDir
	from pyforms.terminal.controls.ControlImage 	import ControlImage
	from pyforms.terminal.controls.ControlSlider 	import ControlSlider
	from pyforms.terminal.controls.ControlPlayer 	import ControlPlayer
	from pyforms.terminal.controls.ControlNumber 	import ControlNumber
	from pyforms.terminal.controls.ControlProgress 	import ControlProgress

elif conf.PYFORMS_MODE=='WEB':

	from pyforms_web.controls.control_base                   import ControlBase
	from pyforms_web.controls.control_autocomplete           import ControlAutoComplete
	from pyforms_web.controls.control_boundingslider         import ControlBoundingSlider
	from pyforms_web.controls.control_breadcrumb             import ControlBreadcrumb
	from pyforms_web.controls.control_button                 import ControlButton
	from pyforms_web.controls.control_calendar               import ControlCalendar
	from pyforms_web.controls.control_checkboxlist           import ControlCheckBoxList
	from pyforms_web.controls.control_checkboxlistquery      import ControlCheckBoxListQuery
	from pyforms_web.controls.control_checkbox               import ControlCheckBox
	from pyforms_web.controls.control_combo                  import ControlCombo
	from pyforms_web.controls.control_date                   import ControlDate
	from pyforms_web.controls.control_datetime               import ControlDateTime
	from pyforms_web.controls.control_dir                    import ControlDir
	from pyforms_web.controls.control_email                  import ControlEmail
	from pyforms_web.controls.control_emptywidget            import ControlEmptyWidget
	from pyforms_web.controls.control_feed                   import ControlFeed
	from pyforms_web.controls.control_file                   import ControlFile
	from pyforms_web.controls.control_fileupload             import ControlFileUpload
	from pyforms_web.controls.control_float                  import ControlFloat
	from pyforms_web.controls.control_html                   import ControlHtml
	from pyforms_web.controls.control_image                  import ControlImage
	from pyforms_web.controls.control_integer                import ControlInteger
	from pyforms_web.controls.control_itemslist              import ControlItemsList
	from pyforms_web.controls.control_label                  import ControlLabel
	from pyforms_web.controls.control_list                   import ControlList
	from pyforms_web.controls.control_menu                   import ControlMenu
	from pyforms_web.controls.control_multiplechecks         import ControlMultipleChecks
	from pyforms_web.controls.control_multipleselection      import ControlMultipleSelection
	from pyforms_web.controls.control_multipleselectionquery import ControlMultipleSelectionQuery
	from pyforms_web.controls.control_password               import ControlPassword
	from pyforms_web.controls.control_piechart               import ControlPieChart
	from pyforms_web.controls.control_player                 import ControlPlayer
	from pyforms_web.controls.control_progress               import ControlProgress
	from pyforms_web.controls.control_querycards             import ControlQueryCards
	from pyforms_web.controls.control_querycombo             import ControlQueryCombo
	from pyforms_web.controls.control_queryitem              import ControlQueryItem
	from pyforms_web.controls.control_querylist              import ControlQueryList
	from pyforms_web.controls.control_slider                 import ControlSlider
	from pyforms_web.controls.control_template               import ControlTemplate
	from pyforms_web.controls.control_textarea               import ControlTextArea
	from pyforms_web.controls.control_text                   import ControlText
	from pyforms_web.controls.control_timeout                import ControlTimeout
	from pyforms_web.controls.control_visvis                 import ControlVisVis
	from pyforms_web.controls.control_workflow               import ControlWorkflow
