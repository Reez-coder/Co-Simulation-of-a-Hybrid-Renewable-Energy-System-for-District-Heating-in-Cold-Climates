# Info on how to configure python for Cosimulation labs

V. Chevrier April 2025
(update of version 0.2)
tested on python 3.13

## Foreword: 32 or 64 bits

Either you want to execute 32 or 64 bit FMU, you need to use the proper version of python



***to know which python you have***:
python ==>

		import platform
		platform.architecture()
answers:

	('64bit', 'WindowsPE')
	or
	('32bit', 'WindowsPE')



## Basics
-

1.
in the shell window type
type pip install for missing package
(that is
attrs==25.3.0
contourpy==1.3.2
cycler==0.12.1
FMPy==0.3.23
fonttools==4.57.0
Jinja2==3.1.6
kiwisolver==1.4.8
lark==1.2.2
lxml==5.4.0
MarkupSafe==3.0.2
matplotlib==3.10.1
msgpack==1.1.0
numpy==2.2.5
packaging==25.0
pillow==11.2.1
pyparsing==3.2.3
PyQt5==5.15.11
PyQt5-Qt5==5.15.2
PyQt5_sip==12.17.0
pyqtgraph==0.13.7
PySide6==6.9.0
PySide6_Addons==6.9.0
PySide6_Essentials==6.9.0
python-dateutil==2.9.0.post0
shiboken6==6.9.0
six==1.17.0
)

2. then try to execute
	- testBase.py
	- examplesBase.py
## Links

https://pip.pypa.io/en/stable/reference/pip_freeze/

requirements file generation by **py -m pip freeze > requirements.txt** on a command line in right directory
