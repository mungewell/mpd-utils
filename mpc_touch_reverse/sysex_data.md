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

