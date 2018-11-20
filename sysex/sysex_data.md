
# Retrieving Program and Global Memory

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

# Summary of Program Memory

It appears that the program memory is a reflection of the current patch active
on the unit, but in a different format. Where as the patch is grouped by pad
(or dial) settings, the program memory has specific settings (ie midi note)
grouped together.

Appart from this reformating they appear to be the same.




# Summary of Global Memory

Global memory seems to be a store of the 'state of things' and can be changed 
on the fly.

Changes forced to the Dial values will be reflected when the next midi data is 
sent. Changes forced the LEDs status will be visible immediately, but cancelled
when the button is pressed.

```
0x0,00: Device Mode (see below)
..
0x0,03: Full Level. 0x00=off, 0x01=on
0x0,04: Note repeat. 0x00=off, 0x01=on (no LED on MPD218)
..
0x0,07: Pad LEDs mode. 0x00=Normal, 0x01=ProgSelect (Preset #),
		0x02..= NRConfig (Div/Swing/Tempo)
..
0x0,0d-0x0,1e: Dial values, CC/Aftertouch
0x0,1f-0x0,30: Dial values, repeated???
0x0,31-0x0,42: Dials, INC-DEC-1/2 mode. 0x01 turned clock, 0x7f anti-clock
0x0,43-0x0,54: Dials, INC-DEC-1/2 mode. 0x01 turned clock, 0x7f anti-clock

0x0,55-0x0,64: Read Button Pressure (addr 0x1,2d below will stop notes/midi)

0x0,65-0x0,74: current Pad BankA LEDs. 0x00=off, 0x01 on.
0x0,75-0x1,04: current Pad BankB LEDs. 0x00=off, 0x01 on.
0x1,05-0x1,14: current Pad BankC LEDs. 0x00=off, 0x01 on.

0x1,15-0x1,24: Unknown, can set 0x00 or 0x01 (unused 'off' LED color?)

0x1,25: Current Preset. 0x00-0x0F.. = Preset 1..16
0x1,26: Pad Bank Select. 0x00=BankA, 0x01=BankB, 0x02=Bank3
0x1,27: Dial Bank Select. 0x00=BankA, 0x01=BankB, 0x02=Bank3
0x1,28: External Midi Clock. 0x00=off (use tap-tempo), 0x01=on

0x1,29: WARNING unit freaks out, might be minimum pressure for NoteOn. default=0x15
0x1,2a: Note Off level? default 0x11, 0x00 keeps LEDs on and no note off is sent
..
0x1,2c: Midi Common Channel? default 0x09 - normally pad/dial specific
0x1,2d: Midi Output?. USB=0x00, ?=0x01 (stops Notes/CC/etc, SysEx still to USB)
..
0x1,2f: Tap Average. 2-4 taps
..
0x1,32: ? default 0x32=50
..
0x1,3a:
```

Features supported on the MPD-226/MPD-232 which the MPD-218 firmware might support
```
16 level
extra pad bank
off colors for pads
repeat toggle mode (226/232 has LED to indicate)
repeat gate (1-99%, sequenced note duty factory)

midi to din - on/off, set for each pad/dial individually

midi common control ch (USB A1-16=1..16, DIN B1-16=17..32)


pad threshold (0-10)
velocity curve (Linear, Exp1, Exp2, Log1, and Log2)
pad gain (1-10)

tap average - number of taps needed 2-4
lock? - 0-off, 1-on
demo? - 0-off, 1-on
```


## Device Mode
Device mode appears to be set by Global addr 0x0,00

mode = 0x01 (or any bit0 set)
no pad LEDs, no bank LEDs, no full level LED (although full level mode works)
no Aftertouch pressure
pads issue note on/off, dials do not issue CCs
pad/dial bank select does not change issued notes (remains as previously set)
```
$ amidi -p hw:1,0,0 -S 'F0 47 00 34 30 00 04 01 00 00 01 F7'
```

mode = 0x02 (or any bit1 set)

Pad LEDs work, but Bank/Prog/Full/etc buttons do not function (LEDs and modes
remain as previously set).
Banks/Full/Repeat can still be set via SysEx.


mode = 0x08 (or any bit3 set)

Bank/Prog/Full/Config/Repeat button presses reported via SysEx
```
116779008: 0xf04700344000020501f7
116786176: 0xf04700344000020500f7
116900864: 0xf04700344000020401f7
116913152: 0xf04700344000020400f7
116944896: 0xf04700344000020301f7
116957184: 0xf04700344000020300f7
```


mode = 0x10 (or any bit4 set)

dial/encoder values reported via SysEx
```
123463680: 0xb00303
123463680: 0xf04700344100020044f7
123468800: 0xb00302
123468800: 0xf04700344100020043f7
123472896: 0xb00301
123472896: 0xf04700344100020042f7
123476992: 0xb00300
123476992: 0xf04700344100020041f7
123482112: 0xf04700344100020040f7
123490304: 0xf0470034410002003ff7
123496448: 0xf0470034410002003ef7
```

note: encoder value is not locked to CC value, and will continue/loop 
when CC reaches max. encoder number doesn't change with bank
```
128304128: 0xf04700344100020001f7
128307200: 0xf04700344100020000f7
128311296: 0xf0470034410002007ff7
128314368: 0xf0470034410002007ef7
128318464: 0xf0470034410002007df7
128323584: 0xf0470034410002007cf7
```

mode = 0x20 (or any bit5 set)

Device sends notes with 'polyphonic aftertouch/pressure' via SysEx
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

mode = 0x40
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

mode = 0x39

no LEDs lit, pads/dials/buttons reported via SysEx (use 0x1,2d to turn notes off).
This may be the route to 'proper' support within MPC Essentials/MPC2

# Device enquiry - F/W and Serial

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

also see:
https://github.com/nsmith-/mpk2

