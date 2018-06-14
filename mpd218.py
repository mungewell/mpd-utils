#!/usr/bin/python
#
# Script decode/encode configuration files for the Akai MPD218
# (c) Simon Wood, 13 June 2018
#

from optparse import OptionParser
from construct import *

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

def main():
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

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("input FILE not specified")

    if options.verbose:
        print("reading %s..." % args[0])

    infile = open(args[0], "rb")
    if not infile:
        print("Unable to open file")
        quit(0)

    data = infile.read(2000)
    config = Mpd218.parse(data)



    # Change stuff here...
    if options.preset:
        config[0]['preset'] = int(options.preset)
    if options.tempo:
        config[0]['tempo'] = int(options.tempo)



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

