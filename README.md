# mpd-utils

Scripts for configuring the Akai MPD218 Midi Pad Controller

Requires 'construct' (v2.9)
https://github.com/construct/construct

The MPD218 is a small/low-cost MIDI pad controller, with touch sensitive
pads and dials. It can be used (with a PC/Laptop) as a drum machine or
a controller for a Digital Audio Workshop.

'mpd219.py' is a command line application which can decode/encode the
configuration files from Akai's MPD218 Editor (Windows application).

The file is a propriatory format and specific to the MPD218. It may
be possible to adjust/tailor the script for other Akai devices.
```
$ python3 mpd218.py -h
Usage: mpd218.py [options] FILENAME

Options:
  -h, --help            show this help message and exit
  -o OUTFILE, --output=OUTFILE
                        write data to OUTFILE
  -v, --verbose         
  -d, --dump            dump configuration to text
  -p PRESET, --preset=PRESET
                        change the profile number to PRESET
  -t TEMPO, --tempo=TEMPO
                        change the tempo to TEMPO
  -n NAME, --name=NAME  change the profile name to NAME
  -X, --division        Interactively change the Division
  -S, --swing           Interactively change the Swing
  -D DIAL, --dial=DIAL  Interactively configure a Dial
  -P PAD, --pad=PAD     Interactively configure a Pad
```

The configuration file is actually a SysEx 'code plug' and can be
uploaded (on Linux) with the ALSA tools. The configuration will
be loaded into it's specified preset (as configured above)
```
$ amidi -l
Dir Device    Name
IO  hw:1,0,0  MPD218 MIDI 1

$ amidi -p hw:1,0,0 -s example.mpd218
```
