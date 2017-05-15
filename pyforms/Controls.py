from pyforms import conf
import logging, traceback

logger = logging.getLogger(__file__)

if conf.PYFORMS_MODE in ['GUI', 'GUI-OPENCSP']:

	from pyforms.gui.Controls.ControlBase import ControlBase
	from pyforms.gui.Controls.ControlText import ControlText
	from pyforms.gui.Controls.ControlBoundingSlider import ControlBoundingSlider
	from pyforms.gui.Controls.ControlButton import ControlButton
	from pyforms.gui.Controls.ControlCheckBoxList import ControlCheckBoxList
	from pyforms.gui.Controls.ControlCheckBox import ControlCheckBox
	from pyforms.gui.Controls.ControlCombo import ControlCombo
	from pyforms.gui.Controls.ControlDir import ControlDir
	from pyforms.gui.Controls.ControlDockWidget import ControlDockWidget
	from pyforms.gui.Controls.ControlEmptyWidget import ControlEmptyWidget
	from pyforms.gui.Controls.ControlFile import ControlFile
	from pyforms.gui.Controls.ControlFilesTree import ControlFilesTree
	from pyforms.gui.Controls.ControlLabel import ControlLabel
	from pyforms.gui.Controls.ControlList import ControlList
	from pyforms.gui.Controls.ControlMdiArea import ControlMdiArea
	from pyforms.gui.Controls.ControlNumber import ControlNumber

	if conf.PYFORMS_MATPLOTLIB_ENABLED:
		try:
			from pyforms.gui.Controls.ControlMatplotlib import ControlMatplotlib
		except:
			logger.warning("Matplot lib not installed or not working properly")
			logger.warning(traceback.format_exc())

	if conf.PYFORMS_WEB_ENABLED:
		try:
			from pyforms.gui.Controls.ControlWeb import ControlWeb
		except:
			logger.warning("QtWebKit lib not installed or not working properly")
			logger.warning(traceback.format_exc())

	if conf.PYFORMS_GL_ENABLED:
		try:
			from pyforms.gui.Controls.ControlOpenGL import ControlOpenGL
			from pyforms.gui.Controls.ControlImage import ControlImage
			from pyforms.gui.Controls.ControlPlayer.ControlPlayer import ControlPlayer
		except:
			logger.warning("GL widgets or Opencv not installed")
			logger.warning(traceback.format_exc())

	from pyforms.gui.Controls.ControlProgress import ControlProgress
	from pyforms.gui.Controls.ControlSlider import ControlSlider
	from pyforms.gui.Controls.ControlTextArea import ControlTextArea
	from pyforms.gui.Controls.ControlToolBox import ControlToolBox
	from pyforms.gui.Controls.ControlTree import ControlTree
	from pyforms.gui.Controls.ControlTreeView import ControlTreeView

	if conf.PYFORMS_VISVIS_ENABLED:
		try:
			from pyforms.gui.Controls.ControlVisVis import ControlVisVis
			from pyforms.gui.Controls.ControlVisVisVolume import ControlVisVisVolume
		except:
			logger.warning("VisVis not installed")
			logger.warning(traceback.format_exc())

	from pyforms.gui.Controls.ControlEventTimeline.ControlEventTimeline import ControlEventTimeline
	from pyforms.gui.Controls.ControlEventsGraph.ControlEventsGraph import ControlEventsGraph

	try:
		from pyforms.gui.Controls.ControlCodeEditor import ControlCodeEditor
	except:
		logger.debug("QScintilla2 not installed")
		logger.debug(traceback.format_exc())


elif conf.PYFORMS_MODE in ['TERMINAL']:

	from pyforms.terminal.Controls.ControlBase import ControlBase
	from pyforms.terminal.Controls.ControlText import ControlText
	from pyforms.terminal.Controls.ControlButton import ControlButton
	from pyforms.terminal.Controls.ControlCheckBox import ControlCheckBox
	from pyforms.terminal.Controls.ControlCombo import ControlCombo
	from pyforms.terminal.Controls.ControlFile import ControlFile
	from pyforms.terminal.Controls.ControlDir import ControlDir
	from pyforms.terminal.Controls.ControlImage import ControlImage
	from pyforms.terminal.Controls.ControlSlider import ControlSlider
	from pyforms.terminal.Controls.ControlPlayer import ControlPlayer
	from pyforms.terminal.Controls.ControlNumber import ControlNumber
	from pyforms.terminal.Controls.ControlProgress import ControlProgress

elif conf.PYFORMS_MODE in ['WEB']:

	from pyforms_web.web.Controls.ControlBase import ControlBase
	from pyforms_web.web.Controls.ControlText import ControlText
	from pyforms_web.web.Controls.ControlBoundingSlider import ControlBoundingSlider
	from pyforms_web.web.Controls.ControlDate import ControlDate
	from pyforms_web.web.Controls.ControlButton import ControlButton
	from pyforms_web.web.Controls.ControlCheckBox import ControlCheckBox
	from pyforms_web.web.Controls.ControlCombo import ControlCombo
	from pyforms_web.web.Controls.ControlDir import ControlDir
	from pyforms_web.web.Controls.ControlFile import ControlFile
	from pyforms_web.web.Controls.ControlImage import ControlImage
	from pyforms_web.web.Controls.ControlSlider import ControlSlider
	from pyforms_web.web.Controls.ControlPlayer import ControlPlayer
	from pyforms_web.web.Controls.ControlProgress import ControlProgress
	from pyforms_web.web.Controls.ControlVisVis import ControlVisVis
	from pyforms_web.web.Controls.ControlList import ControlList
	from pyforms_web.web.Controls.ControlLabel import ControlLabel
	from pyforms_web.web.Controls.ControlTimeout import ControlTimeout
	from pyforms_web.web.Controls.ControlEmptyWidget import ControlEmptyWidget
	from pyforms_web.web.Controls.ControlWorkflow import ControlWorkflow
