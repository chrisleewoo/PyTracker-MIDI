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
#import array
import math
import digitalio
import board
import busio
#import neopixel
import displayio
import simpleio
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_text import label
from digitalio import DigitalInOut, Direction, Pull
#from adafruit_bus_device.i2c_device import I2CDevice
from gamepadshift import GamePadShift
#from micropython import const
#from analogio import AnalogOut
import storage


#import shapes
#import pitches
from notevals import display_note

import usb_midi

#import adafruit_lis3dh
import adafruit_midi

from adafruit_midi.note_on          import NoteOn
from adafruit_midi.control_change   import ControlChange
from adafruit_midi.pitch_bend       import PitchBend

midi_note_C4 = 60
midi_cc_modwheel = 1  
midi_channels = [1,2,3,4] # default MIDI channels for the 4 tracks
velocity = 127 # default velocity
min_octave = -3
max_octave = +3
octave = 0
min_semitone = -11
max_semitone = +11
semitone = 0

bpm = 60 # quarter note beats per minute
beat = 15 / bpm  # 16th note expressed as seconds, each beat is this long

MAX_TRACKS = 4
current_filename = 'nan.csv'
current_songname = 'default'
current_track = 0
current_pattern = 0
current_track = 0
current_level = 127
current_effect = 0
current_menu = 0
current_menu_item = 0
mode = 'Note'  # settings modes
playing = False
screen = 0 
x = 0
seq =   [
        [[10,0,0], [20,0,0], [0,0,0], [40,0,0],
        [50,0,0], [60,0,0], [70,0,0], [80,0,0],
        [0,0,0], [20,0,0], [30,0,0], [40,0,0],
        [50,0,0], [60,0,0], [70,0,0], [80,0,0]],
        
        [[60,0,0], [0,0,0], [0,0,0], [0,0,0],
        [0,0,0], [0,0,0], [0,0,0], [0,0,0],
        [60,0,0], [0,0,0], [0,0,0], [0,0,0],
        [0,0,0], [0,0,0], [0,0,0], [0,0,0]],
        
        [[33,0,0], [0,0,0], [0,0,0], [0,0,0],
        [0,0,0], [0,0,0], [0,0,0], [0,0,0],
        [33,0,0], [0,0,0], [0,0,0], [0,0,0],
        [0,0,0], [0,0,0], [0,0,0], [0,0,0]],
        
        [[40,0,0], [0,0,0], [0,0,0], [0,0,0],
        [40,0,0], [0,0,0], [0,0,0], [0,0,0],
        [40,0,0], [0,0,0], [0,0,0], [0,0,0],
        [40,0,0], [0,0,0], [0,0,0], [0,0,0]]
        ]
#seq has 4 tracks that it might be currently playing
# seq array is [note (0-127), channel(0-15), CC ( 0xffff )  ]
# CC value is where first nybble (ff) is message, second nyble is value

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

midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1],
                          out_channel=(0))

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
OFF = (0,0,0)
PLAY = (0,10,0)
current_buttons = pad.get_pressed()
last_read = 0

display = board.DISPLAY

# Set text, font, and color
text = "ChrisLeeWoo"
font = terminalio.FONT
color = 0x0000FF

# Create the text label
text_area = label.Label(font, text="ChrisLeeWoo", color=0x6F9FAF)
# Set the location
text_area.x = 52
text_area.y = 52

def customwait(wait_time):
        start = time.monotonic()
        while time.monotonic() < (start + wait_time):
            pass
            

# Make the display context
splash = displayio.Group(max_size=10)
display.show(splash)

roundrect = RoundRect(40, 40, 90, 30, 10, fill=0x0, outline=0xAFAF00, stroke=6)
splash.append(roundrect)
splash.append(text_area)
# insert play startup sound here ######
customwait(1)



# Here are the screens to move through
file = displayio.Group(max_size=8)
song = displayio.Group(max_size=8)
mixgrid = displayio.Group(max_size=64)

menu0 = displayio.Group()
menu1 = displayio.Group(max_size=8)
menu2 = displayio.Group(max_size=8)

