#!/usr/bin/python
#requires python3
import time
from datetime import datetime
import board	# blinka
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd


# Modify this if you have a different sized character LCD
lcd_columns = 16
lcd_rows = 2

# compatible with all versions of RPI as of Jan. 2019
# v1 - v3B+
lcd_rs = digitalio.DigitalInOut(board.D22)
lcd_en = digitalio.DigitalInOut(board.D17)
lcd_d4 = digitalio.DigitalInOut(board.D25)
lcd_d5 = digitalio.DigitalInOut(board.D24)
lcd_d6 = digitalio.DigitalInOut(board.D23)
lcd_d7 = digitalio.DigitalInOut(board.D18)


# Initialise the lcd class
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6,
                                      lcd_d7, lcd_columns, lcd_rows)

def time_convert(sec):
	mins = sec // 60
	sec = sec % 60
#	hours = mins // 60
	mins = mins % 60
	return ("min: {0}. sec: {1}".format(int(mins),int(sec))).rjust(lcd_columns," ")

def checkForResetButton():
	global resetPin
	global startTime # could do this with a class and no global variable
	global bottomLine
	global priorSecsInThisRun
	global isCounting # could do this with a class and no global variable
	global continueUpdating
	if resetButton.value == False: # false = button pressed
		priorSecsInThisRun = 0
		continueUpdating = True
		if isCounting == True: # reset time to zero, keep counting
			startTime = time.time()
			bottomLine = time_convert(0)
		else:
			bottomLine = 'ready'.rjust(lcd_columns)
        
def checkForCountingButton():	# assumes latching button
	global countPin
	global lightPin
	global startTime # could do this with a class and no global variable
	global bottomLine
	global isCounting # could do this with a class and no global variable
	global priorSecsInThisRun
	global continueUpdating
	cbv = countButton.value # HIGH == UP == True == button in
	if isCounting == True and cbv == True: # counting and button is still down
		secsPast = time.time() - startTime + priorSecsInThisRun
		bottomLine = time_convert(secsPast)
	if isCounting == False and cbv == True:     # button was just pressed in
#		print('button pressed')
		isCounting = True
		continueUpdating = True
		startTime = time.time()
		buttonLED.value = True # Turn on
		bottomLine = time_convert(priorSecsInThisRun)
	if isCounting == True and cbv == False:     # button was just let out
#		print('button unpressed')
		buttonLED.value = False # Turn off
		priorSecsInThisRun = time.time() - startTime + priorSecsInThisRun
		isCounting = False
		continueUpdating = False
		bottomLine = time_convert(priorSecsInThisRun)
	if isCounting == False and cbv == False: # button is out and has been so
		bottomLine = bottomLine

# operating code starts here

# before we start the main loop
isCounting = False # global
continueUpdating = True # global
priorSecsInThisRun = 0 # global
startTime = time.time() # global
bottomLine = 'ready'.rjust(lcd_columns) # global

lastLocalTime = time.time()

#initialize pins
resetButton = digitalio.DigitalInOut(board.D13)
countButton = digitalio.DigitalInOut(board.D19)
buttonLED = digitalio.DigitalInOut(board.D26)
resetButton.switch_to_input(pull=digitalio.Pull.UP)
countButton.switch_to_input(pull=digitalio.Pull.UP)
buttonLED.switch_to_output()
if countButton.value == True:
	buttonLED.value = True
else:
	buttonLED.value = False

#initial view
lcd.clear()
lcd.message = datetime.now().strftime('%b %d  %H:%M:%S\n') + bottomLine

while True:
	checkForCountingButton()
	checkForResetButton()
	# print('secsPast',round(secsPast,1),'lastSecsPast',round(lastSecsPast,1),'bottomline',bottomLine)
	localtimer = time.time()
	if localtimer - lastLocalTime >= 1:	# update every second
		if continueUpdating:
			lcd.message = datetime.now().strftime('%b %d  %H:%M:%S\n') + bottomLine
		else: #still update clock
			lcd.message = datetime.now().strftime('%b %d  %H:%M:%S')
		lastLocalTime = localtimer
