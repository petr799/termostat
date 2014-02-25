#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys
import datetime
import RPi.GPIO as GPIO

GPIO.setwarnings (False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
hlavice = {}
hlavice_flag = {}
output = {}
endtemp = {}
endtemp_low = {}
endtemp_high = {}
konecna = 0
ovl_kotel = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}
try:

# pripojeni k databazi
  con = mdb.connect('localhost', 'tmep', 'heslotmep', 'tmep');

  cur = con.cursor()
  cur.execute("SELECT room1, room2 FROM tme WHERE id=(SELECT max(id) FROM tme)")

  temp = cur.fetchone()

  print "Room1 : %s " % temp[0]
  print "Room2: %s " % temp[1]

  for x in range (2):
	  cur.execute("SELECT kotel FROM provoz WHERE (room = %s)", x)
	  ovl_kotel_db = cur.fetchone()
	  ovl_kotel[x] = ovl_kotel_db[0]
  for x in range (2):
	  cur.execute("SELECT hlavice FROM provoz WHERE (room = %s)", x)
	  hlavice_db = cur.fetchone()
	  hlavice[x] = hlavice_db[0]

#SELECT * FROM `programy` WHERE den = DAYOFWEEK(CURDATE());  
  for x in range (2):
#	y = "prog_room%s" % x
  	cur.execute("""SELECT konecna_teplota FROM prog_room%s WHERE (start_time <= CURTIME()) and (end_time >= CURTIME()) and (den = DAYOFWEEK(CURDATE()))""", (x))
  	endtemp[x] = cur.fetchone()

  	print "konecna room: %s " % endtemp[x]

#  cur.execute("SELECT konecna_teplota FROM prog_room2 WHERE (start_time <= CURTIME()) and (end_time >= CURTIME()) and (den = DAYOFWEEK(CURDATE()))")
#  endtemp[1] = cur.fetchone()

#  print "konecna room2 : %s " % endtemp[0]

  hyst = 0.5
  for x in range (2):
	konecna = endtemp[x]
	low = konecna[0] - hyst
	high = konecna[0] + hyst
	endtemp_low[x] = low
	endtemp_high[x] = high
  print "nizka hranice room1: %s " % endtemp_low[0]
  print "vysoka hranice room1: %s " % endtemp_high[0]
  print "nizka hranice room2: %s " % endtemp_low[1]
  print "vysoka hranice room2: %s " % endtemp_high[1]

  for x in range (2):
	if temp[x] < endtemp_low[x]:
		
		hlavice_flag[x] = 1
		print "zapnout hlavici %s" % x
		GPIO.output(hlavice[x], GPIO.HIGH)
  	elif temp[x] > endtemp_high[x]:
        	hlavice_flag[x] = 0
		print "vypnout hlavici %s" % x
		GPIO.output(hlavice[x], GPIO.LOW)
	elif (temp[x] > endtemp_low[x]) and (temp[x] < endtemp_high[x]):
		print "nic se nedeje"

  for x in range (2):
	if hlavice_flag[x] == 1 and ovl_kotel[x] > 0:
		print "kotel zapnout"
		GPIO.output(ovl_kotel[x], GPIO.HIGH)
	elif hlavice_flag[x] == 0 and ovl_kotel[x] > 0:
		print "kotel vypnout"
		

#  if temp[1] < endtemp_low[1]:
#        hlavice[1] = 1
#  elif temp[1] > endtemp_high[1]:
#        hlavice[1] = 0

#  if (hlavice[0] == 1) or (hlavice[1] == 1):
#	print "kotel zapnout"
#	GPIO.output(25, GPIO.HIGH)
#  elif (hlavice[0] == 0) and (hlavice[1] == 0):
#	print "kotel vypnout"
#	GPIO.output(25, GPIO.LOW)

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
