#!/usr/bin/python
#
# Script decode/encode configuration files for the Akai MPK Play
# (c) Simon Wood, 22 Dec 2018
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

_DIALS = 4
_DBANKS = 2
_DTOTAL = _DIALS * _DBANKS

#--------------------------------------------------
# Define file format using Construct (v2.9)
# https://github.com/construct/construct

General = Struct(
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
)

Dial = Struct(
    "midicc" /Byte,
    "min" /Byte,
    "max" /Byte,
)

Transpose = Struct(
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

Play_sounds = Struct(
    "keys" / Byte,
    "drums" / Byte,

    "filter" / Byte,
    "res" / Byte,
    "reverb" / Byte,
    "chorus" / Byte,

    "attack" / Byte,
    "release" / Byte,
    "eq_low" / Byte,
    "eq_high" / Byte,
    )
'''
    "keys" / Enum(Byte,
        PIANO     = 0,
        LAST      = 127,
        ),
    "drums" / Enum(Byte,
        STANDARD  = 0,
        LAST      = 9,
        ),
'''

Footer = Struct(
    Const(b"\xf7"),                 # SysEx End
)

Header = Struct(
    Const(b"\xf0"),                 # SysEx Begin
    Const(b"\x47\x7f"),             # Mfg ID = Akai
    Const(b"\x44"),                 # Dev ID = MPK Mini Play
    Const(b"\x64"),                 # CMD = Dump/Load Preset
    Const(b"\x00\x63"),             # Len = 99bytes (7bit stuffed)
                                    # Note: doesn't match actual size...

    Embedded(General),              # Note: different order to Mk1

    Embedded(Arpeggio_enable),
    Embedded(Arpeggio_mode),
    Embedded(Arpeggio_div),
    Embedded(Arpeggio_clk),
    Embedded(Arpeggio),
    Embedded(Joy),
)

Mpk_Play = Sequence(
    Header,
    Array(_PBANKS, Array(_PADS, Pad,)),
    Array(_DBANKS, Array(_DIALS, Dial,)),
    Transpose,
    Play_sounds,
    Footer,
)


#--------------------------------------------------

config = None

def edit_arpeggio():
    global config

    if config[0]['mk2']:
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

    menu = qprompt.Menu()
    for x,y in Header.swing.subcon.ksymapping.items():
        menu.add(str(x),y)
        if config[0]['swing'] == y:
            dft = str(x)
    config[0]['swing'] = int(menu.show(msg="Swing", dft=dft))

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

    config[0]['pchannel'] = \
        qprompt.ask_int("Midi Ch for Pads", dft=config[0]['pchannel'])

    config[0]['dchannel'] = \
        qprompt.ask_int("Midi Ch for Dials/Keys", dft=config[0]['dchannel'])

    menu = qprompt.Menu()
    for x,y in Header.octave.subcon.ksymapping.items():
        menu.add(str(x),y)
        if config[0]['octave'] == y:
            dft = str(x)
    config[0]['octave'] = int(menu.show(msg="Keyboard Octave", dft=dft))
    menu = qprompt.Menu()


def edit_joy():
    global config

    menu = qprompt.Menu()
    for x,y in Header.axis_x.subcon.subcon.ksymapping.items():
        menu.add(str(x),y)
        if config[0]['axis_x'] == y:
            dft = str(x)
    config[0]['axis_x'] = int(menu.show(msg="Axis-X", dft=dft))
    menu = qprompt.Menu()

    config[0]['x_up'] = \
        qprompt.ask_int("X-Up", dft=config[0]['x_up'])

    config[0]['x_down'] = \
        qprompt.ask_int("X-Down", dft=config[0]['x_down'])

    for x,y in Header.axis_y.subcon.subcon.ksymapping.items():
        menu.add(str(x),y)
        if config[0]['axis_y'] == y:
            dft = str(x)
    config[0]['axis_y'] = int(menu.show(msg="Axis-Y", dft=dft))

    config[0]['y_up'] = \
        qprompt.ask_int("Y-Up", dft=config[0]['y_up'])

    config[0]['y_down'] = \
        qprompt.ask_int("Y-Down", dft=config[0]['y_down'])


def edit_transpose():
    global config

    menu = qprompt.Menu()
    for x,y in Transpose.transpose.subcon.subcon.ksymapping.items():
        menu.add(str(x),y)
        if config[3]['transpose'] == y:
            dft = str(x)
    transpose = int(menu.show(msg="Transpose", dft=dft))

    config[3]['transpose'] = transpose


def edit_dial(dial):
    global config

    bank = int((dial-1) / _DIALS)
    subdial = dial-(_DIALS * bank)-1

    config[2][bank][subdial]['midicc'] = \
        qprompt.ask_int("MidiCC", vld=list(range(0,128)),
            dft=config[2][bank][subdial]['midicc'])

    config[2][bank][subdial]['min'] = \
        qprompt.ask_int("Min", vld=list(range(0,128)),
            dft=config[2][bank][subdial]['min'])

    config[2][bank][subdial]['max'] = \
        qprompt.ask_int("Max", vld=list(range(0,128)),
            dft=config[2][bank][subdial]['max'])


def edit_pad(pad):
    global config

    bank = int((pad-1) / _PADS)
    subpad = pad-(_PADS * bank)-1

    config[1][bank][subpad]['note'] = \
        qprompt.ask_int("Note", vld=list(range(0,128)),
            dft=config[1][bank][subpad]['note'])

    menu = qprompt.Menu()


def edit_scale(pad, verbose):
    global config

    rbank = int((pad-1) / _PADS)
    rsubpad = pad-(_PADS * rbank)-1

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

        config[1][bank][subpad]['note'] = note

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

    if _hasQPrompt:
        parser.add_option("-A", "--arpeggio",
            help="Interactively configure the Arpeggiator",
            action="store_true", dest="arpeggio")
        parser.add_option("-G", "--general",
            help="Interactively configure general settings",
            action="store_true", dest="general")
        parser.add_option("-J", "--joy",
            help="Interactively configure the Joystick",
            action="store_true", dest="joy")
        parser.add_option("-T", "--transpose",
            help="Interactively configure the Transposing",
            action="store_true", dest="transpose")
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
    config = Mpk_Play.parse(data)
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
    if options.joy:
        edit_joy()
    if options.transpose:
        edit_transpose()
    if options.dial:
        edit_dial(int(options.dial))
    if options.pad:
        edit_pad(int(options.pad))

    if options.scale:
        edit_scale(int(options.scale), options.verbose)


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
        outfile.write(Mpk_Play.build(config))

if __name__ == "__main__":
    main()

