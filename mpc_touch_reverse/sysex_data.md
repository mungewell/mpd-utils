Responds to 'all call'
--
simon@thevoid:~/mpd-utils-git/mpc_touch_reverse$ amidi -p hw:1,0,0 -S 'F0 7e 00 06 01 f7' -r serial.bin
^C
35 bytes read
simon@thevoid:~/mpd-utils-git/mpc_touch_reverse$ hexdump -C serial.bin 
00000000  f0 7e 00 06 02 47 37 00  19 00 01 00 06 00 00 00  |.~...G7.........|
00000010  00 00 41 31 31 35 31 32  xx xx xx xx xx xx xx xx  |..A11512xxxxxxxx|
00000020  33 00 f7                                          |3..|
00000023
--

Unit also sends a 'powering off' message
--
00000000  f0 47 00 37 64 00 03 02  00 01 f7                 |.G.7d......|
--


ahh, a kink in the shield
--
simon@thevoid:~/mpd-utils-git/mpc_touch_reverse$ amidi -p hw:1,0,0 -S 'f0 47 00 37 64 00 01 01 f7' -r serial.bin
^C
11 bytes read
simon@thevoid:~/mpd-utils-git/mpc_touch_reverse$ hexdump -C serial.bin 
00000000  f0 47 00 37 64 00 03 01  f7 01 f7                 |.G.7d......|
0000000b
--

--
simon@thevoid:~/mpd-utils-git/mpc_touch_reverse$ amidi -p hw:1,0,0 -S 'f0 47 00 37 50 00 03 01 00 01 f7' -r serial.bin
^C
40 bytes read
simon@thevoid:~/mpd-utils-git/mpc_touch_reverse$ !hexdump
hexdump -C serial.bin 
00000000  f0 47 00 37 51 00 20 0e  01 0e 0f 07 09 0c 05 06  |.G.7Q. .........|
00000010  09 04 06 0f 0e 05 03 01  00 01 f7 f7 00 00 00 00  |................|
00000020  00 00 00 00 00 00 00 f7                           |........|
00000028
--

$ amidi -p hw:1,0,0 ...
--
00000000  f0 47 00 37 51 00 20 09  0a 03 0f 00 0e 02 0e 06  |.G.7Q. .........|
00000010  08 08 0c 0b 02 0c 09 f7  00 00 f7 f7 00 00 00 00  |................|
00000020  00 00 00 00 00 00 00 f7                           |........|
00000028
00000000  f0 47 00 37 5a 00 20 00  00 07 08 00 01 00 00 00  |.G.7Z. .........|
00000010  00 00 01 02 00 00 00 00  00 00 00 04 00 00 00 00  |................|
00000020  00 00 04 00 00 00 00 f7                           |........|
00000028
00000000  f0 47 00 37 64 00 03 f7  00 00 f7                 |.G.7d......|
0000000b
--

$ amidi -p hw:1,0,1 ...
--
00000000  f0 47 00 37 51 00 20 0b  08 0e 00 0b 03 07 0d 0b  |.G.7Q. .........|
00000010  0d 03 05 0b 07 01 06 f7  f7 01 f7 00 00 00 00 00  |................|
00000020  00 00 00 00 00 00 00 f7                           |........|
00000028
00000000  f0 47 00 37 53 00 05 f7  f7 01 f7 02 f7           |.G.7S........|
0000000d
--

produces continuous note on/off events
--
$ amidi -p hw:1,0,0 -S 'f0 47 00 37 5a 00 02 00 01 f7'
--

cause screen backlight to flash on (just once, after power on)
--
$ amidi -p hw:1,0,0 -S 'f0 47 00 37 64 00 03 00 01 02 f7' 
--

Turn display off
--
$ amidi -p hw:2,0,0 -S 'f0 47 00 37 64 00 03 00 01 00 f7'
--

Turn display on
--
$ amidi -p hw:2,0,0 -S 'f0 47 00 37 64 00 03 00 01 01 f7'
--



$ amidi -p hw:2,0,0 -S 'f0 47 00 37 5a 00 20 00 00 07 08 00 01 00 00 00 00 00 01 02 00 00 00 00 00 00 00 04 00 00 00 00 00 00 04 00 00 00 00 f7'
