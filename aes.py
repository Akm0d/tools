#!/usr/bin/python3

# TODO make this a command line option
debug = True

# Rcon[] is 1-based, so the first entry is just a place holder
Rcon = bytes([0x00,
              0x01, 0x02, 0x04, 0x08,
              0x10, 0x20, 0x40, 0x80,
              0x1B, 0x36, 0x6C, 0xD8,
              0xAB, 0x4D, 0x9A, 0x2F,
              0x5E, 0xBC, 0x63, 0xC6,
              0x97, 0x35, 0x6A, 0xD4,
              0xB3, 0x7D, 0xFA, 0xEF,
              0xC5, 0x91, 0x39, 0x72,
              0xE4, 0xD3, 0xBD, 0x61,
              0xC2, 0x9F, 0x25, 0x4A,
              0x94, 0x33, 0x66, 0xCC,
              0x83, 0x1D, 0x3A, 0x74,
              0xE8, 0xCB, 0x8D])

# sub bytes box to be used for sub Bytes
# Use self.sbox to access this by row and column
sbox = bytes([
    #    0     1     2     3     4     5     6     7     8     9     a     b     c     d     e     f
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,  # 0
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,  # 1
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,  # 2
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,  # 3
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,  # 4
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,  # 5
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,  # 6
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,  # 7
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,  # 8
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,  # 9
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,  # a
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,  # b
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,  # c
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,  # d
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,  # e
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16  # f
])

xtime = lambda a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)


def ffAdd(a, b, c, d):
    return a ^ b ^ c ^ d


def ffMultiply(a, b):
    p = 0

    for i in range(8):
        if b & 1 == 1:
            p ^= a
        hi_bit = a & 0x80
        a <<= 1
        if hi_bit == 0x80:
            a ^= 0x1b
        b >>= 1
    return p % 256


# Convert an array of bytes to an nb x nk matrix
def genMatrix(byte_array, columns, rows):
    matrix = [[0 for col in range(columns)] for row in range(rows)]
    c = 0
    for col in range(columns):
        for row in range(rows):
            # Pad the matrix with zeros if the byte array is too short
            if c >= len(byte_array):
                matrix[row][col] = 0x00
            else:
                matrix[row][col] = byte_array[c]
            c += 1
    return matrix


def transposeMatrix(state, rows, columns):
    byte_array = []
    for col in range(columns):
        for row in range(rows):
            byte_array.append(state[col][row])

    state = genMatrix(byte_array, columns, rows)
    return state


# Convert an nb x nk matrix into an array of bytes
def genText(state, columns, rows):
    # fill the byte array with zeros
    byte_array = []
    # replace elements in byte array with state data
    for col in range(columns):
        for row in range(rows):
            # Get rid of zero padding
            # This may break things that use 0x00 in the middle of a message
            if not state[row][col] == 0x00:
                byte_array.append(state[row][col])
    return bytes(byte_array)


# Print out as a matrix.
def printMatrix(state):
    output = ""
    for row in state:
        output += "[ "
        for item in row:
            output += "%02x " % item
        output += "]\n"
    print(output)
    return output


def printRow(row):
    output = "[ "
    for item in row:
        output += "%02x " % item
    output += "]"
    return output


