#name=AKAI Midimix

import mixer
import midi
import device
import general
import time
import ui
import transport

# All arrays shown here map the controls from left to right on the midimix
faderInputs  = [19, 23, 27, 31, 49, 53, 57, 61]
masterFader  = 62
panInputs    = [18, 22, 26, 30, 48, 52, 56, 60]
muteButtons  = [1, 4, 7, 10, 13, 16, 19, 22]
soloButtons  = [2, 5, 8, 11, 14, 17, 20, 23]
armButtons   = [3, 6, 9, 12, 15, 18, 21, 24]
bankLeft     = 25
bankRight    = 26
soloSwitch   = 27
LEDknob      = 58
LED1s        = list(range(0, 32))
LED2s        = list(range(32, 64))
LED3s        = list(range(64, 96))
LED4s	     = list(range(96, 127))

panDeadZoneLow  = 62 # range is 0-127 on the knobs
panDeadZoneHigh = 65

mixerTreshold = 0.15
selectedTrack = mixer.getTrackInfo(3)
LEDmode  = 2

# set to 0 to disable this if the very slight input lag bothers you
selectFeedbackDuration = 0

# when disabled, the solo buttons can be mapped to 'Link to controller' functions in FL Studio
useNormalSolo = True


# CONSTANTS
potInput          = 176
buttonPress       = midi.MIDI_NOTEON
buttonRelease     = midi.MIDI_NOTEOFF
minimumAPIVersion = 7
realTrackCount    = mixer.trackCount() - 2

# Environment variables
trackOffset = 1
soloStates  = [0, 0, 0, 0, 0, 0, 0, 0]

def constrain(number, max, trueMax):
	return number * max / trueMax

def constrainPan(number):
	if number >= panDeadZoneLow and number <= panDeadZoneHigh:
		return 0
	else:
		return constrain(number, 2, 127) - 1.0

def updateLEDs():
	global trackOffset, soloStates

	if LEDmode == 1:

		for i in range(0, 8):
			try:
				# set mute
				if mixer.isTrackMuted(trackOffset + i):
					device.midiOutMsg(midi.MIDI_NOTEON + ((i * 3) + 1 << 8) + (0 << 16))
				else:
					device.midiOutMsg(midi.MIDI_NOTEON + ((i * 3) + 1 << 8) + (127 << 16))
				# set solo
				if useNormalSolo:
					if mixer.isTrackSolo(trackOffset + i):
						device.midiOutMsg(midi.MIDI_NOTEON + ((i * 3) + 2 << 8) + (127 << 16))
					else:
						device.midiOutMsg(midi.MIDI_NOTEON + ((i * 3) + 2 << 8) + (0 << 16))
				else:
					if soloStates[i] == 1:
						device.midiOutMsg(midi.MIDI_NOTEON + ((i * 3) + 2 << 8) + (127 << 16))
					else:
						device.midiOutMsg(midi.MIDI_NOTEON + ((i * 3) + 2 << 8) + (0 << 16))

				# bottom buttons
				if mixer.getTrackPeaks(trackOffset + i, 2) > mixerTreshold and mixer.isTrackMuted(trackOffset + i) == False:
					device.midiOutMsg(midi.MIDI_NOTEON + ((i * 3) + 3 << 8) + (127 << 16))
				else:
					device.midiOutMsg(midi.MIDI_NOTEON + ((i * 3) + 3 << 8) + (0 << 16))

			except:
				break

	if LEDmode == 2:

		for i in range(0, 8):
			try:

				# left peak
				if mixer.getTrackPeaks(selectedTrack, 0) >= (i / 7) and mixer.isTrackMuted(selectedTrack) == False:
					device.midiOutMsg(midi.MIDI_NOTEON + ((i * 3) + 1 << 8) + (127 << 16))
				else:
					device.midiOutMsg(midi.MIDI_NOTEON + ((i * 3) + 1 << 8) + (0 << 16))

				# right peak
				if mixer.getTrackPeaks(selectedTrack, 1) >= (i / 7) and mixer.isTrackMuted(selectedTrack) == False:
					device.midiOutMsg(midi.MIDI_NOTEON + ((i * 3) + 3 << 8) + (127 << 16))
				else:
					device.midiOutMsg(midi.MIDI_NOTEON + ((i * 3) + 3 << 8) + (0 << 16))

			except:
				break

	if LEDmode == 3:

		for i in range(0, 8):
			try:

				# left peak
				if mixer.getTrackPeaks(0, 0) >= (i / 7) and mixer.isTrackMuted(0) == False:
					device.midiOutMsg(midi.MIDI_NOTEON + ((i * 3) + 1 << 8) + (127 << 16))
				else:
					device.midiOutMsg(midi.MIDI_NOTEON + ((i * 3) + 1 << 8) + (0 << 16))

				# right peak
				if mixer.getTrackPeaks(0, 1) >= (i / 7) and mixer.isTrackMuted(0) == False:
					device.midiOutMsg(midi.MIDI_NOTEON + ((i * 3) + 3 << 8) + (127 << 16))
				else:
					device.midiOutMsg(midi.MIDI_NOTEON + ((i * 3) + 3 << 8) + (0 << 16))

			except:
				break

	if LEDmode == 4:

		for i in range(0, 8):
			try:

				# master peak
				if mixer.getTrackPeaks(0, 2) >= (i / 7) and mixer.isTrackMuted(0) == False:
					device.midiOutMsg(midi.MIDI_NOTEON + ((i * 3) + 1 << 8) + (127 << 16))
				else:
					device.midiOutMsg(midi.MIDI_NOTEON + ((i * 3) + 1 << 8) + (0 << 16))

				# selected peak
				if mixer.getTrackPeaks(selectedTrack, 2) >= (i / 7) and mixer.isTrackMuted(selectedTrack) == False:
					device.midiOutMsg(midi.MIDI_NOTEON + ((i * 3) + 3 << 8) + (127 << 16))
				else:
					device.midiOutMsg(midi.MIDI_NOTEON + ((i * 3) + 3 << 8) + (0 << 16))

			except:
				break

