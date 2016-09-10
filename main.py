#!/usr/bin/python3

import aes

# TODO make these determinable by command line options
verbose = False

# The number of 32 bit words in a state
nb = 4  # this will always be 4
# The number of 32 bit words in a cipher key
nk = 4  # 4, 6, or 8
# cipher_key = str.encode("decryption key")
# This is the key used by the FIPS document in the key expansion
# cipher_key = bytes([0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c])
# This is the key used in the C.1 Example
cipher_key = bytes(
    [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
     # If nk = 6 then this will get used
     0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
     # If nk = 8 then this will get used
     0x18, 0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f])

# key for expanding 256 bit cipher key example in A.3
#cipher_key = bytes(
#    [0x60, 0x3d, 0xeb, 0x10, 0x15, 0xca, 0x71, 0xbe, 0x2b, 0x73, 0xae, 0xf0, 0x85, 0x7d, 0x77, 0x81,
#     0x1f, 0x35, 0x2c, 0x07, 0x3b, 0x61, 0x08, 0xd7, 0x2d, 0x98, 0x10, 0xa3, 0x09, 0x14, 0xdf, 0xf4])

# TODO split messages larger than nb * nk into segments
message = str.encode("Hello World!")  # Turn the message into a matrix
# message = str.encode(input('Message to Encode: '))
bytes_in_word = int(32 / 8)

# if verbose:
#    print("deciphered text:")
#    print(aes.genText(undo, nb, nk))

# Message to be used for passoff
message = bytes([0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff])
state = aes.genMatrix(message, nb, bytes_in_word)

# run the tests for nk = 4
nk = 4
nk_4 = aes.aes(cipher_key, nb, nk)  # Initialise aes class
cipher_text = nk_4.cipher(state)
nk_4.invCipher(cipher_text)

# run the tests for nk = 6
nk = 6
nk_6 = aes.aes(cipher_key, nb, nk)  # Initialise aes class
cipher_text = nk_6.cipher(state)
nk_6.invCipher(cipher_text)

# run the tests for nk = 8
nk = 8
nk_8 = aes.aes(cipher_key, nb, nk)  # Initialise aes class
cipher_text = nk_8.cipher(state)
nk_8.invCipher(cipher_text)
