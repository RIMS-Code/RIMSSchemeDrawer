# RIMSSchemeDrawer
A drawing program to create publishable RIMS schemes.  

License: GPLv2

## How to use
The GUI should be fairly self explaining. If you don't know what
to do, hover over an enty field and a tooltip should appear.

## Install
Use the provided installers for OSX (10.14 and upwards) or 
Windows 10. Those can be found in releases. This software also 
runs on linux, however, you should compile it yourself for best 
results.

## Compile
This software uses fbs: 
[https://build-system.fman.io/](https://build-system.fman.io/)  
Please check out the fbs tutorial for details. 

To compile the program please download it and unpack it. Make 
sure you have python3.7 installed. Go to the folder on the terminal.

Install python requirements by running:

    pip install -r requirements.txt
    
Now you should be able to run the program with fbs, freeze it, and 
create an installer

    fbs run
    fbs freeze
    fbs installer

Freezing the program will give you an executable that you can run on
your individual system.
    

## Changelog
 * **v2.0.0**: First time there's a readme file. Previous version 
 used TKinter, now we are using PyQt5 and all is compiled w/ fbs.
