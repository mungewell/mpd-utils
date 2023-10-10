
echo "Reading 'Program Memory' chunks (press ^C until done)"
amidi -p hw:2,0,3 -S 'F0 47 00 35 21 00 03 40 00 00 f7' -r Program1.bin
amidi -p hw:2,0,3 -S 'F0 47 00 35 21 00 03 40 00 40 f7' -r Program2.bin
amidi -p hw:2,0,3 -S 'F0 47 00 35 21 00 03 40 01 00 f7' -r Program3.bin
amidi -p hw:2,0,3 -S 'F0 47 00 35 21 00 03 40 01 40 f7' -r Program4.bin
amidi -p hw:2,0,3 -S 'F0 47 00 35 21 00 03 40 02 00 f7' -r Program5.bin
amidi -p hw:2,0,3 -S 'F0 47 00 35 21 00 03 40 02 40 f7' -r Program6.bin
amidi -p hw:2,0,3 -S 'F0 47 00 35 21 00 03 40 03 00 f7' -r Program7.bin
amidi -p hw:2,0,3 -S 'F0 47 00 35 21 00 03 40 03 40 f7' -r Program8.bin
amidi -p hw:2,0,3 -S 'F0 47 00 35 21 00 03 40 04 00 f7' -r Program9.bin
amidi -p hw:2,0,3 -S 'F0 47 00 35 21 00 03 40 04 40 f7' -r ProgramA.bin
amidi -p hw:2,0,3 -S 'F0 47 00 35 21 00 03 40 05 00 f7' -r ProgramB.bin
amidi -p hw:2,0,3 -S 'F0 47 00 35 21 00 03 40 05 40 f7' -r ProgramC.bin
amidi -p hw:2,0,3 -S 'F0 47 00 35 21 00 03 40 06 00 f7' -r ProgramD.bin
amidi -p hw:2,0,3 -S 'F0 47 00 35 21 00 03 40 06 40 f7' -r ProgramE.bin
amidi -p hw:2,0,3 -S 'F0 47 00 35 21 00 03 40 07 00 f7' -r ProgramF.bin
amidi -p hw:2,0,3 -S 'F0 47 00 35 21 00 03 40 07 40 f7' -r ProgramG.bin
amidi -p hw:2,0,3 -S 'F0 47 00 35 21 00 03 40 08 00 f7' -r ProgramH.bin

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
dd bs=64 count=1 skip=10 iflag=skip_bytes if=ProgramA.bin of=Program.bin seek=9 
dd bs=64 count=1 skip=10 iflag=skip_bytes if=ProgramB.bin of=Program.bin seek=10
dd bs=64 count=1 skip=10 iflag=skip_bytes if=ProgramC.bin of=Program.bin seek=11
dd bs=64 count=1 skip=10 iflag=skip_bytes if=ProgramD.bin of=Program.bin seek=12
dd bs=64 count=1 skip=10 iflag=skip_bytes if=ProgramE.bin of=Program.bin seek=13
dd bs=64 count=1 skip=10 iflag=skip_bytes if=ProgramF.bin of=Program.bin seek=14
dd bs=64 count=1 skip=10 iflag=skip_bytes if=ProgramG.bin of=Program.bin seek=15
dd bs=64 count=1 skip=10 iflag=skip_bytes if=ProgramH.bin of=Program.bin seek=16

echo "Reading 'Global Memory' chunks (press ^C until done)"
amidi -p hw:2,0,3 -S 'F0 47 00 35 20 00 03 40 00 00 f7' -r Global1.bin
amidi -p hw:2,0,3 -S 'F0 47 00 35 20 00 03 40 00 40 f7' -r Global2.bin
amidi -p hw:2,0,3 -S 'F0 47 00 35 20 00 03 40 01 00 f7' -r Global3.bin
amidi -p hw:2,0,3 -S 'F0 47 00 35 20 00 03 40 01 40 f7' -r Global4.bin

# Crude processing, leaves 0x7f at end
dd bs=64 count=1 skip=10 iflag=skip_bytes if=Global1.bin of=Global.bin
dd bs=64 count=1 skip=10 iflag=skip_bytes if=Global2.bin of=Global.bin seek=1 
dd bs=64 count=1 skip=10 iflag=skip_bytes if=Global3.bin of=Global.bin seek=2 
dd bs=64 count=1 skip=10 iflag=skip_bytes if=Global4.bin of=Global.bin seek=3 

