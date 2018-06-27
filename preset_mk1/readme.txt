Factory Deault Presets provided by Akai.

http://www.akaipro.com/products/legacy/mpk-mini

Converted to binary blobs with:
$ python3 convert_to_mk1.py Preset1-Chromatic

They can be directly uploaded with:
$ amidi -p hw:1,0,0 -s Preset1-Chromatic.mk1
