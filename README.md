# mpd-utils

Scripts for configuring the Akai MPD218 Midi Pad Controller

Requires 'construct' (v2.9)
https://github.com/construct/construct

Adjusted config files can be uploaded (on Linux) with the Alsa tools
```
$ amidi -l
Dir Device    Name
IO  hw:1,0,0  MPD218 MIDI 1

$ python3 mpd218.py -d test.mpd218  | grep tempo
        tempo = 128
$ python3 mpd218.py -t 30 -o temp.mpd218 test.mpd218
$ python3 mpd218.py -d temp.mpd218  | grep tempo
        tempo = 30
$ amidi -p hw:1,0,0 -s temp.mpd218
```
