# mpd-utils

Scripts for configuring the Akai MPD218 Midi Pad Controller

The MPD218 is a small/low-cost MIDI pad controller, with touch sensitive
pads and dials. It can be used (with a PC/Laptop) as a drum machine or
a controller for a Digital Audio Workshop.

The configuration file is a propriatory format and specific to the MPD218.

'mpd218.py' is a command line application which can decode/encode the
configuration files. It may be possible to adjust/tailor the script
for other Akai devices.

Requires 'construct' (v2.9):
https://github.com/construct/construct

Using Construct allows the file format to be defined in one place, allowing
decoding/encoding from the same defination. The defination is precise and
fairly human readable.

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

## Optional features (require other Python 'libraries')

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

## Downloading from the device

This is a little more complicated, you need to send a sysex command
and store the response (note: this should be exactly 549 bytes). Changing
the last '01' (0x01..0x10) will download each of the 16 presets.

```
$ amidi -p hw:1,0,0 -S 'F0 47 00 34 12 00 01 01 F7' -r recall_1.mpd218
^C
549 bytes read
$ hexdump -Cv recall_1.mpd218
00000000  f0 47 00 34 10 04 1d 01  65 78 61 6d 70 6c 65 31  |.G.4....example1|
00000010  00 3c 04 32 00 09 24 01  01 00 00 00 00 09 25 01  |.<.2..$.......%.|
00000020  01 00 00 00 00 09 26 01  01 00 00 00 00 09 27 01  |......&.......'.|
00000030  01 00 00 00 00 09 28 01  01 00 00 00 00 09 29 01  |......(.......).|
00000040  01 00 00 00 00 09 2a 01  01 00 00 00 00 09 2b 01  |......*.......+.|
00000050  01 00 00 00 00 09 2c 01  01 00 00 00 00 09 2d 01  |......,.......-.|
00000060  01 00 00 00 00 09 2e 01  01 00 00 00 00 09 2f 01  |............../.|
00000070  01 00 00 00 00 09 30 01  01 00 00 00 00 09 31 01  |......0.......1.|
00000080  01 00 00 00 00 09 32 01  01 00 00 00 00 09 33 01  |......2.......3.|
00000090  01 00 00 00 00 09 34 01  01 00 00 00 00 09 35 01  |......4.......5.|
000000a0  01 00 00 00 00 09 36 01  01 00 00 00 00 09 37 01  |......6.......7.|
000000b0  01 00 00 00 00 09 38 01  01 00 00 00 00 09 39 01  |......8.......9.|
000000c0  01 00 00 00 00 09 3a 01  01 00 00 00 00 09 3b 01  |......:.......;.|
000000d0  01 00 00 00 00 09 3c 01  01 00 00 00 00 09 3d 01  |......<.......=.|
000000e0  01 00 00 00 00 09 3e 01  01 00 00 00 00 09 3f 01  |......>.......?.|
000000f0  01 00 00 00 00 09 40 01  01 00 00 00 00 09 41 01  |......@.......A.|
00000100  01 00 00 00 00 09 42 01  01 00 00 00 00 09 43 01  |......B.......C.|
00000110  01 00 00 00 00 09 44 01  01 00 00 00 00 09 45 01  |......D.......E.|
00000120  01 00 00 00 00 09 46 01  01 00 00 00 00 09 47 01  |......F.......G.|
00000130  01 00 00 00 00 09 48 01  01 00 00 00 00 09 49 01  |......H.......I.|
00000140  01 00 00 00 00 09 4a 01  01 00 00 00 00 09 4b 01  |......J.......K.|
00000150  01 00 00 00 00 09 4c 01  01 00 00 00 00 09 4d 01  |......L.......M.|
00000160  01 00 00 00 00 09 4e 01  01 00 00 00 00 09 4f 01  |......N.......O.|
00000170  01 00 00 00 00 09 50 01  01 00 00 00 00 09 51 01  |......P.......Q.|
00000180  01 00 00 00 00 09 52 01  01 00 00 00 00 09 53 01  |......R.......S.|
00000190  01 00 00 00 00 01 03 00  7f 00 00 01 00 01 09 00  |................|
000001a0  7f 00 00 02 00 01 0c 00  7f 00 00 03 00 01 0d 00  |................|
000001b0  7f 00 00 04 00 01 0e 00  7f 00 00 05 00 01 0f 00  |................|
000001c0  7f 00 00 06 00 01 10 00  7f 00 00 07 00 01 11 00  |................|
000001d0  7f 00 00 08 00 01 12 00  7f 00 00 09 00 01 13 00  |................|
000001e0  7f 00 00 0a 00 01 14 00  7f 00 00 0b 00 01 15 00  |................|
000001f0  7f 00 00 0c 00 01 16 00  7f 00 00 0d 00 01 17 00  |................|
00000200  7f 00 00 0e 00 01 18 00  7f 00 00 0f 00 01 19 00  |................|
00000210  7f 00 00 10 00 01 1a 00  7f 00 00 11 00 01 1b 00  |................|
00000220  7f 00 00 12 f7                                    |.....|
00000225
```

## Other Devices

MPK Mini (Mk1 and Mk2) now supported by 'mpk_mini.py' script. Presets
are number 1..4, setting 0 will result in config be uploaded to RAM 
and not stored as a preset.

Tested on MK2, Information for MK1 from:
https://github.com/gljubojevic/akai-mpk-mini-editor

It looks like several other Akai devices follow similar schemes, in
particular the MPD226, MPK-Mini (see above)  and MPK2. 

I got my hands on a MPD266, the preset structure is almost correct. You can
read presets from the device with (00 - current, 01-14 presets).
```
# amidi -p hw:1,0,3 -t 1 -S 'F0 47 00 35 12 00 01 00 F7' -r test.syx
```

Raise a bug if you'de like to see a similar script for your device...

