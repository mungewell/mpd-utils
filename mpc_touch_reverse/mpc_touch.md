Reverse engineering the MPC Touch

When connected to a Linux PC the device presents 2x USB devices (MPC Touch 
and DisplayLink Screen). Initial the LEDs are 'sweeping' left to right,
once the device enumerates on USB none of the buttons are illuminated.

The Touch device is a composite device containing HID, Audio and Midi devices.

The Display device functions with DisplayLink driver for Windows and Linux.

The 1st of the Midi devices ('Public' in Windows, 'MPC Touch MIDI 1' in 
Linux)  will send Note/CC packets (for all buttons and dials), and it also
responds to SysEx commands/requests.

Strangely the 'Private' Midi interface is not listed in Windows

Note: once connected to MPC software in Windows, none of the Midi ports are
connected or sending button presses - suggesting that comms to MPC software
is happening via the USB HID port.
