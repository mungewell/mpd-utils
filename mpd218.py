#!/usr/bin/python
#
# Script decode/encode configuration files for the Akai MPD218
# (c) Simon Wood, 13 June 2018
#

from optparse import OptionParser
from construct import *

#--------------------------------------------------
# For interactive menus (optional)
# https://github.com/jeffrimko/Qprompt

try:
   import qprompt
   _hasQPrompt = True
except ImportError:
   _hasQPrompt = False
'''
_hasQPrompt = False
'''

#--------------------------------------------------
# Define file format using Construct (v2.9)
# https://github.com/construct/construct

Header = Struct(
    Const(b"\xf0"),                 # SysEx Begin
    Const(b"\x47\x00\x34"),         # Mfg ID
    Const(b"\x10"),
    Const(b"\x04\x1d"),

    "preset" / Byte,
    "name" / PaddedString(8, "utf8"),

    # Weird encoding, low byte is only 7 bit, valid 30..300
    "tempo" / ExprAdapter(Int16ub,
        ((obj_ & 0x7f) + ((obj_ & 0x0f00) >> 1)),
        ((obj_ & 0x7f) + ((obj_ & 0x0780) << 1)),
        ),

    "division" / Enum(Byte,
        DIV_1_4   = 0,
        DIV_1_4T  = 1,
        DIV_1_8   = 2,
        DIV_1_8T  = 3,
        DIV_1_16  = 4,
        DIV_1_16T = 5,
        DIV_1_32  = 6,
        DIV_1_32T = 7,
        ),
    "swing" / Enum(Byte,            # This could be byte value
        SWING_OFF = 50,
        SWING_54  = 54,
        SWING_56  = 56,
        SWING_58  = 58,
        SWING_60  = 60,
        SWING_62  = 62,
        ),
    )

Pad = Struct(
    "type" / Enum(Byte,
        NOTE = 0,
        PROG = 1,
        BANK = 2,
        ),
    "channel" / Byte,
    "note" /Byte,                   # NOTE only
    "trigger" / Enum(Byte,          # NOTE only
        MOMENTARY = 0,
        TOGGLE = 1,
        ),
    "aftertouch" / Enum(Byte,       # NOTE only
        OFF = 0,
        CHANNEL = 1,
        POLY = 2,
        ),
    "program" / Byte,               # PROG only
    "msb" / Byte,                   # BANK only
    "lsb" /Byte,                    # BANK only
)

Dial = Struct(
    "type" / Enum(Byte,
        CC = 0,
        AFTERTOUCH = 1,
        INC_DEC_1 = 2,
        INC_DEC_2 = 3,
        ),
    "channel" / Byte,
    "midicc" /Byte,                 # CC and ID2 only
    "min" /Byte,                    # CC and AT only
    "max" /Byte,                    # CC and AT only
    "msb" / Byte,                   # ID1 only
    "lsb" /Byte,                    # ID1 only
    "value" / Byte,                 # ID1 only
)

Footer = Struct(
    Const(b"\xf7"),                 # SysEx End
)

Mpd218 = Sequence(
    Header,
    Array(3, Array(16, Pad,)),
    Array(3, Array(6, Dial,)),
    Footer,
)

#--------------------------------------------------

config = None

def edit_division():
    global config

    menu = qprompt.Menu()
    for x,y in Header.division.subcon.ksymapping.items():
        menu.add(str(x),y)
    config[0]['division'] = int(menu.show())

def edit_swing():
    global config

    menu = qprompt.Menu()
    for x,y in Header.swing.subcon.ksymapping.items():
        menu.add(str(x),y)
    config[0]['swing'] = int(menu.show())

def edit_dial(dial):
    global config

    bank = int((dial-1) / 6)
    subdial = dial-(6*bank)-1
    print("Editing Dial %d (Bank %s-%d):" %
        (dial, chr(65+bank), subdial+1))

    menu = qprompt.Menu()
    for x,y in Dial.type.subcon.ksymapping.items():
        menu.add(str(x),y)
    ptype = menu.show()
    config[2][bank][subdial]['type'] = int(ptype)

    config[2][bank][subdial]['channel'] = \
        qprompt.ask_int("Enter the 'Channel'", vld=range(1,17))

    if ptype == '0' or ptype == '2':
        config[2][bank][subdial]['midicc'] = \
            qprompt.ask_int("Enter the 'MidiCC'", vld=range(0,128))

    if ptype == '0' or ptype == '1':
        config[2][bank][subdial]['min'] = \
            qprompt.ask_int("Enter the 'Min'", vld=range(0,128))
        config[2][bank][subdial]['max'] = \
            qprompt.ask_int("Enter the 'Max'", vld=range(0,128))

    if ptype == '3':
        config[2][bank][subdial]['msb'] = \
            qprompt.ask_int("Enter the 'MSB'", vld=range(0,128))
        config[2][bank][subdial]['lsb'] = \
            qprompt.ask_int("Enter the 'LSB'", vld=range(0,128))
        config[2][bank][subdial]['value'] = \
            qprompt.ask_int("Enter the 'Value'", vld=range(0,128))

