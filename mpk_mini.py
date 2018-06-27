#!/usr/bin/python
#
# Script decode/encode configuration files for the Akai MPK Mk1 and Mk2
# (c) Simon Wood, 25 June 2018
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
# Constants defining MPK features

_PADS = 8
_PBANKS = 2
_PTOTAL = _PADS * _PBANKS

_DIALS = 8
_DBANKS = 1
_DTOTAL = _DIALS * _DBANKS

#--------------------------------------------------
# Define file format using Construct (v2.9)
# https://github.com/construct/construct

Header = Struct(
    "preset" / Byte,
    "pchannel" / Byte,              # Pads
    "dchannel" / Byte,              # Dials and Keys

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
    )

Arpeggio_enable = Struct(
    "enable" / Default(Enum(Byte,
        OFF = 0,
        ON = 1,
        ), 0),
    )
Arpeggio_mode = Struct(
    "mode" / Enum(Byte,
        UP        = 0,
        DOWN      = 1,
        EXCLUSIVE = 2,
        INCLUSIVE = 3,
        RANDOM    = 4,
        ORDER     = 5,
        ),
    )
Arpeggio_div = Struct(
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
    )
Arpeggio_clk = Struct(
    "clock" / Enum(Byte,
        INTERNAL = 0,
        EXTERNAL = 1,
        ),
    )