def LED1():
	global LEDmode
	LEDmode = 1

def LED2():
	global LEDmode
	LEDmode = 2

def LED3():
	global LEDmode
	LEDmode = 3

def LED4():
	global LEDmode
	LEDmode = 4

def setTrackData():
	global trackOffset
	updateLEDs()
	mixer.deselectAll()
	mixer.setTrackNumber(trackOffset)
	if selectFeedbackDuration > 0:
		for i in range(0, 8):
			try:
				mixer.selectTrack(trackOffset + i)
			except:
				break
		time.sleep(selectFeedbackDuration)
		mixer.deselectAll()
		mixer.setTrackNumber(trackOffset)

def OnInit():
	device.setHasMeters()
	global trackOffset
	trackOffset = 1
	if general.getVersion() >= minimumAPIVersion:
		setTrackData()
	else:
		raise Exception("Your version of FL Studio is too old to use this script. Please update to a newer version.")

def OnDeInit():
	print("deinit")
	device.midiOutMsg(midi.MIDI_NOTEON + (25 << 8) + (0 << 16))
	device.midiOutMsg(midi.MIDI_NOTEON + (26 << 8) + (0 << 16))
	for i in range(0, 8):
		device.midiOutMsg(midi.MIDI_NOTEON + ((i * 3) + 1 << 8) + (0 << 16))
		device.midiOutMsg(midi.MIDI_NOTEON + ((i * 3) + 2 << 8) + (0 << 16))
		device.midiOutMsg(midi.MIDI_NOTEON + ((i * 3) + 3 << 8) + (0 << 16))

def OnRefresh(flags):
	if flags == 263 or flags == 7:
		updateLEDs()

def OnUpdateMeters():
	updateLEDs()

def OnMidiMsg(event):
	global trackOffset, soloStates
	event.handled = False
	#print(event.midiId, event.data1, event.data2, event.status, event.note, event.progNum, event.controlNum, event.controlVal)
	if event.midiId == potInput:

		if event.data1 in faderInputs:
			trackNum = faderInputs.index(event.data1) + trackOffset
			if trackNum <= realTrackCount:
				mixer.setTrackVolume(trackNum, constrain(event.data2, 0.8, 127))
			#print("fader input")
			event.handled = True

		elif event.data1 == masterFader:
			mixer.setTrackVolume(0, constrain(event.data2, 0.8, 127))
			#print("master input")
			event.handled = True

		elif event.data1 in panInputs:
			trackNum = panInputs.index(event.data1) + trackOffset
			if trackNum <= realTrackCount:
				mixer.setTrackPan(trackNum, constrainPan(event.data2))
			#print("pan input")
			event.handled = True

		elif event.data1 == LEDknob:
			if event.data2 in LED1s:
				print("LEDmode 1")
				LED1()

			elif event.data2 in LED2s:
				print("LEDmode 2")
				LED2()

			elif event.data2 in LED3s:
				print("LEDmode 3")
				LED3()

			elif event.data2 in LED4s:
				print("LEDmode 4")
				LED4()

	elif event.midiId == buttonPress:
		
		# process input
		if event.data1 == bankLeft:
			device.midiOutMsg(midi.MIDI_NOTEON + (25 << 8) + (0 << 16))
			event.handled = True
			if trackOffset > 1:
				trackOffset = trackOffset - 8
				setTrackData()
				#print("left", trackOffset)
			
		elif event.data1 == bankRight:
			device.midiOutMsg(midi.MIDI_NOTEON + (26 << 8) + (0 << 16))
			event.handled = True
			if trackOffset < (realTrackCount - (realTrackCount % 8) + 1):
				trackOffset = trackOffset + 8
				setTrackData()
				#print("right", trackOffset)
	
		elif event.data1 in muteButtons:
			trackNum = muteButtons.index(event.data1) + trackOffset
			if trackNum <= realTrackCount:
				mixer.muteTrack(trackNum)
			#print("mute")
			event.handled = True
		
		elif event.data1 in soloButtons:
			if useNormalSolo:
				trackNum = soloButtons.index(event.data1) + trackOffset
				if trackNum <= realTrackCount:
					mixer.soloTrack(trackNum)
				#print("solo")
				event.handled = True
			else:
				index = soloButtons.index(event.data1)
				if soloStates[index] == 1:
					event.midiId = potInput
					event.status = potInput
					event.velocity = 0
					event.controlVal = 0
					soloStates[index] = 0
				else:
					event.midiId = potInput
					event.status = potInput
					event.velocity = 127
					event.controlVal = 127
					soloStates[index] = 1
				event.handled = False
			updateLEDs()
		
		elif event.data1 in armButtons:
			trackNum = armButtons.index(event.data1) + trackOffset
			if trackNum <= realTrackCount:
				mixer.armTrack(trackNum)
			#print("arm")
			event.handled = True

		elif event.data1 == soloSwitch:
			event.handled = True

	# visual feedback
	elif event.midiId == buttonPress:
		event.handled = True
		if event.data1 == bankLeft:
			device.midiOutMsg(midi.MIDI_NOTEON + (25 << 8) + (127 << 16))
		elif event.data1 == bankRight:
			device.midiOutMsg(midi.MIDI_NOTEON + (26 << 8) + (127 << 16))
