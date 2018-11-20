
Device enquiry
```
$ amidi -p hw:1,0,0 -S 'F0 7e 00 06 01 f7' -r serial.bin
^C
34 bytes read
$ hexdump -Cv serial.bin 
00000000  f0 7e 00 06 02 47 26 00  19 00 22 00 22 00 00 00  |.~...G&..."."...|
00000010  00 00 00 00 04 00 04 00  03 00 78 00 2c 2d 2e 2f  |..........x.,-./|
00000020  30 f7                                             |0.|
00000022
```

Knob position enquiry - the values for the 8 knobs will be reported as 0..0x7F values.
```
simon@thevoid:~/mpd-utils-git/sysex$ amidi -p hw:1,0,0 -S 'F0 47 00 26 60 00 03 00 00 01 f7' -r temp.bin
^C
16 bytes read
simon@thevoid:~/mpd-utils-git/sysex$ hexdump -Cv temp.bin 
00000000  f0 47 00 26 61 00 08 00  00 00 00 00 00 00 00 f7  |.G.&a...........|
00000010
simon@thevoid:~/mpd-utils-git/sysex$ amidi -p hw:1,0,0 -S 'F0 47 00 26 60 00 03 00 00 10 f7' -r temp.bin
^C
16 bytes read
simon@thevoid:~/mpd-utils-git/sysex$ hexdump -Cv temp.bin 
00000000  f0 47 00 26 61 00 08 00  00 00 00 00 00 00 00 f7  |.G.&a...........|
00000010
simon@thevoid:~/mpd-utils-git/sysex$ amidi -p hw:1,0,0 -S 'F0 47 00 26 60 f7' -r temp.bin ; hexdump -Cv temp.bin 
^C
16 bytes read
00000000  f0 47 00 26 61 00 08 00  00 00 00 00 00 00 00 f7  |.G.&a...........|
00000010
```

All knobs turned down to minimum
```
$ amidi -p hw:1,0,0 -S 'F0 47 00 26 60 f7' -r temp.bin ; hexdump -C temp.bin
^C
16 bytes read
00000000  f0 47 00 26 61 00 08 00  00 00 00 00 00 00 00 f7  |.G.&a...........|
00000010
```

All knobs turned up to maximum
```
$ amidi -p hw:1,0,0 -S 'F0 47 00 26 60 f7' -r temp.bin ; hexdump -C temp.bin
^C
16 bytes read
00000000  f0 47 00 26 61 00 08 7f  7f 7f 7f 7f 7f 7f 7f f7  |.G.&a...........|
00000010
```

select preset
```
$ amidi -p hw:1,0,0 -S 'F0 47 00 26 62 00 01 02 f7' -r temp.bin
^C                                           ^^ preset to select
0 bytes read
```

Normally cmd 0x64 is used to upload a preset to the device, as per config file.

Malformed writes can corrupt presets, nothing is returned by keyboard crashes and 
preset is 'bad' on next boot/read
```
$ amidi -p hw:1,0,0 -S 'F0 47 00 26 64 00 01 00 F7' -r temp.bin
```

This appears to be the command to read back the presets (0x00=ram, 0x01..0x04), however note that
'cmd 0x67' is not the same as the official presets, and these don't upload with tweaking
it to '0x64'
```
$ amidi -p hw:1,0,0 -S 'F0 47 00 26 66 00 01 04 F7' -r recall_4.mpk2
^C                                           ^^ preset to recall
117 bytes read
$ hexdump -Cv recall_4.mpk2 
00000000  f0 47 00 26 67 00 6d 04  09 00 04 01 03 04 00 01  |.G.&g.m.........|
00000010  00 03 01 00 01 00 00 00  02 1e 1f 3c 00 00 00 3d  |...........<...=|
00000020  01 01 00 3e 02 02 00 3f  03 03 00 40 04 04 00 41  |...>...?...@...A|
00000030  05 05 00 42 06 06 00 43  07 07 00 44 08 08 00 45  |...B...C...D...E|
00000040  09 09 00 46 0a 0a 00 47  0b 0b 00 48 0c 0c 00 49  |...F...G...H...I|
00000050  0d 0d 00 4a 0e 0e 00 4b  0f 0f 00 14 00 7f 15 00  |...J...K........|
00000060  7f 16 00 7f 17 00 7f 18  00 7f 19 00 7f 1a 00 7f  |................|
00000070  1b 00 7f 0c f7                                    |.....|
00000075
```

report current preset
```
$ amidi -p hw:1,0,0 -S 'F0 47 00 26 68 00 00 F7' -r temp.bin
^C
9 bytes read
$ hexdump -Cv temp.bin 
00000000  f0 47 00 26 69 00 01 01  f7                       |.G.&i....|
                               ^^ current program
00000009
```