Arpeggio = Struct(
    "latch" / Enum(Byte,
        DISABLE = 0,
        ENABLE  = 1,
        ),
    "swing" / Enum(Byte,
        SWING_50  = 0,
        SWING_55  = 1,
        SWING_57  = 2,
        SWING_59  = 3,
        SWING_61  = 4,
        SWING_64  = 5,
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

Joy = Struct(                       # Default values allow Mk1->Mk2 conversion
    "axis_x" / Default(Enum(Byte,
        PBEND = 0,
        CC1   = 1,
        CC2   = 2,
        ), 0),
    "x_up" / Default(Byte, 0),
    "x_down" / Default(Byte, 1),    # CC2 only
    "axis_y" / Default(Enum(Byte,
        PBEND = 0,
        CC1   = 1,
        CC2   = 2,
        ), 1),
    "y_up" / Default(Byte, 1),
    "y_down" / Default(Byte, 1),    # CC2 only
)

Pad = Struct(
    "note" /Byte,
    "midicc" / Byte,
    "prog" / Byte,
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

Transpose = Struct(                 # Default values allow Mk1->Mk2 conversion
    "transpose" / Default(Enum(Byte,
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
        ), 12),
    )

Empty = Struct(                     # Hack for Mk1 -> MK2 conversion
)

Footer = Struct(
    Const(b"\xf7"),                 # SysEx End
)

Header_Mk1 = Struct(
    Const(b"\xf0"),                 # SysEx Begin
    Const(b"\x47\x7f"),             # Mfg ID = Akai
    Const(b"\x7c"),                 # Dev ID = MPK Mk1
    Const(b"\x61"),                 # CMD = Dump/Load Preset
    Const(b"\x00\x66"),             # Len = 102bytes (7bit stuffed)

    Embedded(Header),               # Note: different order
    Embedded(Transpose),
    Embedded(Arpeggio_clk),
    Embedded(Arpeggio_div),
    Embedded(Arpeggio_mode),
    Embedded(Arpeggio),
    )

Header_Mk2 = Struct(
    Const(b"\xf0"),                 # SysEx Begin
    Const(b"\x47\x00"),             # Mfg ID = Akai
    Const(b"\x26"),                 # Dev ID = MPK Mk2
    Const(b"\x64"),                 # CMD = Dump/Load Preset
    Const(b"\x00\x6d"),             # Len = 109bytes (7bit stuffed)

    Embedded(Header),               # Note: different order to Mk1
    Embedded(Arpeggio_enable),
    Embedded(Arpeggio_mode),
    Embedded(Arpeggio_div),
    Embedded(Arpeggio_clk),
    Embedded(Arpeggio),
    Embedded(Joy),
    )

Mpk_mk1 = Sequence(
    Header_Mk1,
    Array(_PBANKS, Array(_PADS, Pad,)),
    Array(_DBANKS, Array(_DIALS, Dial,)),
    Empty,
    Footer,
)

Mpk_mk2 = Sequence(
    Header_Mk2,
    Array(_PBANKS, Array(_PADS, Pad,)),
    Array(_DBANKS, Array(_DIALS, Dial,)),
    Transpose,
    Footer,
)


#--------------------------------------------------

config = None

def edit_division():
    global config

    menu = qprompt.Menu()
    for x,y in Header.division.subcon.ksymapping.items():
        menu.add(str(x),y)
        if config[0]['division'] == y:
            dft = str(x)
    config[0]['division'] = int(menu.show(msg="Division", dft=dft))

def edit_swing():
    global config

    menu = qprompt.Menu()
    for x,y in Header.swing.subcon.ksymapping.items():
        menu.add(str(x),y)
        if config[0]['swing'] == y:
            dft = str(x)
    config[0]['swing'] = int(menu.show(msg="Swing", dft=dft))

def edit_dial(dial):
    global config

    bank = int((dial-1) / _DIALS)
    subdial = dial-(_DIALS * bank)-1

    menu = qprompt.Menu()
    for x,y in Dial.type.subcon.ksymapping.items():
        menu.add(str(x),y)
        if config[2][bank][subdial]['type'] == y:
            dft = str(x)
    dtype = int(menu.show(hdr="Dial %d (Bank %s-%d):" % (dial, chr(65+bank), subdial+1),
        msg="Type", dft=dft))
    config[2][bank][subdial]['type'] = dtype

    config[2][bank][subdial]['channel'] = \
        qprompt.ask_int("Channel", vld=list(range(0,17)),
            dft=config[2][bank][subdial]['channel'])

    if dtype == 0 or dtype == 3:    # CC or ID2
        config[2][bank][subdial]['midicc'] = \
            qprompt.ask_int("MidiCC", vld=list(range(0,128)),
                dft=config[2][bank][subdial]['midicc'])

    if dtype == 0 or dtype == 1:    # CC or AT
        config[2][bank][subdial]['min'] = \
            qprompt.ask_int("Min", vld=list(range(0,128)),
                dft=config[2][bank][subdial]['min'])
        config[2][bank][subdial]['max'] = \
            qprompt.ask_int("Max", vld=list(range(0,128)),
                dft=config[2][bank][subdial]['max'])

    if dtype == 2:                    # ID1
        config[2][bank][subdial]['msb'] = \
            qprompt.ask_int("MSB", vld=list(range(0,128)),
                dft=config[2][bank][subdial]['msb'])
        config[2][bank][subdial]['lsb'] = \
            qprompt.ask_int("LSB", vld=list(range(0,128)),
                dft=config[2][bank][subdial]['lsb'])
        config[2][bank][subdial]['value'] = \
            qprompt.ask_int("Value", vld=list(range(0,128)),
                dft=config[2][bank][subdial]['value'])

def edit_pad(pad):
    global config

    bank = int((pad-1) / _PADS)
    subpad = pad-(_PADS * bank)-1

    menu = qprompt.Menu()
    for x,y in Pad.type.subcon.ksymapping.items():
        menu.add(str(x),y)
        if config[1][bank][subpad]['type'] == y:
            dft = str(x)
    ptype = menu.show(hdr="Pad %d (Bank %s-%d):" % (pad, chr(65+bank), subpad+1),
        msg="Type", dft=dft)
    config[1][bank][subpad]['type'] = int(ptype)

    config[1][bank][subpad]['channel'] = \
        qprompt.ask_int("Channel", vld=list(range(1,17)),
            dft=config[1][bank][subpad]['channel'])

    if ptype == '0':
        config[1][bank][subpad]['note'] = \
            qprompt.ask_int("Note", vld=list(range(0,128)),
                dft=config[1][bank][subpad]['note'])

        menu = qprompt.Menu()
        for x,y in Pad.trigger.subcon.ksymapping.items():
            menu.add(str(x),y)
            if config[1][bank][subpad]['trigger'] == y:
                dft = str(x)
        config[1][bank][subpad]['trigger'] = int(menu.show(msg="Trigger", dft=dft))

        menu = qprompt.Menu()
        for x,y in Pad.aftertouch.subcon.ksymapping.items():
            menu.add(str(x),y)
            if config[1][bank][subpad]['aftertouch'] == y:
                dft = str(x)
        config[1][bank][subpad]['aftertouch'] = int(menu.show(msg="Aftertouch", dft=dft))
    elif ptype == '1':
        config[1][bank][subpad]['program'] = \
            qprompt.ask_int("Program", vld=list(range(0,128)),
                dft=config[1][bank][subpad]['note'])
    else:
        config[1][bank][subpad]['msb'] = \
            qprompt.ask_int("MSB", vld=list(range(0,128)),
                dft=config[1][bank][subpad]['msb'])
        config[1][bank][subpad]['lsb'] = \
            qprompt.ask_int("LSB", vld=list(range(0,128)),
                dft=config[1][bank][subpad]['lsb'])

def edit_scale(pad, verbose):
    global config

    rbank = int((pad-1) / _PADS)
    rsubpad = pad-(_PADS * rbank)-1

    ptype = config[1][rbank][rsubpad]['type']
    if ptype == "BANK":
        qprompt.error("Pad %d (Bank %s-%d) is configured as a BANK" % (pad, chr(65+rbank), rsubpad+1))
        return

    menu = qprompt.Menu()
    x = 0
    for y in Scale._SCALE_PATTERNS:
        menu.add(str(x),y)
        x = x + 1
    stype = menu.show(hdr="Pad %d (Bank %s-%d):" % (pad, chr(65+rbank), rsubpad+1),
        msg="Scale", returns="desc")
    
    root = qprompt.ask_int("Note", vld=list(range(0,128)),
        dft=config[1][rbank][rsubpad]['note'])

    count = qprompt.ask_int("Count", vld=[0]+list(range(1,_PTOTAL+2-pad)), dft=0)

    same = qprompt.ask_yesno(msg="Config all as per Pad %d?" % pad, dft='N')

    scale = Scale.build_scale(Note.from_midi_num(root), stype)
    scale_lst = []
    for note in scale:
        scale_lst.append(note.midi_note_number())

    if count:
        while len(scale_lst) < count:
            root = scale_lst.pop()
            scale = Scale.build_scale(Note.from_midi_num(root), stype)
            for note in scale:
                scale_lst.append(note.midi_note_number())
    else:
        count = len(scale_lst)
        if pad + count > _PTOTAL:
            count = _PTOTAL + 1 - pad

    for note in scale_lst[:count]:
        bank = int((pad-1) / _PADS)
        subpad = pad-(_PADS * bank)-1

        if same and ptype == "NOTE":
            config[1][bank][subpad]['type'] = config[1][rbank][rsubpad]['type']
            config[1][bank][subpad]['channel'] = config[1][rbank][rsubpad]['channel']
            config[1][bank][subpad]['trigger'] = config[1][rbank][rsubpad]['trigger']
            config[1][bank][subpad]['aftertouch'] = config[1][rbank][rsubpad]['aftertouch']

        if same and ptype == "PROG":
            config[1][bank][subpad]['type'] = config[1][rbank][rsubpad]['type']
            config[1][bank][subpad]['channel'] = config[1][rbank][rsubpad]['channel']

        if ptype == "NOTE":
            config[1][bank][subpad]['note'] = note
        else:
            config[1][bank][subpad]['program'] = note

        if verbose:
            print("Setting Pad %d (Bank %s-%d) to %d (%s)" %
            (pad, chr(65+bank), subpad+1, note, Note.from_midi_num(note)))
        pad = pad + 1

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

    '''
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

        if _hasME:
            parser.add_option("-M", "--scale", dest="scale",
                help="Interactively configure multiple Pads as a scale" )
    '''

    # These should be mutally exclusive
    parser.add_option("-1", "--mk1",
        help="write configuration in mk1 format",
        action="store_true", dest="mk1")
    parser.add_option("-2", "--mk2",
        help="write configuration in mk2 format",
        action="store_true", dest="mk2")

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
    # Attempt to read Mk2 format, fall back to Mk1
    try:
        config = Mpk_mk2.parse(data)
        if not options.mk1:
            options.mk2 = True
    except:
        try:
            config = Mpk_mk1.parse(data)
            if not options.mk2:
                options.mk1 = True
        except:
            quit("Unable to read config file")
    infile.close()



    # Change stuff here...
    if options.preset:
        config[0]['preset'] = int(options.preset)
    if options.tempo:
        config[0]['tempo'] = int(options.tempo)

    '''
    if options.division:
        edit_division()
    if options.swing:
        edit_swing()
    if options.dial:
        edit_dial(int(options.dial))
    if options.pad:
        edit_pad(int(options.pad))

    if options.scale:
        edit_scale(int(options.scale), options.verbose)
    '''


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
        if options.mk1:
            outfile.write(Mpk_mk1.build(config))
        elif options.mk2:
            outfile.write(Mpk_mk2.build(config))

if __name__ == "__main__":
    main()