lbl_file = label.Label(font, text='File', color=0x808080, x=10, y=10)
file.append(lbl_file)
lbl_bank = label.Label(font, text='Bank 0 ', color=0xff9F00, x=2, y=20)
lbl_filename = label.Label(font, text='Name:                  ', color=0xff9F00, x=50, y=20)
file.append(lbl_bank)
file.append(lbl_filename)
lbl_file1 = label.Label(font, text='1 0 1 2 3 4 5 6 7 8 9', color=0xA09F00, x=1, y=40)
lbl_file2 = label.Label(font, text='2 0 1 2 3 4 5 6 7 8 9', color=0xA09F00, x=1, y=50)
lbl_file3 = label.Label(font, text='3 0 1 2 3 4 5 6 7 8 9', color=0xA09F00, x=1, y=60)
lbl_file4 = label.Label(font, text='4 0 1 2 3 4 5 6 7 8 9', color=0xA09F00, x=1, y=70)
file.append(lbl_file1)
file.append(lbl_file2)
file.append(lbl_file3)
file.append(lbl_file4)
lbl_filename.text = 'Name: '+current_filename

lbl_song = label.Label(font, text='Song', color=0x808080, x=10, y=10)
song.append(lbl_song)
lbl_song_page = label.Label(font, text='Page: 0 ', color=0xff9F00, x=2, y=20)
lbl_songname = label.Label(font, text='Name:              ', color=0xff9F00, x=50, y=20)
song.append(lbl_song_page)
song.append(lbl_songname)
lbl_songname.text = 'Name: '+current_songname

lbl_song1 = label.Label(font, text='1 0 0 0 0 0 0 0 0 0 0', color=0x108010, x=1, y=40)
lbl_song2 = label.Label(font, text='2 0 0 0 0 0 0 0 0 0 0', color=0x108010, x=1, y=50)
lbl_song3 = label.Label(font, text='3 0 0 0 0 0 0 0 0 0 0', color=0x108010, x=1, y=60)
lbl_song4 = label.Label(font, text='4 0 0 0 0 0 0 0 0 0 0', color=0x108010, x=1, y=70)
song.append(lbl_song1)
song.append(lbl_song2)
song.append(lbl_song3)
song.append(lbl_song4)

# menus at bottom of screen
lbl_menu0 = label.Label(font, text='                  ', color=0x00A000, x=20, y=120)
menu0.append(lbl_menu0)

menus = [[''],['Env','Note','Pan','Delay'],['Save','File','Song','BPM']]
menu_labels = []
char_width = 8
x_position = 5
for item in menus[1]:
    width = len(item) * char_width
    menu_label = label.Label(font, text=item, color=0x00A000, x=x_position, y=121)
    x_position += width
    menu1.append(menu_label)

x_position = 5
for item in menus[2]:
    width = len(item) * char_width
    menu_label = label.Label(font, text=item, color=0x00A080, x=x_position, y=121)
    x_position += width
    menu2.append(menu_label)

for m in range(35):
    # This initializes the array for the display grid
    blankness = label.Label(font, text="   ", color=0xff9Fff)
    mixgrid.append(blankness)

screen_rects = -1

for g in range(4):
        for h in range(4):
            screen_rects += 1
            gridsq = Rect( (51+25*g), (5+25*h), 25, 25, fill=0x0, outline=0x555555, stroke=1)
            mixgrid.pop(screen_rects)
            mixgrid.insert( (screen_rects) , gridsq)

mixgrid.append(menu0)
menu_hilite = Rect( 1, 115, width=30, height=13, fill=0x0, outline=0x808055, stroke=1)
display.show(mixgrid)

selection = Rect( (51), (5), 25, 25, outline=0xFFAA00, stroke=3)
mixgrid.pop(32)
mixgrid.insert(32,selection)
selected_cell = 0

gridbeat = Rect( (51), (5), 25, 25, outline=0xF00000, stroke=3)
mixgrid.pop(33)
mixgrid.insert(33, gridbeat)

lbl_bpm = label.Label(font, text=( "BPM: " + str(bpm) ), color=0x0f9Fff)  # Beats Per Minute
lbl_bpm.x = 1
lbl_bpm.y = 12
mixgrid.append(lbl_bpm)

lbl_track = label.Label(font, text=( "TRK: " + str(current_track+1) ), color=0x0f9Fff)  # current track number (MIDI channel)
lbl_track.x = 1
lbl_track.y = 24
mixgrid.append(lbl_track)

lbl_pattern = label.Label(font, text=( "PTN: " + str(current_pattern)), color=0x0f9Fff)
lbl_pattern.x = 1
lbl_pattern.y = 36
mixgrid.append(lbl_pattern)

