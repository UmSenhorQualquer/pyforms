********************
Install & configure
********************

* Install Pyforms using **pip**.

.. code:: bash

    pip install pyforms


* To install the pyforms layers indevidually check the documentation at:

.. image:: /_static/imgs/pyforms-gui.jpg
    :width: 80px
    :align: left
    
`pyforms-gui.readthedocs.io <https://pyforms-gui.readthedocs.io>`_

|

.. image:: /_static/imgs/pyforms-web.jpg
    :width: 80px
    :align: left

`pyforms-web.readthedocs.io <https://pyforms-web.readthedocs.io>`_

|

.. image:: /_static/imgs/pyforms-terminal.jpg
    :width: 80px
    :align: left

`pyforms-terminal.readthedocs.io <https://pyforms-terminal.readthedocs.io>`_

|
|

Configure
___________

To switch between execution modes, create the file **local_settings.py** in application running directory with the content:

.. code-block:: python

    # This flag is used by the module confapp to set these settings as high priority.
    SETTINGS_PRIORITY = 0 

    # The variable is used by pyforms to define the mode it will run. 
    # It can has the value 'GUI', 'WEB' or 'TERMINAL'.
    PYFORMS_MODE = 'TERMINAL' 