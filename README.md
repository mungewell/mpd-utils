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
  -M SCALE, --scale=SCALE
                        Interactively configure multiple Pads as a scale
```

## Uploading to the device

The configuration file is actually a SysEx 'code plug' and can be
uploaded (on Linux) with the ALSA tools. The configuration will
be loaded into it's specified preset ('-p PRESET' as configured above).

If the preset is current one, changes to configurations are imediately
active on the device. A little oddly current dial values persist between
preset changes (even if they are now being directed somewhere else).
```
$ amidi -l
Dir Device    Name
IO  hw:1,0,0  MPD218 MIDI 1

$ amidi -p hw:1,0,0 -s example.mpd218
```

Optionally the settings for Pads/Dials can be interactively editted.
Requires:
https://github.com/jeffrimko/Qprompt

Example:
```
$ python3 mpd218.py -P 1 example.mpd218 
-- MENU: Pad 1 (Bank A-1): --
  (0) NOTE
  (1) PROG
  (2) BANK
[?] Type [0]: 
[?] Channel [10]: 
[?] Note [36]: 
-- MENU --
  (0) MOMENTARY
  (1) TOGGLE
[?] Trigger [0]: 
-- MENU --
  (0) OFF
  (1) CHANNEL
  (2) POLY
[?] Aftertouch [1]: 
```

Optionally multiple Pads can be programmed as a scale.
Requires:
https://github.com/charlottepierce/music_essentials

Example:
```
$ python3 mpd218.py -v -M 1 -o scale.mpd218 example.mpd218
Reading example.mpd218...
-- MENU: Pad 1 (Bank A-1): --
  (0) major
  (1) maj
  (2) minor
  (3) min
  (4) natural minor
  (5) nat min
  (6) melodic minor
  (7) dorian
  (8) locrian
  (9) lydian
  (10) mixolydian
  (11) phrygian
  (12) major pentatonic
  (13) minor pentatonic
  (14) chromatic
[?] Scale: 0
[?] Note [36]: 
[?] Count [0]: 
[?] Config all as per Pad 1? [n]: y
Setting Pad 1 (Bank A-1) to 36 (C2)
Setting Pad 2 (Bank A-2) to 38 (D2)
Setting Pad 3 (Bank A-3) to 40 (E2)
Setting Pad 4 (Bank A-4) to 41 (F2)
Setting Pad 5 (Bank A-5) to 43 (G2)
Setting Pad 6 (Bank A-6) to 45 (A2)
Setting Pad 7 (Bank A-7) to 47 (B2)
Setting Pad 8 (Bank A-8) to 48 (C3)
writing scale.mpd218...
```


## Other Devices

It looks like several other Akai devices follow similar schemes, in
particular the MPD226, MPK-Mini and MPK2. Raise a bug if you'de like
to see a similar script for your device...

https://github.com/gljubojevic/akai-mpk-mini-editor
https://github.com/nsmith-/mpk2