lbl_level = label.Label(font, text=( "LVL: " + str(current_level) ), color=0x0f9Fff)
lbl_level.x = 1
lbl_level.y = 48
mixgrid.append(lbl_level)

lbl_effect = label.Label(font, text=( "EFF: " + str(current_effect) ), color=0x0f9Fff)
lbl_effect.x = 1
lbl_effect.y = 60
mixgrid.append(lbl_effect)

lbl_mode = label.Label(font, text='Note         ', color=0xFFFFFF)
lbl_mode.x = 5
lbl_mode.y = 80
mixgrid.append(lbl_mode)

def load_file(path): # load file into seq array
    global seq
    try:
        with open(path, "r") as file:
            map_csv_str = file.read()
            map_csv_lines = map_csv_str.replace("\r", "").split("\n")
            for n,line in enumerate(map_csv_lines):
                if n== 0:
                    continue #skip CSV header
                if len(line) > 3:
                    l = [int(i) for i in line.split(',')]
                    trk = l[0]
                    cell = l[1]
                    data = l[2:5]
                    seq[trk][cell] = data
        print('Loaded file:',path)
        lbl_mode.text = 'Loaded'
    except Exception as exc:
        lbl_mode.text = 'ERROR loading'
        error = exc
        print(error)
    
def save_file(path): # save seq array into a disk file
    try:
        with open(path, "w") as file:
            file.write("Track,Cell,Note,Channel,CC\n") # CSV header
            for t,trk in enumerate(seq):
                for c,cell in enumerate(trk):
                    file.write("{},{},{},{},{}\n".format(t,c,*seq[t][c]))
            print('Saved file:',path)
            lbl_mode.text = 'Saved'
    except Exception as exc:
        lbl_mode.text = 'ERROR saving'
        error = exc
        print(error)
        
    
def pixelocate_x(number):
    return 55 + 25 * ( number % 4 )

def pixelocate_y(number):
    if number < 4:
        return 16
    elif number < 8:
        return 16 + 25
    elif number < 12:
        return 16 + 25*2
    else: return 16 + 25*3

def set_grid_disp(note,spot):
    mixgrid.pop(spot+16)
    thing = label.Label(font, text=note, color=0xff9F00)
    thing.x = ( pixelocate_x(spot) )
    thing.y = ( pixelocate_y(spot) )
    #mixgrid 16 to 31
    mixgrid.insert(spot+16, thing)
    
def update_grid():
    for step in range(16):
        set_grid_disp(display_note(seq[current_track][step][0]), step)

def display_notes_playing(step):
    notes = ''
    for trk in range(0,MAX_TRACKS-1):
        notes += display_note(seq[trk][step][0])+' '
    mixgrid.pop(34)
    noteval = label.Label(font, text=notes, color=0x00FF00)  
    noteval.x = 5
    noteval.y = 108
    mixgrid.insert(34, noteval)

def sequencer(seq, beat, gridbeat, x):
    beatstep = x
    #gridbeat = Rect( (52), (5), 24, 24, outline=0xF00000, stroke=3)

    beatstep = selection_update('right',beatstep, gridbeat)

    #send MIDI for each track
    for trk in range(0,MAX_TRACKS-1):
        if seq[current_track][x][0] != 0:
            midi.send(NoteOn(seq[trk][x][0], 127, channel = seq[0][x][1]))

    # setting channel as x is just to prove we can switch channels or instruments for each step
    # fully supporting this means passing seq[] to sequencer fn includes
    # note number, midi channel, and any CC for that step as well
    customwait(beat)
    # MIDI Note off for each track
    for trk in range(0,MAX_TRACKS-1):
        if seq[current_track][x][0] != 0:
            midi.send(NoteOn(seq[trk][x][0], 0))


