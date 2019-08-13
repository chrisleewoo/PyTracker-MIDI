This is a portable music tracker built for CircuitPython devices, specifically the Adafruit Pybadge and PyGamer platforms. Heavily inspired by LSDJ and Nanoloop.

The project is still in the very early stages of development and will change when new APIs become available, but so far it looks quite possible.

Includes the waveform generator files from the Adafruit Learning System, with just minor tweaks.

Unfortunately, I could not get the 4 channels of waves to mix without overloading memory or outputting just a pop. This will be revisited if circuitpython gets a mixer implimented.

For now, I will continue to make this as a midi controller and sequencer, which still proves to be quite fun to mess with! Adafruit has already provided what I need to get started, and the main works. The older one is on here for posterity.

Moving left and right are working, keeps you on the grid for easier navigation

Milestones:
TO DO

[] wave mixing (ON HOLD)

[] move cursor, menu navigation 

[] impliment pages as displayio groups?

[] envelope (ADSR)

[] tempo control, should be (1/BPM/60) seconds for each step 

[] save/load songs (read and write to file)

