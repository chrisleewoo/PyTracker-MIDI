This is a portable music tracker built for CircuitPython devices, specifically the Adafruit Pybadge and PyGamer platforms. Heavily inspired by LSDJ and Nanoloop.

PLease use the latest STABLE Circuitpython release, at least 5.0, as the firmware for the board. 

Not tested for PyGamer or EdgeBadge, I only have the OG PyBadge.

Current Functionality:
  Outputs MIDI over USB cable in the current version ( repeats a hardcoded loop ) 
  Moving left, right, up, and down are working, keeps you on the grid for easier navigation.
  Sequence displays as stepped according to BPM.
  Can change midi channel per step in the sequence
  

Milestones:
TO DO

[] Connect Groboards giantboard to recieve midi (USB? UART?)

[] menu navigation 

[] impliment pages as displayio groups?

[] envelope (ADSR), pitch bend and other MIDI CC

[] save/load songs (read and write to file)


