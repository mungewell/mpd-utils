'''
Work around for the lack of MPD218 driver in MPC Essentials, many
functions within DAW do not support control via MIDI notes.

This python script detects notes (from MPC preset, BankC) and issue
keyboard presses to the active window, which do drive the functions
within MPC Essentials

It 'shims' between MPD218 and MPC essentials, relaying the Midi and
keypresses. The keypresses are only detected from BankC enable user
to easily enable/disable.

Requires:
https://www.lfd.uci.edu/~gohlke/pythonlibs/#rtmidi-python
https://github.com/olemb/mido
https://github.com/boppreh/keyboard

Setup:
Install the above, or use the pre-built binary

Install the 'Akai Internal MIDI Port' located within MPC directory
C:\Program Files\Akai Pro\MPC Essentials\support

In MPC Essentials, under Edit/Preferences/Midi set a Midi-Output 
to 'Akai Internal MIDI'.

Run script/exe in command window and then switch back to MPC
'''
import sys
import mido

print("MPC Key Check")
inport = None

#mido.set_backend('mido.backends.rtmidi_python')
print(mido.get_input_names())

for port in mido.get_input_names():
  if port[:26]=='MPC Touch:MPC Touch MIDI 1':
    inport = port
    print("Using:", inport)
    break

if inport == None:
  sys.exit("Unable to find MPC 'Public'")

with mido.open_input(inport) as port:
  for message in port:
    print(message)
