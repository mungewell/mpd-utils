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
# For programming scales (optional)
# https://github.com/charlottepierce/music_essentials

try:
   from music_essentials import Note,Scale
   _hasME = True
except ImportError:
   _hasME = False
'''
_hasME = False
'''

#--------------------------------------------------
# Define file format using Construct (v2.9)
# https://github.com/construct/construct

_PADS = 8
_DIALS = 8

Header = Struct(
    Const(b"\xf0"),                 # SysEx Begin
    Const(b"\x47\x7f"),             # Mfg ID = Akai
    Const(b"\x75"),                 # Dev ID = LPD8
    Const(b"\x61"),                 # CMD = Dump/Load Preset
    Const(b"\x00\x3a"),             # Len = 13bytes (7bit stuffed)

    "preset" / Byte,
    "channel" / Byte,
)

Pad = Struct(
    "note" /Byte,
    "program" / Byte,
    "midicc" /Byte,
    "trigger" / Enum(Byte,
        MOMENTARY = 0,
        TOGGLE = 1,
        ),
)

Dial = Struct(
    "midicc" /Byte,
    "min" /Byte,
    "max" /Byte,
)

Footer = Struct(
    Const(b"\xf7"),                 # SysEx End
)

Lpd8 = Sequence(
    Header,
    Array(_PADS, Pad,),
    Array(_DIALS, Dial,),
    Footer,
)


#--------------------------------------------------

config = None

def edit_general():
    global config

    config[0]['channel'] = \
        qprompt.ask_int("Midi Ch for Keys", dft=config[0]['channel'])

    menu = qprompt.Menu()

def edit_dial(dial):
    global config

    config[1][dial]['midicc'] = \
        qprompt.ask_int("CC", vld=list(range(0,128)),
            dft=config[1][dial]['midicc'])

    config[1][dial]['max'] = \
        qprompt.ask_int("Max", vld=list(range(0,128)),
            dft=config[1][dial]['max'])

    config[1][dial]['min'] = \
        qprompt.ask_int("Min", vld=list(range(0,128)),
            dft=config[1][dial]['min'])

def edit_pad(pad):
    global config

    config[1][pad]['note'] = \
        qprompt.ask_int("Note", vld=list(range(0,128)),
            dft=config[1][pad]['note'])

    menu = qprompt.Menu()
    config[1][pad]['program'] = \
        qprompt.ask_int("Program", vld=list(range(0,128)),
            dft=config[1][pad]['program'])

    config[1][pad]['midicc'] = \
        qprompt.ask_int("CC", vld=list(range(0,128)),
            dft=config[1][pad]['midicc'])

    config[1][pad]['trigger'] = \
        qprompt.ask_int("Trigger", vld=list(range(0,2)),
            dft=config[1][pad]['trigger'])

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
    parser.add_option("-c", "--channel", dest="channel",
        help="change the channel number to CHANNEL" )

    if _hasQPrompt:
        parser.add_option("-D", "--dial", dest="dial",
            help="Interactively configure a Dial")
        parser.add_option("-P", "--pad", dest="pad",
            help="Interactively configure a Pad" )

        if _hasME:
            parser.add_option("-M", "--scale", dest="scale",
                help="Interactively configure multiple Pads as a scale" )

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
        config = Lpd8.parse(data)
    except:
        quit("Unable to read config file")
    infile.close()



    # Change stuff here...
    if options.preset:
        config[0]['preset'] = int(options.preset)

    if options.channel:
        config[0]['channel'] = int(options.channel)

    if options.dump:
        print(config)

    if options.dial:
        edit_dial(int(options.dial))
    if options.pad:
        edit_pad(int(options.pad))

    '''
    if options.scale:
        edit_scale(int(options.scale), options.verbose)
    '''


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
        outfile.write(Lpd8.build(config))

if __name__ == "__main__":
    main()

