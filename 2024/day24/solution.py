from collections import deque

inputs = {}
combos = deque()

# input_txt = 'example.txt'
input_txt = 'input.txt'
with open(input_txt) as file:
    for line in file:
        if not line.strip():
            continue
        if ':' in line:
            k, v = line.strip().split(': ')
            inputs[k] = int(v)
        else:
            combos.append([i for i in line.strip().split(' ') if i != '->'])

def swap_outputs(combos, o1, o2):
    for combo1 in combos:
        if combo1[3] == o1:
            for combo2 in combos:
                if combo2[3] == o2:
                    print("Found. Swapping")
                    combo1[3], combo2[3] = o2, o1
                    return combos
        elif combo1[3] == o2:
            for combo2 in combos:
                if combo2[3] == o1:
                    print("Found. Swapping")
                    combo1[3], combo2[3] = o1, o2
                    return combos

# combos = swap_outputs(combos, 'kth', 'z12')
# combos = swap_outputs(combos, 'gsd', 'z26')
# combos = swap_outputs(combos, 'z32', 'tbt')
# combos = swap_outputs(combos, 'qnf', 'vpm')
print("Part 2:", ",".join(sorted(['kth', 'z12', 'gsd', 'z26', 'z32', 'tbt', 'qnf', 'vpm'])))


def evaluate(input1, operator, input2):
    if operator == 'AND': return input1 and input2
    elif operator == 'OR': return input1 or input2
    elif operator == 'XOR': return input1 ^ input2

def fill_inputs(inputs, combos):
    while combos:
        curr = combos.pop()
        if curr[0] in inputs and curr[2] in inputs:
            inputs[curr[3]] = evaluate(inputs[curr[0]], curr[1], inputs[curr[2]])
        else:
            combos.appendleft(curr)
    return inputs

inputs = fill_inputs(inputs, combos)
print("Part 1", int(''.join(str(inputs[k]) for k in sorted((k for k in inputs if k.startswith('z')), reverse=True)), 2))

# Part 2
x_str = ''.join([str(inputs[k]) for k in sorted((k for k in inputs if k.startswith('x')), reverse=True)])
y_str = ''.join([str(inputs[k]) for k in sorted((k for k in inputs if k.startswith('y')), reverse=True)])
target = int(x_str, 2) + int(y_str, 2)
bin_target = bin(target)
print('t:', str(bin_target)[2:]) # target
print('c:', ''.join(str(inputs[k]) for k in sorted((k for k in inputs if k.startswith('z')), reverse=True))) # current



# X    =  111101101000101000010100000000100001000111001
# Y    =  100111010001000111010010000000011111010101111
# Targ = 1100100111001101111100110000001000000011101000
# Curr = 1100101000010010000000110000000111000011101000
#      =       #### #########          ####

# Targ = 1100100111001101111100110000001000000011101000
# Curr = 1100101000010010000000110000001000000011101000
#      =       #### #########

# t: 1100100111001101111100110000001000000011101000
# c: 1100101000001101111100110000001000000011101000
#    45 42
# seems like 36 is first fuckup?

# hhd XOR qnv -> z39
# 
# phr XOR ths -> z38
#
# hpp XOR wkk -> z37
# 
# htb XOR qnf -> z36
# 


# ksf XOR bhh -> z34
#
# nwm XOR rpb -> z33
#
# vtg AND bkh -> z32
# 
# trd XOR dtj -> z31
#
# nvq XOR gtd -> z30
#
# fht XOR vbp -> z29
#
# ghk XOR pgc -> z28
# 
# swt XOR cmf -> z27
#
# x26 AND y26 -> z26
#


# ckk XOR sqb -> z15
# 
# rpt XOR hbh -> z14
#
# mtp XOR kth -> z13
#
# psw OR nng -> z12
#     x12 AND y12 -> psw
#     nhb AND cdq -> nng


# Now for some correct ones.
# x00 XOR y00 -> z00

# twd XOR bdj -> z01
#    y01 XOR x01 -> twd (z1 addition ignoring carried 1)
#    x00 AND y00 -> bdj (carred one from z0)

# rsk XOR rhr -> z02
#    x02 XOR y02 -> rsk  (direct comparison of x02 and y02)
#    cbq OR gwd -> rhr (Either raw one or carried one)
#    twd AND bdj -> cbq (Carried one)
#    y01 AND x01 -> gwd (Raw one)

