#!/usr/bin/python2.7
import re
import sys
from string import maketrans

max_word_size = 25
offset = 65
solutions = []
maps = []
filename = ""
cypher = ""
known_letters = ""
mapped_to = ""
precise = False
verbose = False
thorough = False
color = False
blue = ""
green = ""
red = ""
white = ""

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

# Handle command line arguments
# Python's for loop doesn't work like a c++ for loop so I did it this way.
a = 1
while a < len(sys.argv):
    if sys.argv[a] == "help" or sys.argv[a] == "-?" or sys.argv[a] == "-h" or sys.argv[a] == "--help":
        print "usage: ./decrypt.py [-d dictionary.file] [-m <mapped>:<letters>] [cryptogram] [-v|--verbose] [-t|--thorough] [-c|--color] [-p|--precise]" 
        print "example: ./decrypt.py -d dictionary.txt -m QWJFLD:ABCDEF KCGPBWK ZKFDMBX ZUFXUHAGDM XKCX"
        exit()
    # True or false command line options
    elif sys.argv[a] == "-c" or sys.argv[a] == "--color":
        color = True
        blue = "\033[1;36;40m"
        green = "\033[1;32;40m"
        red = "\033[1;31;40m"
        white = "\033[1;37;40m"
    elif sys.argv[a] == "-p" or sys.argv[a] == "--precise":
        precise = True
    elif sys.argv[a] == "-t" or sys.argv[a] == "--thorough":
        thorough = True
    elif sys.argv[a] == "-v" or sys.argv[a] == "--verbose":
        verbose = True
    # Command line arguments with parameters
    elif sys.argv[a] == "-m":
        a+=1
        if  a >= len(sys.argv) or sys.argv[a][0] == "-" or ':' not in sys.argv[a]:
            print "-m takes an argument in the format ABCD:EFGH"
            exit()
        mapped_to = unused_letters("",re.sub(':.+$','',sys.argv[a].upper()))
        known_letters = unused_letters("",re.sub('.+:','',sys.argv[a].upper()))
        if not len(mapped_to) == len(known_letters):
            print ("both sides of \"" + known_letters + ":" + mapped_to + "\" must be the same length") 
            exit()
    elif sys.argv[a] == "-d":
        a+=1
        if  a >= len(sys.argv) or sys.argv[a][0] == "-":
            print "-d takes an argument!"
            exit()
        filename = sys.argv[a]
    # Whatever is left over is part of the cypher as long as it doesn't start with a  hyphen
    elif not sys.argv[a][0] == "-":
        cypher += (sys.argv[a].upper() + " ")
    # Anything that has a hyphen that hasen't been taken care of is illegal
    else: 
        print sys.argv[a] + " is not a recognized option"
        exit()
    a+=1

# Import the dictionary, ask for a filename if none was given
if filename == "": 
    filename = raw_input("Path to the dictionary file: [/usr/share/dict/words] ")
    if filename == "":
        filename = "/usr/share/dict/words"
words = set()
with open(filename) as f: words = set(f.readlines())

# Get the cypher from user if there wasn't one on the command line
if cypher == "":
    cypher = raw_input("Enter the cypher, then press ENTER:\n").upper()


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
def decrypt(crypto_letters,translation,hashmap):
    # Print out the text being worked on
    #untested_letters = unused_letters("qwertyuiopasdfghjklzxcvbnm",crypto_letters)
    #output_trans = maketrans(crypto_letters+untested_letters,translation+"*"*len(untested_letters))
    output_trans = maketrans(crypto_letters,translation)
    sys.stdout.flush()
    solution = cypher.translate(output_trans)
    sys.stdout.write(solution+"\r")
    sys.stdout.flush()
    # If a key has a letter not in the crypto_letters string, then call decrypt on it
    a=0
    for key in hashmap:
        a+=1
        unused = unused_letters(crypto_letters,key)
        # Base case: Once all the letters in all the keys have been used
        if not unused == "":
            b=0
            for word in hashmap[key]:
                b+=1
                sys.stdout.flush()
                #sys.stdout.write(solution + " " + str(a+1) + "/" + str(len(hashmap)) + " " + str(b+1) + "/"+ str(len(hashmap[key])) + "    \r")
                new_trans = unused_letters(translation,word)
                if not new_trans == "":
                    # If the word has any letters in the translation, they should be in the right spot
                    if len(new_trans) == len(unused) and match(word,key,crypto_letters,translation):
                        # If possible doesn't end with a possible word then skip it and continue in loop
                        possible = decrypt(crypto_letters + unused,translation + new_trans,hashmap)
                        if not possible == "":
                            return possible
            # If none of the words work out then return an empty string
            return ""
    return crypto_letters + ":" + translation

