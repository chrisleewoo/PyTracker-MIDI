# PyTracker
This is a portable music tracker built for CircuitPython devices, specifically the Adafruit Pybadge and PyGamer platforms. Heavily inspired by LSDJ and Nanoloop. 

## Why did I write it in python? 
**Two reasons:**
  1. To show support for Adafruit's work in CircuitPython
  1. The ease of transferring save files/customizing the software with the PyBadge acting as USB mass storage.
  
The heavy lifting of audio output will be provided by a daughter board plugged into the feather headers on the back. This allows the ability to use different synthesis or sampling techniques by "switching out carts". Current development is focused on using the Groboards Giant Board <https://groboards.com/giant-board/>.

Please use the latest STABLE Circuitpython release, at least 5.0, as the firmware for the board. 

Not tested for PyGamer or EdgeBadge, I only have the OG PyBadge.

## Current Functionality:
  * Outputs MIDI over USB cable in the current version ( repeats a hardcoded loop ) 
  * Moving left, right, up, and down are working, keeps you on the grid for easier navigation.
  * Sequence displays as stepped according to BPM.
  
## Features Checklist:

 - [ ] Connect Groboards giantboard to recieve midi (USB? UART? SPI? RX/TX pins?)
 - [x] Test MIDI output on multiple channels
 - [x] menu navigation, change values in pattern arrays
 - [ ] impliment pages as displayio groups
   - [ ] song page
   - [x] pattern page
   - [ ] instrument page
   - [ ] settings page
-  [ ] envelope (ADSR), pitch bend and other MIDI CC per step
-  [ ] save/load songs (read and write to file)

## Usage
* START button: starts/stops the sequencer
* SELECT button: switches screens
* Arrow buttons: move cursor to select one of the sixteen beats
* Hold the B button while using arrow buttons: Change note at selected beat.
  * Up = up one MIDI note
  * Down = down  one MIDI note
  * Right: up one octave
  * Left: down one octave

