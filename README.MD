This is a portable music tracker built for CircuitPython devices, specifically the Adafruit Pybadge and PyGamer platforms. Heavily inspired by LSDJ and Nanoloop.

Hardware in the foreseeable future consists of the adafruit pybadge(or compatible variants) and the fluxamasynth midi add-on board for sound generation. The fluxamasynth examples are written in cpp, but we can make it work with circuitpython since it takes standard midi protocol. 

https://github.com/fluxly/Fluxamasynth

Moving left and right are working, keeps you on the grid for easier navigation.

Sequence displays as stepped according to BPM.

Milestones:
TO DO

[] Connect fluxashield and provide pictures for it

[] Match displayed sequence with midi note vals

[] move cursor, menu navigation 

[] impliment pages as displayio groups?

[] envelope (ADSR)

[] save/load songs (read and write to file)


