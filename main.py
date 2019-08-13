'''
CircuitPython DJ
Inspired by LSDJ and nanoloop gameboy trackers
Code snippets and libraries from the following Adafruit Learning Guides:
    FruitBox Sequencer
    PyBadge GamePad
    Feather Waveform Generator in CircuitPython
    Circuit Playground Express USB MIDI Controller and Synthesizer

'''


import time
import array
import math
import digitalio
import board
import busio
import neopixel
import displayio
import simpleio
import terminalio
import audioio
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_text import label
from digitalio import DigitalInOut, Direction, Pull
from adafruit_bus_device.i2c_device import I2CDevice
from gamepadshift import GamePadShift
from micropython import const
from analogio import AnalogOut
from generator import Generator
import shapes
import pitches

import usb_midi

import adafruit_lis3dh
import adafruit_midi

from adafruit_midi.note_on          import NoteOn
from adafruit_midi.control_change   import ControlChange
from adafruit_midi.pitch_bend       import PitchBend

from adafruit_midi.note_on          import NoteOn
from adafruit_midi.control_change   import ControlChange
from adafruit_midi.pitch_bend       import PitchBend

midi_note_C4 = 60
midi_cc_modwheel = 1  # was const(1)

velocity = 127
min_octave = -3
max_octave = +3
octave = 0
min_semitone = -11
max_semitone = +11
semitone = 0


# Button Constants
BUTTON_LEFT = const(128)
BUTTON_UP = const(64)
BUTTON_DOWN = const(32)
BUTTON_RIGHT = const(16)
BUTTON_SEL = const(8)
BUTTON_START = const(4)
BUTTON_A = const(2)
BUTTON_B = const(1)

pad = GamePadShift(digitalio.DigitalInOut(board.BUTTON_CLOCK),
                   digitalio.DigitalInOut(board.BUTTON_OUT),
                   digitalio.DigitalInOut(board.BUTTON_LATCH))


speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker_enable.direction = digitalio.Direction.OUTPUT
speaker_enable.value = False


midi_channel = 1
midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1],
                          out_channel=midi_channel-1)


bpm = 60  # quarter note beats per minute
beat = 15 / bpm  # 16th note expressed as seconds, each beat is this long



def customwait(wait_time):
        start = time.monotonic()
        while time.monotonic() < (start + wait_time):
            pass




print("playing")
midi.send(NoteOn(60, velocity))
customwait(2)
midi.send(NoteOn(60, 0))

print("stopped")
speaker_enable.value = False


display = board.DISPLAY

# Set text, font, and color
text = "ChrisLeeWoo"
font = terminalio.FONT
color = 0x0000FF

# Create the text label
text_area = label.Label(font, text="ChrisLeeWoo", color=0x6F9FAF)

# Set the location
text_area.x = 23
text_area.y = 23

# Show it
# display.show(text_area)

# Make the display context
splash = displayio.Group(max_size=10)
display.show(splash)

# Make a background color fill
color_bitmap = displayio.Bitmap(160, 128, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x000000
bg_sprite = displayio.TileGrid(color_bitmap, x=0, y=0,
                               pixel_shader=color_palette)
splash.append(bg_sprite)
##########################################################################

# add my sprite

roundrect = RoundRect(10, 10, 90, 30, 10, fill=0x0, outline=0xAFAF00, stroke=6)
splash.append(roundrect)
splash.append(text_area)
# insert play startup sound here ######
customwait(1)

mixgrid = displayio.Group(max_size=40)

for g in range(4):
        for h in range(4):
            gridsq = Rect( (52+24*g), (5+24*h), 24, 24, fill=0x0, outline=0xAFAFFF, stroke=2)
            mixgrid.append(gridsq)

display.show(mixgrid)



pixel_pin = board.D8
num_pixels = 8

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
    customwait(0.5)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(rc_index & 255)
        pixels.show()
        customwait(wait)


def set_grid_disp(note,spot):
    #be aware of overwriting a current note
    # clear the screen starting at (54,7) with size 20

    mixgrid.pop(spot+15)
    thing = label.Label(font, text=note, color=0xff9Fff)
    thing.x = pixelocate_x(spot)
    thing.y = pixelocate_y(spot)
    #insert(index, layer)
    mixgrid.insert(spot+15, thing)

def pixelocate_x(number):
    return 55 + 24 * ( number % 4 )


def pixelocate_y(number):
    if number < 4:
        return 15
    elif number < 8:
        return 15 + 24
    elif number < 12:
        return 15 + 24*2
    else: return 15 + 24*3

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
OFF = (0,0,0)
current_buttons = pad.get_pressed()
last_read = 0

for g in range(15):
    g0 = label.Label(font, text="   ", color=0xff9Fff)
    mixgrid.append(g0)

set_grid_disp('c#4',14)
time.sleep(.5)
set_grid_disp('   ',14)
time.sleep(.5)
set_grid_disp('a 7',14)
time.sleep(.1)
set_grid_disp('c 5',14)

while True:

    pixels.fill(OFF)
    pixels.show()

            # Reading buttons too fast returns 0
    if (last_read + 0.1) < time.monotonic():
        buttons = pad.get_pressed()
        last_read = time.monotonic()
    if current_buttons != buttons:
        # Respond to the buttons
        if (buttons == BUTTON_SEL + BUTTON_A): #
            customwait(.5)
        elif (buttons == 0b01000100):
            customwait(.5)

        elif (buttons == 0b10000100):
            customwait(.5)

        elif (buttons & BUTTON_LEFT) > 0:
            print('Left', buttons)
        elif (buttons & BUTTON_UP) > 0 :
            print('Up', buttons)
        elif (buttons & BUTTON_DOWN) > 0 :
            print('Down', buttons)
        elif (buttons & BUTTON_A) > 0 :
            print('A', buttons)
        elif (buttons & BUTTON_B) > 0 :
            print('B', buttons)
        elif (buttons & BUTTON_START) > 0 :
            print('Start', buttons)

        elif (buttons & BUTTON_SEL) > 0 :
            print('Select', buttons)

        elif (buttons & BUTTON_RIGHT) > 0:
            print('Right', buttons)

        current_buttons = buttons


