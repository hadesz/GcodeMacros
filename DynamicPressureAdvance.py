#!python
import os
import re
import sys

sourceFile = sys.argv[1]

# Read the ENTIRE g-code file into memory
with open(sourceFile, "r") as f:
    lines = f.readlines()

if sourceFile.endswith('.gcode'):
    destFile = re.sub('\.gcode$','', sourceFile)
    try:
        os.rename(sourceFile, destFile+".dpa.bak")
    except FileExistsError:
        os.remove(destFile+".dpa.bak")
        os.rename(sourceFile, destFile+".dpa.bak")
    destFile = re.sub('\.gcode$', '', sourceFile)
    destFile = destFile + '.gcode'
else:
    destFile = sourceFile
    os.remove(sourceFile)

inInfill = False

with open(destFile, "w") as of:
    of.write('; Ensure macros are properly setup in klipper\n')
    of.write('_USE_PA F=default\n')
    for oline in lines:
        if oline.startswith(';TYPE:'):
            of.write(oline)
            lineType = re.sub(r'\s+', '', re.sub(r';TYPE:(.*)\r?\n', '\\1', oline))
            of.write('_USE_PA F="' + lineType + '"\n')
        else:
            of.write(oline)

of.close()
f.close()
