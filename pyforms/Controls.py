from pyforms import conf

if conf.PYFORMS_MODE=='GUI':
	import logging, traceback; logger=logging.getLogger(__file__)

	from pyforms.gui.controls.ControlBase 			import ControlBase
	from pyforms.gui.controls.ControlText 			import ControlText
	from pyforms.gui.controls.ControlBoundingSlider import ControlBoundingSlider
	from pyforms.gui.controls.ControlButton 		import ControlButton
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
	from pyforms.gui.controls.ControlTree 			import ControlTree
	from pyforms.gui.controls.ControlTreeView 		import ControlTreeView
	from pyforms.gui.controls.control_event_timeline.ControlEventTimeline 	import ControlEventTimeline
	from pyforms.gui.controls.control_events_graph.ControlEventsGraph 		import ControlEventsGraph

	if conf.PYFORMS_MATPLOTLIB_ENABLED:
		try:
			from pyforms.gui.controls.ControlMatplotlib import ControlMatplotlib
		except:
			logger.warning("Matplot lib not installed or not working properly")
			logger.warning(traceback.format_exc())

	if conf.PYFORMS_WEB_ENABLED:
		try:
			from pyforms.gui.controls.ControlWeb import ControlWeb
		except:
			logger.warning("QtWebKit lib not installed or not working properly")
			logger.warning(traceback.format_exc())

	if conf.PYFORMS_GL_ENABLED:
		try:
			from pyforms.gui.controls.ControlOpenGL 				import ControlOpenGL
			from pyforms.gui.controls.ControlImage 					import ControlImage
			from pyforms.gui.controls.control_player.ControlPlayer 	import ControlPlayer
		except:
			logger.warning("GL widgets or Opencv not installed")
			logger.warning(traceback.format_exc())
	
	if conf.PYFORMS_VISVIS_ENABLED:
		try:
			from pyforms.gui.controls.ControlVisVis 		import ControlVisVis
			from pyforms.gui.controls.ControlVisVisVolume 	import ControlVisVisVolume
		except:
			logger.warning("VisVis not installed")
			logger.warning(traceback.format_exc())

	if conf.PYFORMS_QSCINTILLA_ENABLED:
		try:
			from pyforms.gui.controls.ControlCodeEditor import ControlCodeEditor
		except:
			logger.debug("QScintilla2 not installed")
			logger.debug(traceback.format_exc())


elif conf.PYFORMS_MODE=='TERMINAL':

	from pyforms.terminal.controls.ControlBase 		import ControlBase
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

	from pyforms_web.web.Controls.ControlBase 			import ControlBase
	from pyforms_web.web.Controls.ControlText 			import ControlText
	from pyforms_web.web.Controls.ControlBoundingSlider import ControlBoundingSlider
	from pyforms_web.web.Controls.ControlDate 			import ControlDate
	from pyforms_web.web.Controls.ControlButton 		import ControlButton
	from pyforms_web.web.Controls.ControlCheckBox 		import ControlCheckBox
	from pyforms_web.web.Controls.ControlCombo 			import ControlCombo
	from pyforms_web.web.Controls.ControlDir 			import ControlDir
	from pyforms_web.web.Controls.ControlFile 			import ControlFile
	from pyforms_web.web.Controls.ControlImage 			import ControlImage
	from pyforms_web.web.Controls.ControlSlider 		import ControlSlider
	from pyforms_web.web.Controls.ControlPlayer 		import ControlPlayer
	from pyforms_web.web.Controls.ControlProgress 		import ControlProgress
	from pyforms_web.web.Controls.ControlVisVis 		import ControlVisVis
	from pyforms_web.web.Controls.ControlList 			import ControlList
	from pyforms_web.web.Controls.ControlLabel 			import ControlLabel
	from pyforms_web.web.Controls.ControlTimeout 		import ControlTimeout
	from pyforms_web.web.Controls.ControlEmptyWidget 	import ControlEmptyWidget
	from pyforms_web.web.Controls.ControlWorkflow 		import ControlWorkflow
