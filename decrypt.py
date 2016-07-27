#!/usr/bin/python2.7
import re
import sys
from string import maketrans

# keep the alphabet in a list
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
max_word_size = 25
offset = 65
solutions = []

# Get the cypher from user if there wasn't one on the command line
cypher = ""
if len(sys.argv) > 1:
    cypher = str(sys.argv[1]).upper()
else: 
    cypher = raw_input("Enter the cypher, then press ENTER:\n").upper()
original_word_list = map(lambda x:re.sub('[^A-Z]+',"",x), cypher.split())

original_lists = [[] for i in range(max_word_size)]
hashmap = {}

# Add words to the dictionary based on their length
for word in original_word_list:
    original_lists[len(word.strip())].append(word.strip().upper())
    hashmap[word.strip().upper()] = set() 
    
# TODO Import the dictionary, possibly ask for a filename
filename = "dictionary.txt"
words = set()
with open(filename) as f: words = set(f.readlines())

# Add words to the dictionary based on their length
dictionary = [[] for i in range(max_word_size)]
for word in words:
    dictionary[len(word.strip())].append(word.strip().upper())

# Add all matching words to the hash map
word_length = 0
for lists in (original_lists):
    if (lists):
        for x_word in lists:
            for y_word in (dictionary[word_length]):
                x_trans = x_word
                y_trans = y_word
                for i in range(0,word_length):
                    x_tab = maketrans(str(x_trans[i]),str(chr(33+i)))
                    y_tab = maketrans(str(y_trans[i]),str(chr(33+i)))
                    x_trans = x_trans.translate(x_tab)
                    y_trans = y_trans.translate(y_tab)
                # When a dictionary word has letters in the same places as a cypher
                if x_trans == y_trans:
                    hashmap[x_word].add(y_word)
    word_length += 1

# Return letters in the string that aren't part of the input_letters
def unused_letters(input_letters,input_string):
    unused_letters = ""
    for x in input_string:
        found = False
        for y in input_letters:
            if x == y:
                found = True
        if not found:
            input_letters += x
            unused_letters += x
    return unused_letters

# See if a word matches what I have so far
def match(word,key,crypto_letters,translation):
   k = 0
   for w in word:
        c = 0
        for t in translation:
            if w == t: # if a letter in the word is in the translation
                # It has to match the same spot in the key
                if not key[k] == crypto_letters[c]:
                    #print "False because " + t + " = " + crypto_letters[c] + " not " + key[k]
                    return False
            c += 1
        k += 1
   return True

# Recursive function
def decrypt(crypto_letters,translation):
    # If a key has a letter not in the crypto_letters string, then call decrypt on it
    for key in hashmap:
        unused = unused_letters(crypto_letters,key)
        # Base case: Once all the letters in all the keys have been used
        if not unused == "":
            for word in hashmap[key]:
                new_trans = unused_letters(translation,word)
                if not new_trans == "":
                    # If the word has any letters in the translation, they should be in the right spot
                    if len(new_trans) == len(unused) and match(word,key,crypto_letters,translation):
                        # If possible doesn't end with a possible word then skip it and continue in loop
                        possible = decrypt(crypto_letters + unused,translation + new_trans)
                        if not possible == "":
                            return possible
            # If none of the words work out then return an empty string
            return ""
    return crypto_letters + ":" + translation

# Initialize Recursion
for key in hashmap:
    #print "\n" + key + ":\n"+ str(hashmap[key])
    for word in hashmap[key]:
        answer = decrypt(unused_letters("",key),unused_letters("",word))
        # Turn answer into translate table
        mixed = re.sub(':.+$','',answer)
        translated = re.sub('.+:','',answer)
        if (len(mixed) == len(translated)) and not answer == "":
            translate_table = maketrans(mixed,translated)
            solution = cypher.translate(translate_table)
            if (solution not in solutions):
                # print "Translate table -> " + answer
                solutions.append(solution)
                print(solution)
