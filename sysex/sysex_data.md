
# Program and Global Memory

Program and Global memory can be read via SysEx calls. Due to the 7bit
limit on the byte count value this has to done in chunks, the returned
data needs to be processed to remove header/footer.

[Disclaimer: very experimental, high risk of bricking device!!]

```
echo "Reading 'Program Memory' chunks (press ^C until done)"
amidi -p hw:1,0,0 -S 'F0 47 00 34 21 00 03 40 00 00 f7' -r Program1.bin
amidi -p hw:1,0,0 -S 'F0 47 00 34 21 00 03 40 00 40 f7' -r Program2.bin
amidi -p hw:1,0,0 -S 'F0 47 00 34 21 00 03 40 01 00 f7' -r Program3.bin
amidi -p hw:1,0,0 -S 'F0 47 00 34 21 00 03 40 01 40 f7' -r Program4.bin
amidi -p hw:1,0,0 -S 'F0 47 00 34 21 00 03 40 02 00 f7' -r Program5.bin
amidi -p hw:1,0,0 -S 'F0 47 00 34 21 00 03 40 02 40 f7' -r Program6.bin
amidi -p hw:1,0,0 -S 'F0 47 00 34 21 00 03 40 03 00 f7' -r Program7.bin
amidi -p hw:1,0,0 -S 'F0 47 00 34 21 00 03 40 03 40 f7' -r Program8.bin
amidi -p hw:1,0,0 -S 'F0 47 00 34 21 00 03 31 04 00 f7' -r Program9.bin

# Crude processing, leaves 0x7f at end
dd bs=64 count=1 skip=10 iflag=skip_bytes if=Program1.bin of=Program.bin
dd bs=64 count=1 skip=10 iflag=skip_bytes if=Program2.bin of=Program.bin seek=1
dd bs=64 count=1 skip=10 iflag=skip_bytes if=Program3.bin of=Program.bin seek=2
dd bs=64 count=1 skip=10 iflag=skip_bytes if=Program4.bin of=Program.bin seek=3
dd bs=64 count=1 skip=10 iflag=skip_bytes if=Program5.bin of=Program.bin seek=4
dd bs=64 count=1 skip=10 iflag=skip_bytes if=Program6.bin of=Program.bin seek=5
dd bs=64 count=1 skip=10 iflag=skip_bytes if=Program7.bin of=Program.bin seek=6
dd bs=64 count=1 skip=10 iflag=skip_bytes if=Program8.bin of=Program.bin seek=7
dd bs=64 count=1 skip=10 iflag=skip_bytes if=Program9.bin of=Program.bin seek=8

echo "Reading 'Global Memory' chunks (press ^C until done)"
amidi -p hw:1,0,0 -S 'F0 47 00 34 20 00 03 40 00 00 f7' -r Global1.bin
amidi -p hw:1,0,0 -S 'F0 47 00 34 20 00 03 40 00 40 f7' -r Global2.bin
amidi -p hw:1,0,0 -S 'F0 47 00 34 20 00 03 3b 01 00 f7' -r Global3.bin

# Crude processing, leaves 0x7f at end
dd bs=64 count=1 skip=10 iflag=skip_bytes if=Global1.bin of=Global.bin
dd bs=64 count=1 skip=10 iflag=skip_bytes if=Global2.bin of=Global.bin seek=1
dd bs=64 count=1 skip=10 iflag=skip_bytes if=Global3.bin of=Global.bin seek=2
```

# Summary of Global Memory

I am not sure how Program memory is used by the device, but Global memory
seems to be a store of the state of things and can be changed on the fly.

Changes to the Dial values will be reflected when the next midi data is 
sent. Changes the LEDs status will be visible immediately, but cancelled
when the button is pressed.

