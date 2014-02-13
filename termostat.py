#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys
import datetime
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
try:
  con = mdb.connect('localhost', 'testuser', 'test123', 'testdb');

  cur = con.cursor()
  cur.execute("SELECT teplota, teplota2 FROM tme WHERE id=(SELECT max(id) FROM tme)")

  temp = cur.fetchone()

  print "Nejnovejsi teplota : %s " % temp[0]
  print "Room2: %s " % temp[1]
#SELECT * FROM `programy` WHERE den = DAYOFWEEK(CURDATE());  
  cur.execute("SELECT konecna_teplota FROM programy_room1 WHERE (start_time <= CURTIME()) and (end_time >= CURTIME()) and (den = DAYOFWEEK(CURDATE()))")
  endtemp_r1 = cur.fetchone()

  print "konecna room1 : %s " % endtemp_r1

  cur.execute("SELECT konecna_teplota FROM programy_room2 WHERE (start_time <= CURTIME()) and (end_time >= CURTIME()) and (den = DAYOFWEEK(CURDATE()))")
  endtemp_r2 = cur.fetchone()

  print "konecna room2 : %s " % endtemp_r2

  hyst = 0.5
  endtemplow_r1 = endtemp_r1[0] - hyst
  print "nizka hranice room1: %s " % endtemplow_r1
  endtemphigh_r1 = endtemp_r1[0] + hyst
  print "vysoka hranice room1: %s " % endtemphigh_r1

  endtemplow_r2 = endtemp_r2[0] - hyst
  print "nizka hranice room2: %s " % endtemplow_r2
  endtemphigh_r2 = endtemp_r2[0] + hyst
  print "vysoka hranice room2: %s " % endtemphigh_r2


#  if temp[0] < endtemplow:
#	print "kotel zapnout"
#  elif temp[0] > endtemphigh:
#	print "kotel vypnout"

  if temp[0] < endtemplow_r1:
	hlavice_r1 = 1
	GPIO.output(4, GPIO.HIGH)
  elif temp[0] > endtemplow_r1:
        hlavice_r1 = 0
	GPIO.output(4, GPIO.LOW)

  if temp[1] < endtemplow_r2:
        hlavice_r2 = 1
  elif temp[1] > endtemplow_r2:
        hlavice_r2 = 0

  if (hlavice_r1 == 1) or (hlavice_r2 == 1):
	print "kotel zapnout"
	GPIO.output(25, GPIO.HIGH)
  elif (hlavice_r1 == 0) and (hlavice_r2 == 0):
	print "kotel vypnout"
	GPIO.output(25, GPIO.LOW)

########################################################
#  else:
#	print "nedelej nic"
#  if temp < endtemp and laststate = 0:
#	print "kotel zapnout"
#	cur.execute("UPDATE provoz SET hodnota = 1 WHERE promena = laststate"
#  if temp < endtemp and laststate = 1:
#	print "kotel topi"
#  if temp = endtemp and laststate = 1:
#	print "teplota stoupa"
#  if temp > endtemp and laststate = 1:
#	print "kotel vypnout"
#	cur.execute("UPDATE provoz SET hodnota = 0 WHERE promena = laststate"
#  if temp > endtemp and laststate = 0:
#	print "kotel netopi"
#  if temp = endtemp and laststate = 0:
#	print "teplota klesa"

except mdb.Error, e:

  print "Error %d: %s" % (e.args[0],e.args[1])
  sys.exit(1)
#  GPIO.cleanup()

finally:

  if con:
	con.close()
#GPIO.cleanup()
