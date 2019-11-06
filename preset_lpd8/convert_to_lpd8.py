from optparse import OptionParser

usage = "usage: %prog [options] FILENAME"
parser = OptionParser(usage)
(options, args) = parser.parse_args()

if len(args) != 1:
    parser.error("input FILE not specified")

infile = open(args[0], "r")
if not infile:
    print("Unable to open file")
    quit(0)

outfile = open(args[0]+".lpd8", "wb")
if not outfile:
    print("Unable to open output file")
    quit(0)

data = infile.read(2000)

for num in data.split(" "):
    if num:
        print("%2.2x " % int(num), end="")
        outfile.write(bytes([int(num)]))
print("")