```
0x0,00: Device Mode (see below)
..
0x0,03: Full Level. 0x00=off, 0x01=on
0x0,04: Note repeat. 0x00=off, 0x01=on
..
0x0,07: LED mode. 0x00=Normal, 0x01=Preset, 0x02.. Div/Swing/Tempo
..
0x0,0d-0x0,1e: Set Dial values, CC/Aftertouch
0x0,1f-0x0,30: Set Dial values, repeated???
0x0,31-0x0,42: Dials, INC-DEC-1/2 mode. 0x01 clock, 0x7f anti-clock
0x0,43-0x0,54: Dials, INC-DEC-1/2 mode. 0x01 clock, 0x7f anti-clock

0x0,55-0x0,64: Read Button Pressure (0x1,2d below will stop notes/midi)

0x0,65-0x0,74: Force BankA LEDs. 0x00=off, 0x01 on.
0x0,75-0x1,04: Force BankB LEDs. 0x00=off, 0x01 on.
0x1,05-0x1,14: Force BankC LEDs. 0x00=off, 0x01 on.

0x1,15-0x1,24: Unknown, can set 0x00 or 0x01 (unused BankD LEDs?)

0x1,25: Preset. 0x00-0x0F
0x1,26: Pad Bank Select. 0x00=BankA, 0x01=BankB, 0x02=Bank3
0x1,27: Dial Bank Select. 0x00=BankA, 0x01=BankB, 0x02=Bank3
0x1,28: External Midi Clock. 0x00=off, 0x01=on

0x1,29: WARNING unit freaks out, might be minimum pressure for NoteOn. Only set=0x15
0x1,2a: Note Off level? default 0x11, 0x00 keeps LEDs on and no note off is sent
..
0x1,2d: MIDI sent, yes=0x00, no=0x01
..
0x1,3a:
```

## Device Mode
no LEDs/no Aftertouch pressure???
```
$ amidi -p hw:1,0,0 -S 'F0 47 00 34 30 00 04 01 00 00 01 F7'
```

Device sends 'polyphonic aftertouch/pressure' via SysEx
```
$ amidi -p hw:1,0,0 -S 'F0 47 00 34 30 00 04 01 00 00 20 F7'
or
$ amidi -p hw:1,0,0 -S 'F0 47 00 34 30 00 04 01 00 00 80 F7'
--
18296832: 0xf04700344300020c00f7
18296832: 0xf04700344300020c00f7
18297856: 0xf04700344300020c02f7
18297856: 0xd906
18297856: 0xf04700344300020c00f7
18297856: 0xd900
18297856: 0x893000
```

Continuous SysEx messages with polyphonic aftertouch/pressure
```
$ amidi -p hw:1,0,0 -S 'F0 47 00 34 30 00 04 01 00 00 40 F7'
--
          0xf0470034480003005500f7
75216896: 0xf0470034480003005600f7
75216896: 0xf0470034480003005700f7
75216896: 0xf0470034480003005800f7
75216896: 0xf0470034480003005900f7
75216896: 0xf0470034480003005a00f7
75216896: 0xf0470034480003005b00f7
75216896: 0xf0470034480003005c00f7
75216896: 0xf0470034480003005d00f7
75216896: 0xf0470034480003005e00f7
75216896: 0xf0470034480003005f00f7
75216896: 0xf0470034480003006000f7
75216896: 0xf0470034480003006100f7
75216896: 0xf0470034480003006200f7
75216896: 0xf0470034480003006300f7
75216896: 0xf0470034480003006400f7
and loops.....
```

# F/W and Serial

```
$ amidi -p hw:1,0,0 -S 'F0 7e 00 06 01 f7' -r serial.bin
^C
35 bytes read
$ hexdump -Cv serial.bin
00000000  f0 7e 00 06 02 47 34 00  19 00 01 00 01 00 00 7f  |.~...G4.........|
00000010  7f 7f 41 33 31 38 30 31  31 36 39 xx xx xx xx xx  |..A31801169xxxxx|
00000020  xx 00 f7                                          |x..|
00000023
```

http://www.akaipro.com/apc40map
says... which looks pretty similar.
```
1 0xF0 MIDI System exclusive message start
2 0x7E Non-Realtime Message
3 <MIDI Channel> Common MIDI channel setting
4 0x06 Inquiry Message
5 0x02 Inquiry Response
6 0x47 Manufacturers ID Byte
7 0x73 Product model ID
8 0x00 Number of data bytes to follow (most significant)
9 0x19 Number of data bytes to follow (least significant)
10 <Version1> Software version major most significant
...
13 <Version4> Software version minor least significant
14 <DeviceID> System Exclusive Device ID
15 <Serial1> Serial Number first digit
...
18 <Serial4> Serial Number fourth digit
19 <Manufacturing1> Manufacturing Data byte 1
...
34 <Manufacturing16> Manufacturing Data byte 16
35 0xF7  MIDI System exclusive message terminator
```


also see:
https://github.com/nsmith-/mpk2