def edit_pad(pad):
    global config

    bank = int((pad-1) / 16)
    subpad = pad-(16*bank)-1
    print("Editing Pad %d (Bank %s-%d):" %
        (pad, chr(65+bank), subpad+1))

    menu = qprompt.Menu()
    for x,y in Pad.type.subcon.ksymapping.items():
        menu.add(str(x),y)
    ptype = menu.show()
    config[1][bank][subpad]['type'] = int(ptype)

    config[1][bank][subpad]['channel'] = \
        qprompt.ask_int("Enter the 'Channel'", vld=range(1,17))

    if ptype == '0':
        config[1][bank][subpad]['note'] = \
            qprompt.ask_int("Enter the 'Note'", vld=range(0,128))

        menu = qprompt.Menu()
        for x,y in Pad.trigger.subcon.ksymapping.items():
            menu.add(str(x),y)
        config[1][bank][subpad]['trigger'] = int(menu.show())

        menu = qprompt.Menu()
        for x,y in Pad.aftertouch.subcon.ksymapping.items():
            menu.add(str(x),y)
        aftertouch = menu.show()
    elif ptype == '1':
        config[1][bank][subpad]['program'] = \
            qprompt.ask_int("Enter the 'Program'", vld=range(0,128))
    else:
        config[1][bank][subpad]['msb'] = \
            qprompt.ask_int("Enter the 'MSB'", vld=range(0,128))
        config[1][bank][subpad]['lsb'] = \
            qprompt.ask_int("Enter the 'LSB'", vld=range(0,128))

def main():
    global config

    usage = "usage: %prog [options] FILENAME"
    parser = OptionParser(usage)
    parser.add_option("-o", "--output", dest="outfile",
        help="write data to OUTFILE")
    parser.add_option("-v", "--verbose",
        action="store_true", dest="verbose")
    parser.add_option("-d", "--dump",
        help="dump configuration to text",
        action="store_true", dest="dump")

    parser.add_option("-p", "--preset", dest="preset",
        help="change the profile number to PRESET" )
    parser.add_option("-t", "--tempo", dest="tempo",
        help="change the tempo to TEMPO" )
    parser.add_option("-n", "--name", dest="name",
        help="change the profile name to NAME")

    if _hasQPrompt:
        parser.add_option("-X", "--division",
            help="Interactively change the Division",
            action="store_true", dest="division")
        parser.add_option("-S", "--swing",
            help="Interactively change the Swing",
            action="store_true", dest="swing")
        parser.add_option("-D", "--dial", dest="dial",
            help="Interactively configure a Dial")
        parser.add_option("-P", "--pad", dest="pad",
            help="Interactively configure a Pad" )

    (options, args) = parser.parse_args()

    if len(args) != 1 and not options.outfile:
        parser.error("input FILE not specified")

    if options.verbose:
        if len(args) == 1:
            print("reading %s..." % args[0])
        else:
            print("reading %s..." % options.outfile)

    if len(args) != 1:
        infile = open(options.outfile, "rb")
    else:
        infile = open(args[0], "rb")
    if not infile:
        print("Unable to open file")
        quit(0)

    data = infile.read(2000)
    config = Mpd218.parse(data)
    infile.close()



    # Change stuff here...
    if options.preset:
        config[0]['preset'] = int(options.preset)
    if options.tempo:
        config[0]['tempo'] = int(options.tempo)
    if options.name:
        config[0]['name'] = options.name[:8]

    if options.division:
        edit_division()
    if options.swing:
        edit_swing()
    if options.dial:
        edit_dial(int(options.dial))
    if options.pad:
        edit_pad(int(options.pad))


    if options.dump:
        print(config)

    if options.outfile:
        if options.verbose:
            print("writing %s..." % options.outfile)
        outfile = open(options.outfile, "wb")
        if not outfile:
            print("Unable to open output file")
        else:
            outfile.write(Mpd218.build(config))

if __name__ == "__main__":
    main()

