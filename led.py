#!/usr/bin/python

from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(25, GPIO.OUT)
GPIO.output(25, GPIO.LOW)

try:
 while True:
	
	    GPIO.output(25, GPIO.HIGH)
except:	    
 GPIO.cleanup()
