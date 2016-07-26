#!/usr/bin/python2.7
from string import maketrans

# keep the alphabet in a list
max_word_size = 50
offset = 65

# Returns the number value of letters. A is 0 and Z is 25
def letter_number(letter):
    return str(ord(letter.upper())-offset)

# Finds the most common letter in a string skipping over letters in the "skip" string
def most_common_letter( text, skip ):
    most_common = '~'
    letter = '~'
    highest = 0
    skip += ' '
    # Remove letters in the "skip" string
    text = text.translate(None,skip)
    while len(text) > 0:
        current = 0
        letter = text[:1]
        for character in text:
            if character == letter:
                current += 1
        if current > highest:
            highest = current
            most_common = letter
        text = text.translate(None,str(letter))
    return most_common

# Get the cypher from user
cypher = raw_input("Enter the cypher, then press ENTER:\n").upper()
original_word_list = cypher.split()

original_lists = [[] for i in range(max_word_size)]
hashmap = {}
# Add words to the dictionary based on their length
for word in original_word_list:
    original_lists[len(word.strip())].append(word.strip().upper())
    hashmap[word.strip().upper()] = set() 
    
# Make a list of all the letters in the cypher from most common to least common
letters_by_frequency = "etaoinshrdlcumwfgypbvkjxqz"
cypher_by_frequency = ""
least_frequent_letter = ""
while least_frequent_letter != "~":
    least_frequent_letter = most_common_letter(cypher,str(cypher_by_frequency))
    if least_frequent_letter != "~":
        cypher_by_frequency += least_frequent_letter

print ("Letter frequency: " + cypher_by_frequency)

# Import the dictionary, possibly ask for a filename
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

# Recursive function
def decrypt(crypto_letters,translation):
    # If a key has a letter not in the crypto_letters string, then call decrypt on it
    for key in hashmap:
        unused = unused_letters(crypto_letters,key)
        # Base case: Once all the letters in all the keys have been used
        if not unused == "":
            new_trans = ""
            # TODO try multiple translation paths
            for word in hashmap[key]:
                # If the word doesn't fit the current translation then skip it
                    # Do this with the map() function and set intersections?
                # Else, Try to decript it
                # TODO Return "None" if translation isn't possible
            # Do I want this to return?  I might be eliminating possilbe translations
            return decrypt(crypto_letters + unused,translation + new_trans)
    return maketranse(crypto_letters,translation)

# look at the first key and then look at its first value
# look at the next key 
# If it contains the same letters as the previous key then select only the words that map the same letters to the same value
# If it contains none of the same letters then repeat the first step
# Store a list of the letters that have been looked at, and what they map to currently
# If a second key has no values mapped to it, then look at the second item of the first key's list
for key in hashmap:
    #print "\n" + key + ":\n"+ str(hashmap[key])
    for word in hashmap[key]:
        translate_table = decrypt(key,word)
        if not answer == None:
            print(text.translate(translate_table))
# This only needs to be done for one key in the hashmap as an initialization of the recursion
# TODO Or does it?
    exit()
