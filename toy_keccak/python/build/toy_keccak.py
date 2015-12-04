# Modified Keccak with the purpose of fewer rounds and thus a smaller
# digest. 
#
# Chris Celi - Rensselaer Polytechnic Institute - Fall 2015
#
#
# -*- coding: utf-8 -*-
# Implementation by the Keccak, Keyak and Ketje Teams, namely, Guido Bertoni,
# Joan Daemen, Michael Peeters, Gilles Van Assche and Ronny Van Keer, hereby
# denoted as "the implementer".
#
# For more information, feedback or questions, please refer to our websites:
# http://keccak.noekeon.org/
# http://keyak.noekeon.org/
# http://ketje.noekeon.org/
#
# To the extent possible under law, the implementer has waived all copyright
# and related or neighboring rights to the source code in this file.
# http://creativecommons.org/publicdomain/zero/1.0/

def ROL64(a, n):
    return ((a >> (64-(n%64))) + (a << (n%64))) % (1 << 64)

def KeccakF1600onLanes(lanes):
    
    R = 1
    
    # Modified rounds from 24 to 3
    for round in range(24):
    # for round in range(3):
    
        # theta
        C = [lanes[x][0] ^ lanes[x][1] ^ lanes[x][2] ^ lanes[x][3] ^ lanes[x][4] for x in range(5)]
        D = [C[(x+4)%5] ^ ROL64(C[(x+1)%5], 1) for x in range(5)]
        lanes = [[lanes[x][y]^D[x] for y in range(5)] for x in range(5)]
    
        # rho and pi
        (x, y) = (1, 0)
        current = lanes[x][y]
        # for t in range(3):
        for t in range(24):
            (x, y) = (y, (2*x+3*y)%5)
            (current, lanes[x][y]) = (lanes[x][y], ROL64(current, (t+1)*(t+2)//2))
    
        # chi
        for y in range(5):
            T = [lanes[x][y] for x in range(5)]
            for x in range(5):
                lanes[x][y] = T[x] ^((~T[(x+1)%5]) & T[(x+2)%5])
    
        # iota
        for j in range(7):
            R = ((R << 1) ^ ((R >> 7)*0x71)) % 256
            if (R & 2):
                lanes[0][0] = lanes[0][0] ^ (1 << ((1<<j)-1))
    
    return lanes

def load64(b):
    return sum((b[i] << (8*i)) for i in range(8))

def store64(a):
    return list((a >> (8*i)) % 256 for i in range(8))

def KeccakF1600(state):
    
    lanes = [[load64(state[8*(x+5*y):8*(x+5*y)+8]) for y in range(5)] for x in range(5)]
    lanes = KeccakF1600onLanes(lanes)
    state = bytearray(200)
    
    for x in range(5):
        for y in range(5):
            state[8*(x+5*y):8*(x+5*y)+8] = store64(lanes[x][y])
    
    return state

def Keccak(rate, capacity, inputBytes, delimitedSuffix, outputByteLen):
    
    outputBytes = bytearray()
    state = bytearray([0 for i in range(200)])
    rateInBytes = rate//8
    blockSize = 0
    
    if (((rate + capacity) != 1600) or ((rate % 8) != 0)):
        return
    
    inputOffset = 0
    # === Absorb all the input blocks ===
    while(inputOffset < len(inputBytes)):
    
        blockSize = min(len(inputBytes)-inputOffset, rateInBytes)
    
        for i in range(blockSize):
            state[i] = state[i] ^ inputBytes[i+inputOffset]
    
        inputOffset = inputOffset + blockSize
    
        if (blockSize == rateInBytes):
            state = KeccakF1600(state)
            blockSize = 0
    
    # === Do the padding and switch to the squeezing phase ===
    state[blockSize] = state[blockSize] ^ delimitedSuffix
    
    if (((delimitedSuffix & 0x80) != 0) and (blockSize == (rateInBytes-1))):
        state = KeccakF1600(state)
    
    state[rateInBytes-1] = state[rateInBytes-1] ^ 0x80
    state = KeccakF1600(state)
    
    # === Squeeze out all the output blocks ===
    while(outputByteLen > 0):
    
        blockSize = min(outputByteLen, rateInBytes)
        outputBytes = outputBytes + state[0:blockSize]
        outputByteLen = outputByteLen - blockSize
    
        if (outputByteLen > 0):
            state = KeccakF1600(state)
    
    return outputBytes

def SHA3_256(inputBytes):
    return Keccak(1088, 512, inputBytes, 0x06, 256//8)

def SHA3_X(inputBytes, x):
    return Keccak(1600-x, x, inputBytes, 0x06, x//8)