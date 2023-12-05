example = 'advent_of_code/2023/day5/example.txt'
input_txt = 'advent_of_code/2023/day5/input.txt'
with open(input_txt) as file:
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
        
# soils = [translate(i, sts_map) for i in seeds]
# ferts = [translate(i, stf_map) for i in soils]
# waters = [translate(i, ftw_map) for i in ferts]
# lights = [translate(i, wtl_map) for i in waters]
# temps = [translate(i, ltt_map) for i in lights]
# humids = [translate(i, tth_map) for i in temps]
# locs = [translate(i, htl_map) for i in humids]



# Part 2

# uhhhh....
# We need to split on breakpoints.
# create tree?
# tree = {}
# for row in sts_map:
#     tree[(row[1], row[1] + row[2] - 1)] = [row[0] - row[1], (row[0], row[0] + row[2] - 1)]

# tree2 = {}
# for row in stf_map:
#     tree2[(row[1], row[1] + row[2] - 1)] = [row[0] - row[1], (row[0], row[0] + row[2] - 1)]
    
# tree3 = {}
# for row in ftw_map:
#     tree3[(row[1], row[1] + row[2] - 1)] = [row[0] - row[1], (row[0], row[0] + row[2] - 1)]
    
    
    
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
# sts_map = [[50, 98, 2], [52, 50, 48]]
# stf_map = [[0, 15, 37], [37, 52, 2], [39, 0, 15]]
# seed_to_fert_map = [
#     [39, 0, 15],
#     [0, 15, 35],
#     [37, 50, 2],
#     [54, 52, 46],
#     [35, 98, 2],
# ] # Tested, it works

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


# def subdivide(sts_map, stf_map):
    


# [50, 97, []] # Seed start, seed end, soil modifier



# Seed start, seed end, modifier to get soil
# sts_map = [
#     [0, 49, [0]],
#     [50, 97, [2]],
#     [98, 99, [-48]],
#     [100, 999999999999999, [0]]
# ]

#sts updated
# [0, 49] 0,
# [52, 99] 2, 
# [50, 51] -48,
# [100, 999999999999999]] 0

# Overlaps between updated and stf
# [0, 14] 39
# [15, 49] -15
# [50-51] -63 => 98-99
# [52-53] -13 => 50-51
# [54-99] 2 => 52-97
# 100 0

# Translate back

# stf_map = [
#     [0, 14, [39]],
#     [15, 51, [-15]],
#     [52, 53, [-15]],
#     [54, 999999999999999, [0]]
# ]

# Levels 1 and 2 (goal)
# (0, 14): 39 (39, 53)
# (15-49): -15 (0, 34)
# (50-51): -13 (37, 38)
# (52-97): 2 (54, 99)
# (98-99): -63 (35, 36)
# (100): 0 (100, 100)

# Do we just get all beginnings and all ends?
# [0, 15, 50, 52, 54, 100]
# [14, 49, 51, 53, 99 ,99999999]
# # then pair?
# [[0, 14]], 

# nu_starts = 
# seed_rng = sts_map[0]
# soil_rng = [seed_rng[0] + seed_rng[2][0], seed_rng[1] + seed_rng[2][0]]
# for i in stf_map:
    
        
def update_map(old_map, new_map):
    old_updated = []
    for i in old_map:
        old_updated.append([
            i[0] + i[2][0], i[1] + i[2][0], i[2]
        ])
    starts = sorted(list(set([i[0] for i in old_updated + new_map])))
    ends = sorted(list(set([i[1] for i in old_updated + new_map])))
    new_map_untranslated = []
    for i in range(len(starts)):
        builder = [starts[i], ends[i], [0]]
        for j in old_updated:
            if starts[i] >= j[0] and ends[i] <= j[1]: #within 
                builder[2][0] += j[2][0]
        for j in new_map:
            if starts[i] >= j[0] and ends[i] <= j[1]: #within 
                builder[2][0] += j[2][0]
        new_map_untranslated += [builder]
    for i in range(len(new_map_untranslated)):
        for j in old_updated:
            if new_map_untranslated[i][0] >= j[0] and new_map_untranslated[i][1] <= j[1]:
                new_map_untranslated[i][0] -= j[2][0]
                new_map_untranslated[i][1] -= j[2][0]
                break
    return new_map_untranslated

def to_classic(new_map_style):
    classic = []
    for row in new_map_style:
        builder = []
        builder.append(row[0] + row[2][0])
        builder.append(row[0])
        builder.append(row[1]-row[0]+1)
        classic.append(builder)
    return classic

