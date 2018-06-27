As there are no preset files provide by Akai, these are read back from each 
program following a firmware update (MPKmini2_Firmware_Updatev0.022.zip).

http://www.akaipro.com/products/keyboard-controllers/mpk-mini-mkii

Altered to set the 'preset' parameter appropriately, so that they can be 
directly uploaded with:
$ amidi -p hw:1,0,0 -s preset1.mk2
