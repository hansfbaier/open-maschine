# open-maschine
Open Source Driver for Native Instruments(TM) Maschine

The goal of this project is to create an open source
driver for the Native Instruments (TM) Maschine Controller.

The Hardware I use is the Maschine MK2.

Currently this repository contains proof of concept code to demonstrate,
how to talk to Maschine and how to read from it.

To run the proof of concept you have to compile and install hidapi
and pyhidapi first.

Then connect Maschine and:
$ cd proof-of-concept
$ sudo ./talk-with-maschine.py

if you want to put your own images on the displays,
you can use GIMP to create an xbm file like the
two examples, run 
xmbtostring.pl < input.xbm > output.hex
to create the hex string and then read them in with python.

This includes setting all the button leds,
the displays and reading
all buttons and encoders (last is implicit since thats the output)

Have fun!
Kind regards,
Hans