def to_new(classic_map_style):
    new = []
    for row in classic_map_style:
        builder = []
        builder.append(row[1])
        builder.append(row[1] + row[2] - 1)
        builder.append([row[0] - row[1]])
        new.append(builder)
    has_zero = False
    min_start = 999999999999999
    has_big = False # 999999999999999
    max_end = 0
    for row in new:
        if row[0] == 0:
            has_zero = True
        if row[1] == 999999999999999:
            has_big = True
        if row[0] < min_start:
            min_start = row[0]
        if row[1] > max_end:
            max_end = row[1]
    if not has_zero:
        new.append([0, min_start - 1, [0]])
    if not has_big:
        new.append([max_end + 1, 999999999999999, [0]])
    return new
        

# level 1
# (50, 97): [2, (52, 99)]
# (98, 99): [-48, (50, 51)]

# sts_map = [[50, 98, 2], [52, 50, 48]]
# stf_map = [[0, 15, 37], [37, 52, 2], [39, 0, 15]]
# seed_to_fert_map = [
#     [39, 0, 15],
#     [0, 15, 35],
#     [37, 50, 2],
#     [54, 52, 46],
#     [35, 98, 2],
# ] # Tested, it works  



seeds, sts_map, stf_map, ftw_map, wtl_map, ltt_map, tth_map, htl_map = get_maps(lines)

new_sts_map = to_new(sts_map)
new_stf_map = to_new(stf_map)
new_ftw_map = to_new(ftw_map)
new_wtl_map = to_new(wtl_map)
new_ltt_map = to_new(ltt_map)
new_tth_map = to_new(tth_map)
new_htl_map = to_new(htl_map)

combine1 = update_map(new_sts_map, new_stf_map)
classic_seed_to_fert = to_classic(combine1)
combine2 = update_map(combine1, new_ftw_map)
classic_seed_to_water = to_classic(combine2)
combine3 = update_map(combine2, new_wtl_map)
classic_seed_to_light = to_classic(combine3)
combine4 = update_map(combine3, new_ltt_map)
classic_seed_to_temp = to_classic(combine4)
combine5 = update_map(combine4, new_tth_map)
classic_seed_to_humid = to_classic(combine5)
combine6 = update_map(combine5, new_htl_map)
classic_seed_to_loc = to_classic(combine6)

# seeds
# new_seeds = []
# for i in range(0, len(seeds), 2):
#     for j in range(seeds[i + 1]):
#         print(i, j)
#         new_seeds += [seeds[i] + j]
        


[translate(i, classic_seed_to_fert) for i in seeds]
[translate(i, classic_seed_to_water) for i in seeds]
[translate(i, classic_seed_to_light) for i in seeds]
[translate(i, classic_seed_to_temp) for i in seeds]
[translate(i, classic_seed_to_humid) for i in seeds]
[translate(i, classic_seed_to_loc) for i in seeds]

min([translate(i, classic_seed_to_loc) for i in new_seeds])

def custom_sort(lst):
    return sorted(lst, key=lambda x: x[0])

# We only need to check the edges of the seed buckets and our buckets
# LEt's test the theory. We'll generate seed ranges.
[translate(i, classic_seed_to_loc) for i in new_seeds]
new_seeds
custom_sort(combine6)



# So yes, we just need edges. seed_edges first
edge_list = []
for i in range(0, len(seeds), 2):
    edge_list+=[seeds[i], seeds[i] + seeds[i+1]]
    
seed_ranges = []
for i in range(0, len(seeds), 2):
    seed_ranges.append((seeds[i], seeds[i] + seeds[i+1]))
    
edge_list2 = []
for i in range(0, len(combine6), 2):
    edge_list2+=[combine6[0], combine6[1]]
    
edge_list3 = []
for i in edge_list2:
    for j in seed_ranges:
        print(i, j)
        edge_list3 += [i[0]] if i[0] >= j[0] and i[0] < j[1] else [0]
        edge_list3 += [i[1]] if i[1] >= j[0] and i[1] < j[1] else [0]
edge_list3 = list(set(edge_list3))
edge_list3 = [i for i in edge_list3 if i > 0]

    
final_edge_locs = [translate(i, classic_seed_to_loc) for i in edge_list + edge_list3]
# 305466162 is too high
# for this seed? 2738486655

