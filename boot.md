Normally, when the PyBadge is connected to a host computer via USB,
only the host computer can write files to the PyBadge's flash memory filesystem.
This is to prevent corruption of the filesystem by clashes between two different writers.

You can change this so that the PyBadge fisesystem is only writable by
the PyBadge itself and not the host computer, by running some code in a file named: boot.py

boot.py runs only when you power on the PyBadge. It needs to be copied to the root
of the CIRCUITPY drive (right next to the usual code.py)

The boot.py provided here checks to see if any buttons are pressed when the PyBadge is
powered on. If you are holding down any button when you turn on the power switch
the PyBadge filesystem will be set to be writeable by the PyBadge, but not writeable by
the host computer. Now you can run code that writes files to the PyBadge's filesystem.
