from pyforms.basewidget import BaseWidget
from pyforms.controls   import ControlFile
from pyforms.controls   import ControlText
from pyforms.controls   import ControlSlider
from pyforms.controls   import ControlPlayer
from pyforms.controls   import ControlButton

class ComputerVisionAlgorithm(BaseWidget):

    def __init__(self, *args, **kwargs):
        super().__init__('Computer vision algorithm example')

        #Definition of the forms fields
        self._videofile  = ControlFile('Video')
        self._outputfile = ControlText('Results output file')
        self._threshold  = ControlSlider('Threshold', default=114, minimum=0, maximum=255)
        self._blobsize   = ControlSlider('Minimum blob size', default=110, minimum=100, maximum=2000)
        self._player     = ControlPlayer('Player')
        self._runbutton  = ControlButton('Run')

        #Define the function that will be called when a file is selected
        self._videofile.changed_event = self.__video_file_selection_event
        #Define the event that will be called when the run button is processed
        self._runbutton.value = self.run_event
        #Define the event called before showing the image in the player
        self._player.process_frame_event = self.__process_frame

        #Define the organization of the Form Controls
        self._formset = [
            ('_videofile', '_outputfile'),
            '_threshold',
            ('_blobsize', '_runbutton'),
            '_player'
        ]


    def __video_file_selection_event(self):
        """
        When the videofile is selected instanciate the video in the player
        """
        self._player.value = self._videofile.value

    def __process_frame(self, frame):
        """
        Do some processing to the frame and return the result frame
        """
        return frame

    def run_event(self):
        """
        After setting the best parameters run the full algorithm
        """
        print("The function was executed", self._videofile.value)


if __name__ == '__main__':

    from pyforms import start_app
    start_app(ComputerVisionAlgorithm)