# jfr XOR twj -> z03
#    x03 XOR y03 -> jfr (direct comparison)
#    fph OR nkm -> twj (Either raw one or carred one)
#    rhr AND rsk -> nkm (Carried one)
#    y02 AND x02 -> fph (Raw one)

# Seems like a pattern. Let's skip to the first wrong one.

# psw OR nng -> z12
#    y12 XOR x12 -> nhb (Direct comparison)
#    fkw OR mdq -> cdq
#    nhb AND cdq -> nng
#    x12 AND y12 -> psw (Raw one.)

# So we see a few things. 
# The top level circuit is OR instead of XOR (wrong).
# The Raw one seems to be the raw one for THIS circuit instead of the last one.
# We SHOULD have 
# nhb XOR (Either raw one or carred one)
# raw one should be mdq: x11 AND y11 -> mdq 
# carried one should be: AND of previous z. tnr XOR kdw -> z11. So tnr AND kdw. 
# so we SHOULD have...

# (x03 XOR y03) XOR ((cmp1 of prev topline z AND cmp2 of prev topline z) OR (x02 AND y02)) -> z12
# (x12 XOR y12) XOR ((tnr AND kdw) OR (x11 AND y11)) -> z12

# x11 AND y11 -> mdq
# fkw OR mdq -> cdq
# nhb XOR cdq -> kth # maybe this is the row that should swap with (psw OR nng -> z12)

# This would give us

# nhb XOR cdq -> z12
# psw OR nng -> kth

# Trying to confirm

# nhb XOR cdq -> z12
#    y12 XOR x12 -> nhb (direct comparison)
#    fkw OR mdq -> cdq (Either raw one or carried one)
#    tnr AND kdw -> fkw (carried one because tnr XOR kdw -> z11)
#    x11 AND y11 -> mdq (raw one)

# CORRECT. What was the other thing we fixed?

# mtp XOR kth -> z13
#    x13 XOR y13 -> mtp (direct comparison)
#    psw OR nng -> kth (Either raw one or carried one)
#    nhb AND cdq -> nng
#    x12 AND y12 -> psw

# YES! LETS GO!

# x26 AND y26 -> z26
# i mean, obviously this is fucking wrong lol. 
# Correct would be...
# (x26 XOR y26) XOR ((tnr AND kdw) OR (x25 AND y25)) -> z26
# y26 XOR x26 -> dfp
# x25 AND y25 -> qmv
# qmv OR ftq -> mbg
# pmm AND msc -> ftq (where pmm XOR msc -> z25)
# So the one to swap would be dfp XOR mbg -> gsd
# Swap gsd and z26

# Okay, next 
# vdn OR qtn -> z45
# we SHOULD have 
# (x45 XOR y45) XOR ((tnr AND kdw) OR (x44 AND y44)) -> z45
# oh this one might be correct lol


# Finally
# vtg AND bkh -> z32
# (x32 XOR y32) XOR ((tnr AND kdw) OR (x31 AND y31)) -> z32
# x32 XOR y32 -> bkh
# x31 AND y31 -> nhq
# trd XOR dtj -> z31
# dtj AND trd -> bjf
# bjf xor bkh
# nhq OR bjf -> vtg is the same as (dtj AND trd) OR (x31 AND y31)

# bkh XOR vtg
# vtg XOR bkh -> tbt (found in input)


# Okay so confirmed: we swap z32 and tbt. This makes z32:
# vtg XOR bkh -> z32
#    x32 XOR y32 -> bkh
#    nhq OR bjf -> vtg
#    dtj AND trd -> bjf (where trd XOR dtj -> z31)
#    x31 AND y31 -> nhq
# NICE!

# ALright, no nice XOR mistake to make this easy, but it looks like z36 has the issue.
# htb XOR qnf -> z36
# y36 AND x36 -> qnf
# bbb OR cnp -> htb
# x35 AND y35 -> cnp
# jng AND brg -> bbb (where jng XOR brg -> z35)

# Correct would be:
# (x36 XOR y36) XOR ((tnr AND kdw) OR (x35 AND y35))

# y36 XOR x36 -> vpm THIS IS WRONG! 
# Maybe we swap qnf (y36 AND x36) with vpm (y36 XOR x36)
