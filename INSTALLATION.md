# Installation

## Install
Use the provided installers for OSX (10.14 and upwards) or 
Windows 10. Those can be found in releases. This software also 
runs on Linux, however, you should compile it yourself for best 
results.


## Compilation: TL;DR

You must have python3.5 or 3.6 installed. Create a virtual environment and activate it with:

	python -m venv venv
	source venv/bin/activate

or via conda:

	conda create -n schemedrawer python=3.6
	conda activate schemedrawer

Install dependencies:

	pip install -r requirements.txt

Freeze and create installer

	fbs freeze
	fbs installer

Look at the output, it will tell you where the files are.


## Compilation: Detailed Instructions

This software uses fbs to build the PyQt5, python application.
[https://build-system.fman.io/](https://build-system.fman.io/)  
Please check out the fbs tutorial for details. 

### Virtual environment creation

The best results are achieved if you compile from a virtual environment. You must have python3.5 or python3.6 installed. If you use standard python, go ahead and type:

	python -m venv venv

to create a virtual environment. It can then be activated with 

	source venv/bin/activate

or on Windows via:
	
	call venv\Scripts\activate

With conda create a virtual environment in python3.6 by typing:

	conda create -n schemedrawer python=3.6

This will ensure that you have a python3.6 environment. The `-n` option furthermore lets you specify a name for the virtual environment, here the name is `schemedrawer`. Activating the virtual environment can be done via:

	conda activate schemedrawer

### Installation of requirements

Several python packages must be installed in python virtual environment. This repository contains a requirement file, which lets you easily set up the requirements by running:

    pip install -r requirements.txt

Note: Please see the [fbs tutorial](https://github.com/mherrmann/fbs-tutorial) for further requirements if you want to create installers of the program as well.

### Freezing the software and creating installers
  
You should be able to run the software now if you are in the project folder by running:

    fbs run

To freeze the program, i.e., create an executable run:

    fbs freeze

An installer, the type of which depends on your operating system, can be created after freezing by typing:

    fbs installer

Such installers can also be found in the released versions. 

If you want to clean up your compiled versions, go ahead and type 

	fbs clean

### Troubleshooting

 * On Windows, freezing the application, even if all the dependencies mentioned on the fbs tutorial site are installed, can throw an error that not all libraries are installed. It gives you a link to download the windows developer kit or something like that. After doing that and installing it, you should be good to go.

 * I have seen PyInstaller errors that look something like this: `subprocess.CalledProcessError: Command '['pyinstaller', some more characters]` These errors can indicate a package conflict. I had conflicts especially with the `enum34` package. Simply uninstall it with: `pip uninstall enum34` usually solves the problem and should not give you any trouble since you are in a virtual environment.