class aes(object):
    # Python constructor
    def __init__(self, cipher_key, nb, nk):
        self.round = 0
        self.nb = nb
        self.nk = nk
        self.nr = self.nb + self.nk + 2
        self.k = transposeMatrix(genMatrix(cipher_key, self.nk, self.nb), self.nk, self.nb)
        # Initialize the sbox as a matrix and transpose it
        self.sbox = transposeMatrix(genMatrix(sbox, 16, 16), 16, 16)
        self.key_schedule, self.inv_key_schedule = self.keyExpansion(self.k)

    # Initialize encryption recursion
    def cipher(self, state):
        if debug:
            print("\nPLAINTEXT:", self.toString("", state, self.nb))
            print("KEY:      ", self.toString("", transposeMatrix(self.k, self.nb, self.nk), self.nk))
            print("\nCIPHER (ENCRYPT):")
            print(self.toString("input", state, self.nb))
        state = self.addRoundKey(state)

        # Run through all 4 cycles for the number of rounds
        for i in range(self.nr - 1):
            self.round += 1
            if debug: print(self.toString("start", state, self.nb))
            state = self.subBytes(state)
            state = self.shiftRows(state)
            state = self.mixColumns(state)
            state = self.addRoundKey(state)

        self.round += 1
        if debug: print(self.toString("start", state, self.nb))
        state = self.subBytes(state)
        state = self.shiftRows(state)
        state = self.addRoundKey(state)
        if debug: print(self.toString("output", state, self.nb))
        return state

    # Transformation in the Cipher that processes the State using a non-
    # linear byte substitution table (S-box) that operates on each of the
    # State bytes independently
    def subBytes(self, state):
        for row in range(self.nb):
            for col in range(self.nb):
                x = state[row][col] >> 4  # this is the row number in sbox
                y = state[row][col] & 0x0f  # this is the column number in sbox
                state[row][col] = self.sbox[x][y]
        if debug: print(self.toString("s_box", state, self.nb))
        return state

    # This transformation performs a circular shift on each row in the state
    # How does it work for matrices with 6 rows?
    # Shift by row + 1 % 4
    def shiftRows(self, state):
        for row in range(self.nb):
            byte_array = []
            for col in range(self.nb):
                byte_array.append(state[row][(col + row) % self.nb])
            state[row] = byte_array
        if debug: print(self.toString("s_row", state, self.nb))
        return state

    # Transformation in the Cipher that takes all of the columns of the
    # State and mixes their data (independently of one another) to
    # produce new columns.
    def mixColumns(self, a):
        b = [[0 for col in range(self.nb)] for row in range(self.nb)]
        for col in range(self.nb):
            b[0][col] = ffAdd(
                ffMultiply(2, a[0][col]),
                ffMultiply(3, a[1][col]),
                ffMultiply(1, a[2][col]),
                ffMultiply(1, a[3][col]))
            b[1][col] = ffAdd(
                ffMultiply(1, a[0][col]),
                ffMultiply(2, a[1][col]),
                ffMultiply(3, a[2][col]),
                ffMultiply(1, a[3][col]))
            b[2][col] = ffAdd(
                ffMultiply(1, a[0][col]),
                ffMultiply(1, a[1][col]),
                ffMultiply(2, a[2][col]),
                ffMultiply(3, a[3][col]))
            b[3][col] = ffAdd(
                ffMultiply(3, a[0][col]),
                ffMultiply(1, a[1][col]),
                ffMultiply(1, a[2][col]),
                ffMultiply(2, a[3][col]))
        if debug: print(self.toString("m_col", b, self.nb))
        return b

    # Transformation in the Cipher and Inverse Cipher in which a Round
    # Key is added to the State using an XOR operation. The length of a
    # Round Key equals the size of the State (i.e., for Nb = 4, the Round
    # Key length equals 128 bits/16 bytes).
    def addRoundKey(self, state):
        # Transpose the state to work easier with key schedule
        state = transposeMatrix(state, self.nb, self.nb)
        result = [[0 for col in range(self.nb)] for row in range(self.nb)]
        # Prepare Debug state ment
        k_sch = bytearray([])
        for i in range(self.nb):
            k_sch.extend(self.key_schedule[self.round * self.nb + i])
            state[i] = self.xorWords(state[i], self.key_schedule[self.round * self.nb + i])
        # Transpose the matrix back to how it should be
        state = transposeMatrix(state, self.nb, self.nb)
        matrix = genMatrix(k_sch, self.nb, self.nb)
        if debug: print(self.toString("k_sch", matrix, self.nb))
        return state

    def invCipher(self, state):
        # Restart the rounds for the inverse cipher
        self.round = 0
        if debug: print("\nINVERSE CIPHER (DECRYPT):")
        if debug: print(self.toString("iinput", state, self.nb))
        state = self.invAddRoundKey(state)

        # Run through all 4 cycles for the number of rounds
        for i in range(self.nr - 1):
            if debug: print(self.toString("istart", state, self.nb))
            self.round += 1
            state = self.invShiftRows(state)
            if debug: print(self.toString("is_row", state, self.nb))
            state = self.invSubBytes(state)
            if debug: print(self.toString("is_box", state, self.nb))
            state = self.invAddRoundKey(state)
            if debug: print(self.toString("ik_add", state, self.nb))
            state = self.invMixColumns(state)

        self.round += 1
        state = self.invShiftRows(state)
        if debug: print(self.toString("is_row", state, self.nb))
        state = self.invSubBytes(state)
        if debug: print(self.toString("is_box", state, self.nb))
        state = self.invAddRoundKey(state)
        if debug: print(self.toString("ioutput", state, self.nb))
        return state

    # Transformation in the Inverse Cipher that is the inverse of SubBytes().
    # Row = 17 /16  16 is the length of row in sbox
    # col = 17 % 16 ; 17 is the position in array
    def invSubBytes(self, state):
        for row in range(self.nb):
            for col in range(self.nb):
                index = sbox.index(state[row][col])
                x = int(index / 16) << 4
                y = index % 16
                state[row][col] = (x | y)
        return state

    # Transformation in the Inverse Cipher that is the inverse of ShiftRows().
    def invShiftRows(self, state):
        for row in range(self.nb):
            byte_array = []
            for col in range(self.nb):
                byte_array.append(state[row][(col - row) % self.nb])
            state[row] = byte_array
        return state

    def invAddRoundKey(self, state):
        # Transpose the state to work easier with key schedule
        state = transposeMatrix(state, self.nb, self.nb)
        result = [[0 for col in range(self.nb)] for row in range(self.nb)]
        # Prepare Debug state ment
        k_sch = bytearray([])
        for i in range(self.nb):
            k_sch.extend(self.inv_key_schedule[self.round * self.nb + i])
            state[i] = self.xorWords(state[i], self.inv_key_schedule[self.round * self.nb + i])
        # Transpose the matrix back to how it should be
        state = transposeMatrix(state, self.nb, self.nb)
        matrix = genMatrix(k_sch, self.nb, self.nb)
        if debug: print(self.toString("ik_sch", matrix, self.nb))
        return state

    # Transformation in the Inverse Cipher that is the inverse of MixColumns().
    def invMixColumns(self, a):
        b = [[0 for col in range(self.nb)] for row in range(self.nb)]
        for col in range(self.nb):
            b[0][col] = ffAdd(
                ffMultiply(0x0e, a[0][col]),
                ffMultiply(0x0b, a[1][col]),
                ffMultiply(0x0d, a[2][col]),
                ffMultiply(0x09, a[3][col]))
            b[1][col] = ffAdd(
                ffMultiply(0x09, a[0][col]),
                ffMultiply(0x0e, a[1][col]),
                ffMultiply(0x0b, a[2][col]),
                ffMultiply(0x0d, a[3][col]))
            b[2][col] = ffAdd(
                ffMultiply(0x0d, a[0][col]),
                ffMultiply(0x09, a[1][col]),
                ffMultiply(0x0e, a[2][col]),
                ffMultiply(0x0b, a[3][col]))
            b[3][col] = ffAdd(
                ffMultiply(0x0b, a[0][col]),
                ffMultiply(0x0d, a[1][col]),
                ffMultiply(0x09, a[2][col]),
                ffMultiply(0x0e, a[3][col]))
        # if debug: print(self.toString("im_col", b, self.nb))
        return b

    # rotWord() - performs a cyclic permutation on its input word.
    # Function used in the Key Expansion routine that takes a four-byte
    # word and performs a cyclic permutation.
    def rotWord(self, word):
        result = [0 for col in range(self.nb)]
        for i in range(self.nb):
            result[i] = word[(i + 1) % self.nb]
        return result

    def subWord(self, word):
        for byte in range(self.nb):
            x = word[byte] >> 4  # this is the row number in sbox
            y = word[byte] & 0x0f  # this is the column number in sbox
            word[byte] = self.sbox[x][y]
        # the cipher key which contains nk words.A)
        return word

    def xorWords(self, a, b):
        word = [0 for col in range(self.nb)]
        for i in range(self.nb):
            word[i] = a[i] ^ b[i]
        return word

    # The state which contains nr + 1 words
    # we also need to know nk
    # TODO Debug this for 8 row keys
    def keyExpansion(self, state):

        # This will become the key schedule
        words = genMatrix(bytes([]), self.nb, self.nb * (self.nr + 1))

        # Load the cipher key byte by byte
        i = 0
        while i < self.nk:
            for b in range(self.nb):
                words[i][b] = state[i][b]
            i += 1

        # Expand the key
        i = self.nk
        while i < self.nb * (self.nr + 1):
            # Allocate memory for the temp Array
            temp = [0 for col in range(self.nb)]
            for j in range(4):
                temp[j] = words[i - 1][j]

            # print(i,"temp", printRow(temp))
            if (i % self.nk) == 0:
                # Turn a byte from the rcon array into a word
                rcon = [0 for col in range(self.nb)]
                rcon[0] = Rcon[int(i / self.nk)]
                temp = self.rotWord(temp)
                # print(i,"rotw", printRow(temp))
                temp = self.subWord(temp)
                # print(i,"subw", printRow(temp))
                temp = self.xorWords(temp, rcon)
                # print(i,"rcon", printRow(rcon))
                # print(i,"xorw", printRow(temp))
            elif (self.nk > 6) and ((i % self.nk) == 4):
                # If Nk = 8 and i -4 is a multiple of NK
                # Then subword() is applied to words[i - 1] prior to the XOR
                temp = self.subWord(temp)
                # print(i,"subw", printRow(temp))
            # End if

            words[i] = self.xorWords(words[i - self.nk], temp)
            i += 1

        # Generate the inverse key schedule for decipher
        inv_words = genMatrix(bytes([]), self.nb, self.nb * (self.nr + 1))
        b = self.nb * (self.nr + 1)  # Backwards counter
        f = 0  # forwards counter
        while b > 0:
            inv_words[f + 0] = words[b - 4]
            inv_words[f + 1] = words[b - 3]
            inv_words[f + 2] = words[b - 2]
            inv_words[f + 3] = words[b - 1]
            f += 4
            b -= 4

        # if debug: print("key schedule: ")
        # if debug: print(printMatrix(transposeMatrix(words, self.nb, self.nb * (self.nr + 1))))
        # if debug: print(printMatrix(transposeMatrix(inv_words, self.nb, self.nb * (self.nr + 1))))
        return words, inv_words

    def toString(self, header, state, columns):
        if header == "":
            output = header + " "
        elif self.round >= 10:
            # Do double digits
            output = "round[%d]." % self.round + header + " \t"
        else:
            output = "round[ %d]." % self.round + header + " \t"

        for col in range(columns):
            for row in range(4):
                output += "%02x" % state[row][col]
        return output
