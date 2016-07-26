#!/bin/python2.7
import sys
import threading
from string import maketrans
from random import randint
from time import sleep

# Swaps two random letters
def scramble(letters):
    x = list(letters)
    a = randint(0, len(letters) - 1)
    b = randint(0, len(letters) - 1)
    while b == a:
        b = randint(0, len(letters) - 1)
    x[a], x[b] = x[b], x[a]
    return ''.join(x)


# Mix things up right away to make recursion easier
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
mixed = scramble(alphabet)
text = ""
subprocess_locked = False


# Constantly scramble alphabet in subprocess
def background_randomizer():
    global subprocess_locked
    global mixed
    while text == "":
        subprocess_locked = True
        mixed = scramble(mixed)
        subprocess_locked = False
threading.Thread(target=background_randomizer).start()

# Prompt for input if there was no message passed in
if len(sys.argv) > 1:
    arg = str(sys.argv[1])
    if arg == "help":
        print("USE: ./enigma.py \"<Text to encrypt>\"")
        exit()
    else:
        sleep(2)
        text = arg
else:
    text = raw_input("Enter the message to encrypt, only use letters and spaces: \n").upper()
# Encrypt the data
translate_table = maketrans(alphabet, mixed)
print(text.translate(translate_table))
exit()