# Make it possible to loop through all the calculations again
def full_decryption(cypher_text):
    original_word_list = map(lambda x:re.sub('[^A-Z]+',"",x), cypher_text.split())
    original_lists = [[] for i in range(max_word_size)]
    hashmap = {}

    # Add words to the dictionary based on their length
    for word in original_word_list:
        original_lists[len(word.strip())].append(word.strip().upper())
        hashmap[word.strip().upper()] = set() 
    dictionary = [[] for i in range(max_word_size)]
    for word in words:
        new_word = re.sub('[^A-Z]+',"",word.strip().upper())
        dictionary[len(new_word)].append(new_word)

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

    # Initialize Recursion
    a = 0
    for key in hashmap:
        a+=1
        #print "\n" + key + ":\n"+ str(hashmap[key])
        b = 0
        for word in hashmap[key]:
            b+=1
            answer = ""
            full_key = unused_letters("",mapped_to + key)
            full_word = unused_letters("",known_letters + word)
            if len(full_word) == len(full_key):
                if full_key+full_word not in maps:
                    #print full_key + ":" + full_word
                    maps.append(full_key+full_word)
                    answer = decrypt(full_key,full_word,hashmap)
            # Turn answer into translate table
            mixed = re.sub(':.+$','',answer)
            translated = re.sub('.+:','',answer)
            if (len(mixed) == len(translated)) and not answer == "":
                translate_table = maketrans(mixed,translated)
                solution = cypher_text.translate(translate_table)
                if (solution not in solutions) and not answer == full_key+":"+full_word:
                    valid_solution = True
                    color_solution = ""
                    # Double check that the solution is indeed a correct one, with "color" show it, with "precise" eliminate it
                    if precise or color:
                        for c in range (0,len(original_word_list)):
                            solution_words = solution.split()
                            if solution_words[c] not in hashmap[original_word_list[c]]:
                                color_solution += red + solution_words[c] + " "
                            else: 
                                color_solution += green + solution_words[c] + " "
                            if precise:
                               valid_solution = False
                    if color:
                        solution = color_solution + white
                    # print "Translate table -> " + answer
                    if valid_solution:
                        solutions.append(solution)
                        if verbose:
                            print (" "*len(cypher))
                            sys.stdout.flush()
                            #print key + ":" + word
                            print blue + answer + white
                            #print unused_letters(mapped_to,mixed)
                            print(solution + " " + blue + str(a+1) + "/" + str(len(hashmap)) + " " + str(b+1) + "/"+ str(len(hashmap[key]))+ white)
                        else:
                            print(solution)

# Run the program once
full_decryption(cypher)

# run the program on each solution until There are no more possibilitie
if thorough:
    solutions_size = len(solutions)
    new_solutions = 1
    while not solutions_size == new_solutions:
        for solution in solutions:
            full_decryption(solution)
        new_solutions = len(solutions)

# Give advice if there were no solutions
if len(solutions) == 0:
    print red + "No solutions were found!\n" + white + "Try adding the --thorough flag, removing the --precise flag, simplifying your -m map, or add/remove words from the cryptogram"
else:
    # Remove the last line of jibberish
    sys.stdout.flush()
    sys.stdout.write(" "*len(cypher))

