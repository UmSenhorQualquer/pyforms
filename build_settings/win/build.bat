@echo off

setlocal enableextensions enabledelayedexpansion

rem set /A PYTHON_VERSION=2

IF /I "%PYTHON_VERSION%" EQU "2" (
	ECHO "python 2"

	set "WINPYDIR=C:\Users\swp\Python\WinPython-32bit-2.7.10.3\python-2.7.10"
	set "WINPYVER=2.7.10.3"
) ELSE (
	ECHO "python 3"

	set "WINPYDIR=C:\Users\swp\Python\WinPython-32bit-3.4.3.7\python-3.4.3"
	set "WINPYVER=3.4.3.7"
)

set "HOME=%WINPYDIR%\..\settings"
set "WINPYARCH=WIN32"

set "PATH=%WINPYDIR%\Lib\site-packages\PyQt4;%WINPYDIR%\;%WINPYDIR%\DLLs;%WINPYDIR%\Scripts;%WINPYDIR%\..\tools;"

rem keep nbextensions in Winpython directory, rather then %APPDATA% default
set "JUPYTER_DATA_DIR=%WINPYDIR%\..\settings"

set PROJECTNAME="pyforms"

python --version

pip uninstall -y %PROJECTNAME%
pip install .
pip show %PROJECTNAME%

python setup.py sdist --formats=zip