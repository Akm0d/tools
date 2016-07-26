# tools
Personal exploration projects

Privacy.pl
----------
A tool that can be used to hide the commands and output from commands 
in your terminal so that someone looking over your shoulder doesn't 
see what you are doing.
WARNING: You have to know exactly what to expect as output when you type in
a command because there is no indication of whether or not anything worked or not.
-- maybe I should spit out the error codes of every command at the very least...

calvin.pl
---------
I made this just to mess around with espeak.  It doesn't really do anything yet 
except read what you put in as a command line argument.

encrypt.py
----------
Swaps around the letters of the alphabet randomly in a subprocess and uses the
mixed up alphabet as a translation table for a message you input.

decrypt.py
----------
decrypts messages that were encrypted using the encrypt.py(or similar) function.
- Uses the dictionary.txt file
    - I am going to wrap this up with language packages and ask at the command line
      which language you want to use or if you want to use a custom dictionary

dictionary.txt
--------------
for use with decrypt.py
The file was made with the following command:
'cat /usr/share/dict/words > dictionary.txt'
and I removed most single letter words in vim by searching for /^.$ and
removing the ones i didn't want.  
I also removed words with apostrophes, but I might fix that.
the decrypt.py script uses special characters and I need to make a few modifications....

sendfiles.pl
------------
Sends files in the current working directory to a remote server