def selection_update(dir,current, type):
    if dir == 'left':
        if current % 4 != 0:     #0, 4, 8, 12
            type.x = type.x - 25
            current -= 1
            return current
        elif current == 0:
            return current
        else:
            type.x = type.x + 25 * 3
            type.y = type.y - 25
            current -= 1
            return current
    if dir == 'right':
        if current % 4 != 3:     #3, 7, 11, 15
            type.x = type.x + 25
            current += 1
            return current
        elif current == 15:
            type.x = 51
            type.y = 5
            current = 0
            return current
        else:
            type.x = type.x - 25 * 3
            type.y = type.y + 25
            current += 1
            return current
    if dir == 'up':
        if current > 3 :     #3, 7, 11, 15
            type.y = type.y - 25
            current -= 4
            return current
        elif current < 4:
            return current
        else:
            type.x = type.x - 25 * 3
            type.y = type.y + 25
            current += 1
            return current
    if dir == 'down':
        if current < 12:     #3, 7, 11, 15
            type.y = type.y + 25
            current += 4
            return current
        elif current > 11:
            return current
        else:
            type.x = type.x - 25 * 3
            type.y = type.y + 25
            current += 1
            return current

def set_bpm_mode(setting):
    bpm_mode = setting
    if bpm_mode:
        lbl_bpm.color = 0xFFFFFF
    else:
        lbl_bpm.color = 0x0f9Fff

def set_mode(setting):
    global mode
    print('set_mode:',setting)
    if mode != 'BPM' and setting == 'BPM':
        set_bpm_mode(True)
        mode = setting
        lbl_mode.text = setting
    else:
        set_bpm_mode(False)
        
        mode = setting
        lbl_mode.text = setting


def show_menu(current_menu):
    if current_menu == 1:
        mixgrid.remove(menu0)
        mixgrid.append(menu_hilite)
        mixgrid.append(menu1)

    elif current_menu == 2:
        mixgrid.remove(menu1)
        mixgrid.append(menu2)
    else:
        mixgrid.remove(menu2)
        mixgrid.append(menu0)
        mixgrid.remove(menu_hilite)

def hilite_menu_item(menu, item):
    global char_width
    if current_menu==0:
        return
    last_pos = 1
    pos=[last_pos]
    for menu_item in menus[menu]:
        width = len(menu_item) * char_width
        begin = width + last_pos
        last_pos = begin
        pos.append( begin)
    # move hilite to menu item
    print(item,menus[menu][item], 'X:',menu_hilite.x,'WIDTH:',width)
    width = len(menus[menu][item]) * char_width
    menu_hilite.width = width
    menu_hilite.x = pos[item]

def increment_menu_item(menu,direction):
    global current_menu_item
    if menu==0:
        return
    last = len(menus[menu])
    current_menu_item += direction
    if current_menu_item >= last:
        current_menu_item = 0
    if current_menu_item  < 0:
        current_menu_item = last-1
    hilite_menu_item(menu,current_menu_item)
    print('Menu:',menu,'Item:',current_menu_item)

def show_screen(screen_number):
    if screen_number == 0:
        # the main song screen, it should eventually show a pattern number in the grid
        display.show(mixgrid)
    elif screen_number == 1:
        display.show(file)
    elif screen_number == 2:
        display.show(song)
    elif screen_number == 3:
        display.show(instruments)
    elif screen_number == 3:
        display.show(settings)

def change_note(position, amount):
    note, channel, cc = seq[current_track][position]
    note += amount
    if note >=0 and note <=127:
        seq[current_track][position][0] = note
        set_grid_disp(display_note(note),position)
        print('change_note @',position, 'amount',amount,'note', note)
        
def increment_track(amount):
    global current_track
    print('inc_track ',amount)
    current_track += amount
    if current_track > (MAX_TRACKS-1):
        current_track = 0
    if current_track <0:
        current_track = (MAX_TRACKS-1)
    switch_track(current_track)    
    
def switch_track(track_num):
    lbl_track.text = "TRK: " + str(track_num+1)
    update_grid()
    
    
#### start up  
load_file(current_filename)
update_grid()