translate(2738486655, classic_seed_to_loc) # 305466162
translate(305466162, classic_seed_to_loc)  # 4054967413
translate(4239267129, classic_seed_to_loc) # 896125601
translate(911212652, classic_seed_to_loc)  # 332823205
translate(2433934396, classic_seed_to_loc) # 138114552
translate(2433336664, classic_seed_to_loc) # 138114552


# For each bucket, lets find out if we have seeds in it.
sorted_bucket = custom_sort(combine6)

for bucket in sorted_bucket:
    for rng in seed_ranges:
        if rng[0] >= bucket[0] and rng[0] <= bucket[1]:
            print('bucket has seed!', bucket)
            print('bseed at bottom of bucket')
        if rng[1] - 1 >= bucket[0] and rng[1] - 1 <= bucket[1]:
            print('bucket has seed!', bucket)
            print('bseed at top of bucket')
            print(rng[1])

# 2433934396
# (2354891449, 2592044334) seed range
#  [2433336664, 2466745844, [-2295819844]] bucket range

import matplotlib.pyplot as plt
import numpy as np
import random

# Step function definition
step_function = [
[21006552, 23932217, [2118000943]],
 [23932218, 66948581, [3216530819]],
 [66948582, 71705009, [3216530819]],
 [71705010, 99708532, [2037080041]],
 [99708533, 101927453, [2037080041]],
 [116638140, 124534616, [2767635833]],
 [124534617, 208686805, [2767635833]],
 [208686806, 237483913, [1992282999]],
 [237483914, 248421505, [1992282999]],
 [248421506, 283074538, [521325695]],
 [283074539, 288918561, [1290378205]],
 [288918562, 326219312, [3749501251]],
 [326219313, 335738672, [3749501251]],
 [335738673, 414344678, [2952497156]],
 [414344679, 432366319, [1077178170]],
 [432366320, 466126327, [-428476810]],
 [481649445, 641364295, [2914874078]],
 [641364296, 641886785, [165614037]],
 [789510941, 789510940, [834675520]],
 [832476273, 832476272, [1201025465]],
 [832476273, 834684214, [3113180891]],
 [834684215, 893720858, [1307248946]],
 [893720859, 897602251, [3191519065]],
 [897602252, 1026604245, [-578389447]],
 [1026604246, 1116033066, [-988954728]],
 [1116033067, 1129066740, [1188686802]],
 [1129066741, 1181889284, [1188686802]],
 [1181889285, 1210018623, [83447865]],
 [1210018624, 1262605140, [216849759]],
 [1262605141, 1300529010, [1203186576]],
 [1300529011, 1351323942, [1114467774]],
 [1351323943, 1397856338, [2463800936]],
 [1397856339, 1399635828, [499431866]],
 [1399635829, 1411023848, [499431866]],
 [1411023849, 1430656934, [1194727272]],
 [1430656935, 1447289333, [1194727272]],
 [1447289334, 1452959758, [-639788511]],
 [1452959759, 1482511955, [-639788511]],
 [1482511956, 1497378065, [-639788511]],
 [1552322736, 1552322735, [-1051183008]],
 [1584816050, 1584816049, [-108253744]],
 [1584816050, 1585939057, [2299402329]],
 [1585939058, 1604095071, [-292472569]],
 [1655608967, 1655608966, [-3204745037]],
 [1655608967, 1672886659, [2566261498]],
 [1672886660, 1693684694, [1428654683]],
 [1693684695, 1704123175, [-1566606356]],
 [1704123176, 1714220499, [1662718659]],
 [1714220500, 1749742786, [-109831373]],
 [1749742787, 1773785332, [2135598600]],
 [1773785333, 1789656337, [875419560]],
 [1789656338, 1794605053, [-1027624760]],
 [1794605054, 1797371960, [-1027624760]],
 [1797371961, 1798780817, [443332544]],
 [1798780818, 1814064011, [-117011033]],
 [1814064012, 1814932253, [-117011033]],
 [1814932254, 1820552130, [29409565]],
 [1820552131, 1823543177, [1572980345]],
 [1823543178, 1829281996, [1160343875]],
 [1829281997, 1829281996, [-86553821]],
 [1892530428, 1894627066, [-86553821]],
 [1894627067, 1895696670, [1482312092]],
 [1895696671, 1900163269, [-1243175122]],
 [1900163270, 1907769068, [2188958047]],
 [1907769069, 1953269061, [2188958047]],
 [1953269062, 1955852812, [-1430443968]],
 [2027746720, 2027746719, [95183873]],
 [2267862848, 2284719018, [107295649]],
 [2284719019, 2291907305, [357297587]],
 [2291907306, 2294485404, [-1487507072]],
 [2294485405, 2353842284, [-273332718]],
 [2353842285, 2378550831, [371255811]],
 [2378550832, 2408112944, [1860597326]],
 [2408112945, 2430496993, [1860597326]],
 [2430496994, 2433336663, [-580535298]],
 [2433336664, 2466745844, [-2295819844]],
 [2466745845, 2486663524, [753799512]],
 [2486663525, 2525803569, [-969174714]],
 [2525803570, 2549498771, [1632934711]],
 [2549498772, 2607115195, [115577126]],
 [2607115196, 2609520969, [115577126]],
 [2609520970, 2637796453, [-529011403]],
 [2637796454, 2664182387, [220091585]],
 [2664182388, 2668361193, [-856109142]],
 [2668361194, 2747799879, [-2433020493]],
 [2747799880, 2752993202, [630208883]],
 [2752993203, 2781954322, [1156390730]],
 [2781954323, 2785827298, [1509139997]],
 [2785827299, 2786341875, [-275061400]],
 [2786341876, 2802459127, [-2129353728]],
 [2802459128, 2886680721, [-865528035]],
 [2886680722, 3008494426, [669557652]],
 [3008494427, 3026735117, [-2055643846]],
 [3026735118, 3089988645, [-2578520319]],
 [3098487039, 3105487226, [-519161940]],
 [3105487227, 3130579586, [-1526190460]],
 [3130579587, 3228785565, [-8240209]],
 [3228785566, 3245296737, [913441543]],
 [3245296738, 3299327385, [-3074370737]],
 [3299327386, 3304342814, [-725017716]],
 [3304342815, 3402192560, [-1984749575]],
 [3402192561, 3411617957, [-1984749575]],
 [3411617958, 3416200367, [-1041041871]],
 [3416200368, 3467470663, [-2705439086]],
 [3467470664, 3484833131, [-910523462]],
 [3484833132, 3495217183, [-3259876483]],
 [3495217184, 3603298579, [-745410541]],
 [3603298580, 3619085601, [-3077889735]],
 [3820897110, 3843879226, [-1428882442]],
 [3843879227, 3855458271, [-2364424327]],
 [3855458272, 3855947175, [-2364424327]],
 [3855947176, 3861842845, [-2003145810]],
 [3861842846, 3907509571, [-1350562370]],
 [3907509572, 3946946553, [274923911]],
 [3946946554, 3954917290, [-2635324051]],
 [3954917291, 3955612580, [-2983826019]],
 [3955612581, 3959502090, [-3955612581]],
 [3959502091, 3967446411, [-2449957601]],
 [3967446412, 3990007515, [-105789137]],
 [3990007516, 4019212983, [-3066362403]],
 [4019212984, 4029543373, [-636010898]],
 [4029543374, 4034632390, [-3488347507]],
 [4034632391, 4100038840, [-3488347507]],
 [4100038841, 4140869055, [-3488347507]],
 [4140869056, 4178524937, [-3467763656]],
 [4178524938, 4200731082, [-500472859]],
 [4200731083, 4266786640, [-3343141528]],
 [4266786641, 4278143407, [-3755318314]],
 [4278143408, 4294967295, [-2721514552]],
 [4294967296, 4398120065, [0]],
 [4398120066, 4450310058, [0]],
 [4450310059, 999999999999999, [0]]]

# Given ranges for uniform sampling
ranges = [
    (4239267129, 4259728934),
    (2775736218, 2828126748),
    (3109225152, 3850550524),
    (1633502651, 1680409289),
    (967445712, 1014538181),
    (2354891449, 2592044334),
    (2169258488, 2280443291),
    (2614747853, 2738486655),
    (620098496, 911212652),
    (2072253071, 2100364273)
]

# Uniform sampling from the given ranges
sample_size = 20000
x_values = []

for r in ranges:
    x_values.extend(random.sample(range(r[0], r[1] + 1), sample_size // len(ranges)))

# Applying the step function to the sampled x-values
y_values = []
for x in x_values:
    for step in step_function:
        added = False
        if step[0] <= x <= step[1]:
            y_values.append(x + step[2][0])
            added = True
            break
    if not added:
        y_values.append(x)

# Plotting
plt.figure(figsize=(10, 6))
plt.scatter(x_values, y_values, s=1)
plt.title("Stepwise Function Plot")
plt.xlabel("X-values")
plt.ylabel("Y-values (after step function)")
plt.show()