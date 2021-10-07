'''
Python script to manipulate keygroups for MPCv2.3 and MPC Essentials.

A keygroup file is XML which declares how samples will be trigger from
the midi data and how they are tuned. This script allows the triggers
to be moved around the keyboard and to merge keygroup files - effectively
creating a keyboard split between multiple instruments.
'''

import xml.etree.ElementTree as ET
from optparse import OptionParser

usage = "usage: %prog [options] FILENAME"
parser = OptionParser(usage)

parser.add_option("-v", "--verbose",
    action="store_true", dest="verbose")

parser.add_option("-o", "--output", dest="outfile",
    help="write changes/data to OUTFILE")
parser.add_option("-O", "--same", dest="samefile",
    action="store_true", help="write changes/data to same/input file")

parser.add_option("-n", "--name", dest="name",
    help="change name of the keygroup")
parser.add_option("-m", "--merge", dest="merge",
    help="merge in the samples from a second keygroup file")

parser.add_option("-d", "--delete", dest="delete",
    help="delete a specific instrument")
parser.add_option("-D", "--delnotes", dest="delnotes",
    help="delete a range of notes/instruments (positive=up-to-inc, negative=up-from-inc)")
parser.add_option("-T", "--tidy", dest="tidy",
    action="store_true", help="remove instruments which have no sample files specified")

parser.add_option("-s", "--semi", dest="semi",
    help="change tuning of instruments by number of SEMI-tones (positive or negative)")
parser.add_option("-S", "--semisamp", dest="semisamp",
    help="change tuning of samples by number of SEMI-tones (positive or negative)")
parser.add_option("-M", "--move", dest="movekeys",
    action="store_true", help="move keys by same number of semitones")

parser.add_option("-k", "--keyspan", dest="keyspan",
    help="limit the keyspan of instruments by number of SEMI-tones (positive or negative)")

(options, args) = parser.parse_args()

if len(args) != 1:
    parser.error("input FILE not specified")

if options.verbose:
    print("Reading %s..." % args[0])


# Open primary XML file
tree = ET.parse(args[0])
root = tree.getroot()

# Find the instruments section
program = root.find("Program")
instruments = program.find("Instruments")

if options.name:
   name = program.find("ProgramName")
   name.text = options.name

lowest = 128
highest = 0
last_inst = 0

