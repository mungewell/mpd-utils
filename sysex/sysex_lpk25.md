
Search for device
```
$ amidi -p hw:1,0,0 -S 'F0 7e 00 06 01 f7' -r serial.bin
^C
$ hexdump -Cv serial.bin 
00000000  f0 7e 00 06 02 47 76 00  19 00 00 00 65 00 00 00  |.~...Gv.....e...|
00000010  00 00 01 01 01 01 01 01  01 01 01 11 11 11 11 11  |................|
00000020  11 11 f7                                          |...|
00000023
```


Recall preset 4, note have to change 'cmd 63' to '61' to allow uploading
```
$ amidi -p hw:1,0,0 -S 'F0 47 7f 76 63 00 01 04 F7' -r recall_4.lpk25
^C                                           ^^ preset to recall
21 bytes read
$ hexdump -Cv recall_4.lpk25 
00000000  f0 47 7f 76 63 00 0d 04  00 04 0c 00 04 05 00 00  |.G.vc...........|
00000010  03 00 78 00 f7                                    |..x..|
00000015
```


You can read back current/live settings from preset 0
but don't know how to write back as of yet... just locks up device
```
$ amidi -p hw:1,0,0 -S 'f0 47 7f 76 63 00 01 00 f7' -r temp.bin
^C
21 bytes read
simon@thevoid:~/mpd-utils-git/sysex$ hexdump -Cv temp.bin 
00000000  f0 47 7f 76 63 00 0d 00  00 00 00 00 00 00 00 00  |.G.vc...........|
00000010  02 01 70 00 f7                                    |..p..|
00000015
```


Check which preset is active on device
```
$ amidi -p hw:1,0,0 -S 'F0 47 7f 76 64 00 00 F7' -r temp.bin
^C
9 bytes read
$ hexdump -Cv temp.bin 
00000000  f0 47 7f 76 64 00 01 03  f7                       |.G.vd....|
00000009                       ^^ current preset
```


select preset
```
$ amidi -p hw:1,0,0 -S 'F0 47 7f 76 62 00 01 02 f7' -r temp.bin
^C                                           ^^ preset
0 bytes read



$ amidi -p hw:1,0,0 -S 'F0 47 7f 76 64 00 01 01 F7' -r temp.bin
^C
9 bytes read
$ hexdump -Cv temp.bin 
00000000  f0 47 7f 76 64 00 01 01  f7                       |.G.vd....|
00000009
$ amidi -p hw:1,0,0 -S 'F0 47 7f 76 62 00 01 02 f7' -r temp.bin
^C                                           ^^ preset


0 bytes read
$ amidi -p hw:1,0,0 -S 'F0 47 7f 76 64 00 01 01 F7' -r temp.bin
^C
9 bytes read
$ hexdump -Cv temp.bin 
00000000  f0 47 7f 76 64 00 01 02  f7                       |.G.vd....|
00000009                       ^^ has changed
```