while True:
    if playing:
        gridbeat.outline = 0x009900
        sequencer (seq, beat, gridbeat, x)
        x = (x+1) % 16
        display_notes_playing(x)
    else:
        gridbeat.outline = 0xff0000

    # Reading buttons too fast returns 0
    if (last_read + 0.1) < time.monotonic():
        buttons = pad.get_pressed()
        last_read = time.monotonic()

    if current_buttons != buttons:
        # Respond to the buttons
        if (buttons & BUTTON_START) > 0 :
            if playing == False:
                playing = True
                print("playing")
            else:
                playing = False
                print("stopped")
            print('Start', buttons)
            
        if (buttons == BUTTON_SEL + BUTTON_UP > 0 ):
            print ("SEL + UP", buttons)
            increment_track(1)
        elif (buttons == BUTTON_SEL + BUTTON_DOWN > 0 ):
            print ("SEL + DOWN", buttons)
            increment_track(-1)
           
        elif (buttons == BUTTON_SEL + BUTTON_A): #
            customwait(.1)
            print ("SEL + A", buttons)
            
        elif (buttons & BUTTON_SEL) > 0 :
            current_menu += 1
            if current_menu >2:
                current_menu = 0
                set_mode('Note')
            else:
                set_mode(' ')
            if current_menu == 2:
                current_menu_item=0
                hilite_menu_item(current_menu, current_menu_item)
            print('SEL', buttons, 'menu:',current_menu)
            show_screen(0)
            show_menu(current_menu)

        elif (buttons == BUTTON_A + BUTTON_RIGHT > 0 ):
            print ("A + Right", buttons)
        elif (buttons == BUTTON_A + BUTTON_LEFT > 0 ):
            print ("A + Left", buttons)
        elif (buttons == BUTTON_A + BUTTON_UP > 0 ):
            print ("A + Up", buttons)
        elif (buttons == BUTTON_A + BUTTON_DOWN > 0 ):
            print ("A + Down", buttons)

        elif (buttons == BUTTON_B + BUTTON_RIGHT > 0 ):
            print ("B + Right", buttons)
            change_note(selected_cell,12)
        elif (buttons == BUTTON_B + BUTTON_LEFT > 0 ):
            print ("B + Left", buttons)
            change_note(selected_cell,-12)
        elif (buttons == BUTTON_B + BUTTON_UP > 0 ):
            print ("B + Up", buttons)
            change_note(selected_cell,1)
        elif (buttons == BUTTON_B + BUTTON_DOWN > 0 ):
            print ("B + Down", buttons)
            change_note(selected_cell,-1)
            
        elif (buttons & BUTTON_LEFT) > 0:
            print('Left ', end = '')
            if mode == 'Note':
                selected_cell = selection_update('left', selected_cell, selection)
                print('Cell:',selected_cell)
            else:
                increment_menu_item(current_menu,-1)

        elif (buttons & BUTTON_RIGHT) > 0:
            print('Right ', end = '')
            if mode == 'Note':
                selected_cell = selection_update('right', selected_cell, selection)
                print('Cell:',selected_cell)
            else:
                increment_menu_item(current_menu,1)

        elif (buttons & BUTTON_UP) > 0 :
            print('Up ', end = '')
            if mode == 'Note':
                selected_cell = selection_update('up', selected_cell, selection)
                print('Cell:',selected_cell)
            elif mode == 'BPM':
                bpm +=1
                if bpm > 300:
                    bpm = 300
                lbl_bpm.text = 'BPM:'+str(bpm)
            elif mode == 'ENV':
                current_level +=1
                if current_level > 127:
                    current_level = 0
                lbl_level.text = 'LVL:'+str(current_level)
            
            
        elif (buttons & BUTTON_DOWN) > 0 :
            print('Down ', end = '')
            if mode == 'Note':
                selected_cell = selection_update('down', selected_cell, selection)
                print('Cell:',selected_cell)
            elif mode == 'BPM':
                bpm -= 1
                if bpm < 1:
                    bpm=1
                lbl_bpm.text = 'BPM:'+str(bpm)
            elif mode == 'ENV':
                current_level -=1
                if current_level < 0:
                    current_level = 127
                lbl_level.text = 'LVL:'+str(current_level)
            
            
        elif (buttons & BUTTON_A) > 0 :
            print('A', buttons)

        elif (buttons & BUTTON_B) > 0 :
            print('B', end = '')
            if current_menu == 0:
                set_mode('Note')
            if current_menu == 1:
                if current_menu_item == 0: # ENV
                    set_mode('ENV')
                if current_menu_item == 1: # Note
                    set_mode('Note')
                if current_menu_item == 2: # PAN
                    set_mode('Pan')
                if current_menu_item == 3: # DELAY
                    set_mode('Delay')
            if current_menu == 2:
                if current_menu_item == 0: # Save
                    save_file(current_filename)
                elif current_menu_item == 1: # File
                    show_screen(1)
                elif current_menu_item == 2: # Song
                    show_screen(2)
                elif current_menu_item == 3: # BPM
                    set_mode('BPM')
            
        current_buttons = buttons