# print out all the high and low notes for each instrument
for instrument in list(instruments.iter("Instrument")):
   if options.verbose:
      print("-")
      print(instrument.tag, instrument.attrib)

   inst_active = False
   for layers in instrument.iter("Layers"):
      for layer in layers.iter("Layer"):
         for sample_name in layer.iter("SampleName"):
            if options.verbose:
               print(layer.tag, layer.attrib, sample_name.text)
            if sample_name.text:
               inst_active = True 

   # ignore instruments which are not used
   if not inst_active:
      if options.merge or options.tidy:
         if options.verbose:
            print("Removing unused instrument:", instrument.attrib)
         instruments.remove(instrument)
      continue

   # ignore instruments which are marked for deletion
   if options.delete:
      if int(options.delete) == int(instrument.attrib['number']):
         if options.verbose:
            print("Deleting instrument:", instrument.attrib)
         instruments.remove(instrument)
         continue
   if options.delnotes:
      for note in instrument.iter("LowNote"):
         low_note = int(note.text)
      for note in instrument.iter("HighNote"):
         high_note = int(note.text)

      # delete outright
      if ((int(options.delnotes) > 0 and int(options.delnotes) >= high_note) or
            (int(options.delnotes) < 0 and (0-int(options.delnotes)) <= low_note)):
         if options.verbose:
            print("Deleting instrument:", instrument.attrib)
         instruments.remove(instrument)
         continue

      # modify to limit high/low note notes
      if (int(options.delnotes) > 0 and int(options.delnotes) >= low_note):
         if options.verbose:
            print("Limiting LowNote:", instrument.attrib, options.delnotes)
         for low_note in instrument.iter("LowNote"):
            low_note.text = str(int(options.delnotes)+1)
      if (int(options.delnotes) < 0 and (0-int(options.delnotes)) <= high_note):
         if options.verbose:
            print("Limiting HighNote:", instrument.attrib, options.delnotes)
         for high_note in instrument.iter("HighNote"):
            high_note.text = str(1-int(options.delnotes))

   # have to re-write instrument numbers as one (or more)
   # may have been deleted
   last_inst = last_inst + 1
   instrument.attrib['number'] = str(last_inst)

   ignore_base_note = False
   root_note = False
   if instrument.find("IgnoreBaseNote").text == "True":
      ignore_base_note = True

   tune_coarse = instrument.find("TuneCoarse")
   if options.semi and (not ignore_base_note):
      tune_coarse.text = str(int(tune_coarse.text) - int(options.semi))
      if options.verbose:
         print("adjusting instrument tune:", tune_coarse.text)

   for layers in instrument.iter("Layers"):
      for layer in layers.iter("Layer"):
         tune_coarse = layer.find("TuneCoarse")
         sample_name = layer.find("SampleName")
         if sample_name.text:
            root_note = int(layer.find("RootNote").text)
            if options.semisamp and (not ignore_base_note):
               tune_coarse.text = str(int(tune_coarse.text) - int(options.semisamp))
               if options.verbose:
                  print("adjusting sample tune:", tune_coarse.text)

   semi_adjust = 0
   if options.movekeys and options.semi and (not ignore_base_note):
      semi_adjust = semi_adjust + int(options.semi)
   if options.movekeys and options.semisamp and (not ignore_base_note):
      semi_adjust = semi_adjust + int(options.semisamp)

   for low_note in instrument.iter("LowNote"):
      if options.semi or options.semisamp:
         low_note.text = str(int(low_note.text) + semi_adjust)
      if options.keyspan and int(options.keyspan) < 1:
         low_note.text = str(root_note + int(options.keyspan))
      if options.verbose:
         print("Low Note:", low_note.text)

      if int(low_note.text) < lowest:
         lowest = int(low_note.text)

   if options.verbose:
      print("Root Note:", root_note)

   for high_note in instrument.iter("HighNote"):
      if options.semi or options.semisamp:
         high_note.text = str(int(high_note.text) + semi_adjust)
      if options.keyspan and int(options.keyspan) > -1:
         high_note.text = str(root_note + int(options.keyspan))
      if options.verbose:
         print("High Note:", high_note.text)

      if int(high_note.text) > highest:
         highest = int(high_note.text)

if options.verbose:
    print("=")
    print("Lowest Note:", lowest)
    print("Highest Note:", highest)
    print("Last Instrument:", last_inst)



# --------
# Merge in the instruments from a second keygroup file
if options.merge:
   # Open primary XML file
   merge_tree = ET.parse(options.merge)
   merge_root = merge_tree.getroot()

   # Find the instruments section
   merge_program = merge_root.find("Program")
   merge_instruments = merge_program.find("Instruments")

   for instrument in merge_instruments.iter("Instrument"):
      if options.verbose:
         print(instrument.tag, instrument.attrib)

      inst_active = False
      for layers in instrument.iter("Layers"):
         for layer in layers.iter("Layer"):
            for sample_name in layer.iter("SampleName"):
               if options.verbose:
                  print(layer.tag, layer.attrib, sample_name.text)
               if sample_name.text:
                  inst_active = True 

      # ignore instruments which are not used
      if not inst_active:
         continue

      last_inst = last_inst + 1
      if options.verbose:
         print("Appending Instrument as:", last_inst)

      instrument.attrib['number'] = str(last_inst)

      # this is the original XML tree
      instruments.append(instrument)

# Correct the number of keygroups
keygroups = program.find("KeygroupNumKeygroups")
keygroups.text = str(last_inst)

# ---------------------
# write out the changes
if options.outfile:
   tree.write(options.outfile, encoding='utf-8', xml_declaration=True)
if options.samefile:
   tree.write(args[0], encoding='utf-8', xml_declaration=True)

