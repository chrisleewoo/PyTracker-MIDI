# NanoLoop PyTracker

https://github.com/chrisleewoo/PyTracker-MIDI

This is a portable music tracker built for the adafruit PyBadge written in CircuitPython. 
Heavily inspired by Nanoloop. 

PLease use the latest STABLE Circuitpython release, at least 5.0, as the firmware for the board. 
  
## Current Functionality:
  * Outputs MIDI over USB cable to the host computer 
  * Moving left, right, up, and down are working, keeps you on the grid for easier navigation.
  * Sequence displays as stepped according to BPM.
  * 4 tracks - each outputs MIDI simultaneously - so 4 note polyphony.
  * save and load from a disk file (currently only one file with a fixed name: nan.csv) To be able to save, the filesystem must be writable. It is normally readonly. See boot.md and boot.py for details

## Usage
* START button: starts/stops the sequencer
* SELECT button: access menus - click to cycle through the 2 menus, and a blank "menu"
* Arrow buttons: move cursor to select one of the sixteen beats in the grid
* Hold the B button while using arrow buttons: Change note at selected beat.
  * Up = up one MIDI note
  * Down = down  one MIDI note
  * Right: up one octave
  * Left: down one octave
* Hold SELECT and press Up or Down to choose one of the 4 tracks.
* Press SELECT to access Menu 1, use LEFT, RIGHT to move to a menu item, press B to activate.
  * Env: Change the level (LVL) - probably should alter the MIDI velocity
  * Note: back to the grid for pattern editing
  * Pan: not implemented - probably should just alter a MIDI CC
  * Delay: not implemented - supposed to alter the Swing timing
 * Press SELECT again to access Menu2, RIGHT and LEFT to move to a menu item, press B to activate
   * Save - Save data in a disk file "nan.csv" (load happens automatically upon startup, if the file exists)
   * File - store a grid pattern in a bank - not implemented
   * Song - put grid patterns in order for a song -not implemented
   * BPM - set the Beats Per Minute - press B, then use UP and DOWN to change BPM
   
