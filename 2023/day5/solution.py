example = 'advent_of_code/2023/day5/example.txt'
input_txt = 'advent_of_code/2023/day5/input.txt'
with open(example) as file:
    lines = [line.strip() for line in file]

def get_maps(lines):
    for row, line in enumerate(lines):
        if len(line) > 4 and line[0:5] == 'seeds':
            seeds = [int(i) for i in line.split()[1:]]
        if len(line) > 5 and line[0:5] == 'seed-':
            subline = row + 1
            sts_map = []
            while lines[subline] != '':
                sts_map += [[int(i) for i in lines[subline].split()]]
                subline += 1
        if len(line) > 5 and line[0:5] == 'soil-':
            subline = row + 1
            stf_map = []
            while lines[subline] != '':
                stf_map += [[int(i) for i in lines[subline].split()]]
                subline += 1
        if len(line) > 5 and line[0:5] == 'ferti':
            subline = row + 1
            ftw_map = []
            while lines[subline] != '':
                ftw_map += [[int(i) for i in lines[subline].split()]]
                subline += 1
        if len(line) > 5 and line[0:5] == 'water':
            subline = row + 1
            wtl_map = []
            while lines[subline] != '':
                wtl_map += [[int(i) for i in lines[subline].split()]]
                subline += 1
        if len(line) > 5 and line[0:5] == 'light':
            subline = row + 1
            ltt_map = []
            while lines[subline] != '':
                ltt_map += [[int(i) for i in lines[subline].split()]]
                subline += 1
        if len(line) > 5 and line[0:5] == 'tempe':
            subline = row + 1
            tth_map = []
            while lines[subline] != '':
                tth_map += [[int(i) for i in lines[subline].split()]]
                subline += 1
        if len(line) > 5 and line[0:5] == 'humid':
            subline = row + 1
            htl_map = []
            while subline <= len(lines) - 1 and lines[subline] != '':
                htl_map += [[int(i) for i in lines[subline].split()]]
                subline += 1
    return seeds, sts_map, stf_map, ftw_map, wtl_map, ltt_map, tth_map, htl_map

def translate(item, my_map):
    for row in my_map:
        if item >= row[1] and item < row[1] + row[2]:
            return row[0] + item - row[1]
    return item
        
seeds, sts_map, stf_map, ftw_map, wtl_map, ltt_map, tth_map, htl_map = get_maps(lines)
        
soils = [translate(i, sts_map) for i in seeds]
ferts = [translate(i, stf_map) for i in soils]
waters = [translate(i, ftw_map) for i in ferts]
lights = [translate(i, wtl_map) for i in waters]
temps = [translate(i, ltt_map) for i in lights]
humids = [translate(i, tth_map) for i in temps]
locs = [translate(i, htl_map) for i in humids]



# Part 2

# uhhhh....
# We need to split on breakpoints.
# create tree?
tree = {}
for row in sts_map:
    tree[(row[1], row[1] + row[2] - 1)] = [row[0] - row[1], (row[0], row[0] + row[2] - 1)]

tree2 = {}
for row in stf_map:
    tree2[(row[1], row[1] + row[2] - 1)] = [row[0] - row[1], (row[0], row[0] + row[2] - 1)]
    
tree3 = {}
for row in ftw_map:
    tree3[(row[1], row[1] + row[2] - 1)] = [row[0] - row[1], (row[0], row[0] + row[2] - 1)]
    
    
    
# {(98, 99): [-48, (50, 51)], (50, 97): [2, (52, 99)]}
# {(15, 51): [-15, (0, 36)], (52, 53): [-15, (37, 38)], (0, 14): [39, (39, 53)]}
# {(53, 60): [-4, (49, 56)], (11, 52): [-11, (0, 41)], (0, 6): [42, (42, 48)], (7, 10): [50, (57, 60)]}

# to produce:
#


# level 1
# (50, 97): [2, (52, 99)]
# (98, 99): [-48, (50, 51)]

# level 2
# (52, 53): [-15, (37, 38)]
# (15, 51): [-15, (0, 36)]
# (0,  14):  [39, (39, 53)]

# level 3
# (53, 60): [-4, (49, 56)], 
# (11, 52): [-11, (0, 41)], 
# (0,   6): [42, (42, 48)], 
# (7,  10): [50, (57, 60)]

# Levels 1 and 2
# (0, 14): 39 (39, 53)
# (15-49): -15 (0, 34)
# (50-51): -13 (37, 38)
# (52-97): 2 (54, 99)
# (98-99): -63 (35, 36)
# (100): 0 (100, 100)

# Levels 1 and 2
sts_map = [[50, 98, 2], [52, 50, 48]]
stf_map = [[0, 15, 37], [37, 52, 2], [39, 0, 15]]
seed_to_fert_map = [
    [39, 0, 15],
    [0, 15, 35],
    [37, 50, 2],
    [54, 52, 46],
    [35, 98, 2],
] # Tested, it works

# Levels 1, 2 and 3
# (0, 13): 28 (28, 41)
# (14, 14): 25 (49, 49)
# (15, 21): 27 (42, 48)
# (22, 25): 35 (57, 60)
# (26, 49): -26 (0, 23)
# (50, 51): -24 (26, 27)
# (52, 58): -2 (50, 56)
# (59, 97): 2 (61, 97)
# (98, 99): -74 (24, 25)
# (100, 100): 0 (100, 100)

# This is the way.


def subdivide(sts_map, stf_map):
    


[50, 97, []] # Seed start, seed end, soil modifier



# Seed start, seed end, modifier to get soil
sts_map = [
    [0, 49, [0]],
    [50, 97, [2]],
    [98, 99, [-48]],
    [100, 999999999999999, [0]]
]

#sts updated
# [0, 49],
# [52, 99], 
# [50, 51],
# [100, 999999999999999]]

stf_map = [
    [0, 14, [39]],
    [15, 51, [-15]],
    [52, 53, [-15]],
    [54, 999999999999999, [0]]
]

# Levels 1 and 2 (goal)
# (0, 14): 39 (39, 53)
# (15-49): -15 (0, 34)
# (50-51): -13 (37, 38)
# (52-97): 2 (54, 99)
# (98-99): -63 (35, 36)
# (100): 0 (100, 100)


sts_map_updated = []
for rng in sts_map:
    sts_map_updated.append([rng[0] + rng[2][0], rng[1] + rng[2][0]])
    # Now that they're both in soil mode, 
