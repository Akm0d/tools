#!/usr/bin/python3
import os
import sys

if not len(sys.argv) == 2:
    print("usage: switch_workspace.py [Right|Left]")
    exit(0)

if sys.argv[1].upper() == "RIGHT":
    os.system("xdotool keydown ctrl alt Right;xdotool keyup ctrl alt Right")
elif sys.argv[1].upper() == "LEFT":
    os.system("xdotool keydown ctrl alt Left;xdotool keyup ctrl alt Left")
if sys.argv[1].upper() == "MOVE_RIGHT":
    os.system("xdotool keydown shift ctrl alt Right;xdotool keyup shift ctrl alt Right")
elif sys.argv[1].upper() == "MOVE_LEFT":
    os.system("xdotool keydown shift ctrl alt Left;xdotool keyup shift ctrl alt Left")
else:
    print("Invalid Argument \"",sys.argv[1],"\"")
