# Enable PyBadge to write to its filesystem
# if a button is pressed while rebooting
# (normally the filesystem is only writeable by the host over USB)
import board
import digitalio
import storage
import time

from gamepadshift import GamePadShift
pad = GamePadShift(digitalio.DigitalInOut(board.BUTTON_CLOCK),
                   digitalio.DigitalInOut(board.BUTTON_OUT),
                   digitalio.DigitalInOut(board.BUTTON_LATCH))
    
time.sleep(.5) # wait a bit to read buttons
if pad.get_pressed():
	# CircuitPython can write to the local drive if readonly is False
	storage.remount("/", False)
	print(' Filesystem Writeable')
else:
	print(' Filesystem ReadOnly')
    

