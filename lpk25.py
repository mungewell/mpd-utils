#!/usr/bin/python
#
# Script decode/encode configuration files for the Akai LPK25
# (c) Simon Wood, 8 July 2018
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
    Const(b"\x47\x7f"),             # Mfg ID = Akai
    Const(b"\x76"),                 # Dev ID = LPK25
    Const(b"\x61"),                 # CMD = Dump/Load Preset
    Const(b"\x00\x0d"),             # Len = 13bytes (7bit stuffed)

    "preset" / Byte,
    "channel" / Byte,
    "octave" / Enum(Byte,
        OCT_M4    = 0,
        OCT_M3    = 1,
        OCT_M2    = 2,
        OCT_M1    = 3,
        OCT_0     = 4,
        OCT_P1    = 5,
        OCT_P2    = 6,
        OCT_P3    = 7,
        OCT_P4    = 8,
        ),
    "transpose" / Enum(Byte,
        TRANS_M12 = 0,
        TRANS_M11 = 1,
        TRANS_M10 = 2,
        TRANS_M9  = 3,
        TRANS_M8  = 4,
        TRANS_M7  = 5,
        TRANS_M6  = 6,
        TRANS_M5  = 7,
        TRANS_M4  = 8,
        TRANS_M3  = 9,
        TRANS_M2  = 10,
        TRANS_M1  = 11,
        TRANS_0   = 12,
        TRANS_P1  = 13,
        TRANS_P2  = 14,
        TRANS_P3  = 15,
        TRANS_P4  = 16,
        TRANS_P5  = 17,
        TRANS_P6  = 18,
        TRANS_P7  = 19,
        TRANS_P8  = 20,
        TRANS_P9  = 21,
        TRANS_P10 = 22,
        TRANS_P11 = 23,
        TRANS_P12 = 24,
        ),
    "enable" / Default(Enum(Byte,
        OFF = 0,
        ON = 1,
        ), 0),
    "mode" / Enum(Byte,
        UP        = 0,
        DOWN      = 1,
        INCLUSIVE = 2,          # note: different order
        EXCLUSIVE = 3,          # to markings on keyboard
        RANDOM    = 4,
        ORDER     = 5,
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
    "clock" / Enum(Byte,
        INTERNAL = 0,
        EXTERNAL = 1,
        ),
    "latch" / Enum(Byte,
        DISABLE = 0,
        ENABLE  = 1,
        ),
    "taps" / Byte,
    "tempo" / ExprAdapter(Int16ub, # 7bit stuffed - each byte max 0x7F
        ((obj_ & 0x7f) + ((obj_ & 0x7f00) >> 1)),
        ((obj_ & 0x7f) + ((obj_ & 0x3f80) << 1)),
        ),
    "octaves" / Enum(Byte,
        OCT_1     = 0,
        OCT_2     = 1,
        OCT_3     = 2,
        OCT_4     = 3,
        ),
)

Footer = Struct(
    Const(b"\xf7"),                 # SysEx End
)

Lpk25 = Sequence(
    Header,
    Footer,
)


#--------------------------------------------------

config = None

def edit_arpeggio():
    global config

    menu = qprompt.Menu()
    for x,y in Header.enable.subcon.subcon.ksymapping.items():
        menu.add(str(x),y)
        if config[0]['enable'] == y:
            dft = str(x)
    config[0]['enable'] = int(menu.show(msg="Enable", dft=dft))

    menu = qprompt.Menu()
    for x,y in Header.division.subcon.ksymapping.items():
        menu.add(str(x),y)
        if config[0]['division'] == y:
            dft = str(x)
    config[0]['division'] = int(menu.show(msg="Division", dft=dft))

    menu = qprompt.Menu()
    for x,y in Header.mode.subcon.ksymapping.items():
        menu.add(str(x),y)
        if config[0]['mode'] == y:
            dft = str(x)
    config[0]['mode'] = int(menu.show(msg="Mode", dft=dft))

    menu = qprompt.Menu()
    for x,y in Header.latch.subcon.ksymapping.items():
        menu.add(str(x),y)
        if config[0]['latch'] == y:
            dft = str(x)
    config[0]['latch'] = int(menu.show(msg="Latch", dft=dft))

    menu = qprompt.Menu()
    for x,y in Header.octaves.subcon.ksymapping.items():
        menu.add(str(x),y)
        if config[0]['octaves'] == y:
            dft = str(x)
    config[0]['octaves'] = int(menu.show(msg="Octaves", dft=dft))

    config[0]['taps'] = \
        qprompt.ask_int("Taps", vld=list(range(2,4)),
            dft=config[0]['taps'])

    config[0]['tempo'] = \
        qprompt.ask_int("Tempo", dft=config[0]['tempo'])

    menu = qprompt.Menu()
    for x,y in Header.clock.subcon.ksymapping.items():
        menu.add(str(x),y)
        if config[0]['clock'] == y:
            dft = str(x)
    config[0]['clock'] = int(menu.show(msg="Clock", dft=dft))


def edit_general():
    global config

    config[0]['channel'] = \
        qprompt.ask_int("Midi Ch for Keys", dft=config[0]['channel'])

    menu = qprompt.Menu()
    for x,y in Header.octave.subcon.ksymapping.items():
        menu.add(str(x),y)
        if config[0]['octave'] == y:
            dft = str(x)
    config[0]['octave'] = int(menu.show(msg="Keyboard Octave", dft=dft))
    menu = qprompt.Menu()


def edit_transpose():
    global config

    menu = qprompt.Menu()
    for x,y in Header.transpose.subcon.ksymapping.items():
        menu.add(str(x),y)
        if config[0]['transpose'] == y:
            dft = str(x)
    config[0]['transpose'] = int(menu.show(msg="Transpose", dft=dft))


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

    if _hasQPrompt:
        parser.add_option("-A", "--arpeggio",
            help="Interactively configure the Arpeggiator",
            action="store_true", dest="arpeggio")
        parser.add_option("-G", "--general",
            help="Interactively configure general settings",
            action="store_true", dest="general")
        parser.add_option("-T", "--transpose",
            help="Interactively configure the Transposing",
            action="store_true", dest="transpose")

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("input FILE not specified")

    if options.verbose:
        print("Reading %s..." % args[0])

    infile = open(args[0], "rb")
    if not infile:
        print("Unable to open file")
        quit(0)

    data = infile.read(2000)
    try:
        config = Lpk25.parse(data)
    except:
        quit("Unable to read config file")
    infile.close()



    # Change stuff here...
    if options.preset:
        config[0]['preset'] = int(options.preset)
    if options.tempo:
        config[0]['tempo'] = int(options.tempo)

    if options.arpeggio:
        edit_arpeggio()
    if options.general:
        edit_general()
    if options.transpose:
        edit_transpose()


    if options.dump:
        print(config)

    if options.verbose:
        if options.outfile:
            print("writing %s..." % options.outfile)
        else:
            print("writing %s..." % args[0])

    if options.outfile:
        outfile = open(options.outfile, "wb")
    else:
        outfile = open(args[0], "wb")

    if not outfile:
        print("Unable to open output file")
    else:
        outfile.write(Lpk25.build(config))

if __name__ == "__main__":
    main()

