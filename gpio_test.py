#!/usr/bin/python

from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.LOW)

GPIO.setup(27, GPIO.IN)

while True:
	
	if ( GPIO.input(27) == True ):
	    GPIO.output(17, GPIO.HIGH)
	    print "stisknuto tlacitko "
	else:
	    GPIO.output(17, GPIO.LOW)
	    
