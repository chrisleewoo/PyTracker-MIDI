# CircuitPython LSDJ


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
from lib import Generator
import shapes

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
speaker_enable.value = True

chan1 = [0]*6   #freq, vol, wave, length, ticks, duty_cycle
chan2 = [0]*6
chan3 = [0]*6
chan4 = [0]*6

def length(frequency):
    return int(32000 / frequency)



class Generator:

    sample = None
    dac = None
    shape = None
    frequency = None


    def __init__(self):
        self.dac = audioio.AudioOut(board.A0)


    def reallocate(self, frequency):
        self.sample = array.array("h", [0] * length(frequency))


    def make_sine(self, volume):
        l = len(self.sample)
        for i in range(l):
            self.sample[i] = min(2 ** volume - 1, int(math.sin(math.pi * 2 * i / l) * (2 ** volume)))


    def make_square(self):
        l = len(self.sample)
        half_l = l // 2
        for i in range(l):
            if i < half_l:
                self.sample[i] = -1 * ((2 ** 15) - 1)
            else:
                self.sample[i] = (2 ** 15) - 1


    def make_triangle(self):
        l = len(self.sample)
        half_l = l // 2
        s = 0
        for i in range(l):
            if i <= half_l:
                s = int((i / half_l) * (2 ** 16)) - (2 ** 15)
            else:
                s = int((1 - ((i - half_l) / half_l)) * (2 ** 16)) - (2 ** 15)
            self.sample[i] = min(2 ** 15 -1, s)



    def make_sawtooth(self):
        l = len(self.sample)
        for i in range(l):
            self.sample[i] = int((i / l) * (2 ** 16)) - (2 ** 15)


    def update(self, shape, frequency, volume):
        if shape == self.shape and frequency == self.frequency:
            return

        if frequency != self.frequency:
            self.reallocate(frequency)
            self.frequency = frequency

        self.shape = shape
        if shape == shapes.SINE:
            self.make_sine(volume)
        elif shape == shapes.SQUARE:
            self.make_square()
        elif shape == shapes.TRIANGLE:
            self.make_triangle()
        elif shape == shapes.SAWTOOTH:
            self.make_sawtooth()

        #self.dac.stop()
        #self.dac.play(audioio.RawSample(self.sample, channel_count=1, sample_rate=64000), loop=True)


generator = Generator()
delta = 0                             # how much to change the frequency by
shape = shapes.SINE                          # the active waveform
frequency = 110                       # the current frequency
volume = 12                     #0 -15


for x in range(20000):
    generator.update(shape, frequency, volume)

print(generator.sample)

##need to add volume for all waves










def customwait(wait_time):
        start = time.monotonic()
        while time.monotonic() < (start + wait_time):
            pass


def sound_player(chan1, chan2, chan3, chan4, ticks):
    #need to add arrays
        mixer_wave = array.array("H", [0] * length(ticks) )
        buffer_bytes = wave_out(chan1[0], chan1[1], chan1[2], chan1[3], chan1[4], chan1[5])
        #then mod by volume setting
		#then send to AudioOut
        real_freq = chan1[0]
        print(real_freq)
        for x in range (len(buffer_bytes)):
            analog_out.value = buffer_bytes[x]
            time.sleep(real_freq)


print("playing")
#       freq, vol,  wave,   length,    ticks,   duty_cycle

ticks = chan1[4]


chan1 = [110,   2,   'sqr',   10000,   100,      .5]
chan2 = [110, 2, 'sqr', 10000, 100, .5]
chan3 = [110, 2, 'sqr', 10000, 100, .75]
#sound_player(chan1, chan2, chan3, chan4, ticks)
#sound_player(chan2, chan2, chan3, chan4, ticks)
#sound_player(chan3, chan2, chan3, chan4, ticks)

chan1 = [110,   2,   'sqr',   10000,   100,      .5]
chan2 = [110, 2, 'sqr', 10000, 100, .5]
chan3 = [110, 2, 'sqr', 10000, 100, .75]
#sound_player(chan1, chan2, chan3, chan4, ticks)
#sound_player(chan2, chan2, chan3, chan4, ticks)
#sound_player(chan3, chan2, chan3, chan4, ticks)


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


    #print("sorry nothing...")
    #pixels.fill(RED)
    #pixels.show()
    #time.sleep(.2)
    #pixels.fill(YELLOW)
    #pixels.show()
    # Increase or decrease to change the speed of the solid color change.
    #time.sleep(.2)
    #pixels.fill(GREEN)
    #pixels.show()
    #time.sleep(.2)
    #pixels.fill(CYAN)
    #pixels.show()
    #time.sleep(.2)
    #pixels.fill(BLUE)
    #pixels.show()
    #time.sleep(.2)
    #pixels.fill(PURPLE)
    #pixels.show()
    #time.sleep(.2)
    #pixels.fill(OFF)
    #pixels.show()
    #time.sleep(10)
    #for f in (262, 294, 330, 349, 392, 440, 494, 523):
     #   simpleio.tone(board.A0, f, 1)
    #time.sleep(1)

    #color_chase(RED, .1)  # Increase the number to slow down the color chase
    #color_chase(YELLOW, .1)
    #color_chase(GREEN, .1)
    #color_chase(CYAN, .1)
    #color_chase(BLUE, .1)
    #color_chase(PURPLE, .1)

    #rainbow_cycle(.1)  # Increase the number to slow down the rainbow
    pixels.fill(OFF)
    pixels.show()
    #time.sleep(10)

            # Reading buttons too fast returns 0
    if (last_read + 0.1) < time.monotonic():
        buttons = pad.get_pressed()
        last_read = time.monotonic()
    if current_buttons != buttons:
        # Respond to the buttons
        if (buttons == 0b00010100):

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


