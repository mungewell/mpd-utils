
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

