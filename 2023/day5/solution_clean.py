# Functions
def parse_map_section(lines, start_line):
    map_data = []
    for line in lines[start_line:]:
        if line == '':
            break
        map_data.append([int(i) for i in line.split()])
    return map_data


def get_maps(lines):
    maps = {
        'seed-to-soil map': [],
        'soil-to-fertilizer map': [],
        'fertilizer-to-water map': [],
        'water-to-light map': [],
        'light-to-temperature map': [],
        'temperature-to-humidity map': [],
        'humidity-to-location map': []
    }
    seeds = []
    for row, line in enumerate(lines):
        if line.startswith('seeds:'):
            seeds = [int(i) for i in line.split()[1:]]
        else:
            for map_name in maps:
                if line.startswith(map_name.split()[0]):
                    maps[map_name] = parse_map_section(lines, row + 1)
                    break
    return seeds, *maps.values()


def translate(item, my_map):
    for row in my_map:
        if item >= row[1] and item < row[1] + row[2]:
            return row[0] + item - row[1]
    return item


def fill_missing_intervals(intervals):
    # input: [(3, 5)]; output: [(0, 2), (3, 5), (6, 999999999999999)]
    intervals.sort()
    filled_intervals = []
    start = 0
    for interval in intervals:
        if interval[0] > start:
            filled_intervals.append((start, interval[0] - 1))
        filled_intervals.append(interval)
        start = interval[1] + 1
    if start <= 999999999999999:
        filled_intervals.append((start, 999999999999999))
    return filled_intervals


def get_combined_map(base_map, update_map):
    # Combines 2 maps, e.g. seed2soil map and soil2fert map => seed2fert map
    # Get base_map destination intervals
    bm_dests = []
    for row in base_map:
        bm_dests.append((row[0], row[0] + row[2] - 1))
    # Get update map source intervals
    um_sources = []
    for row in update_map:
        um_sources.append((row[1], row[1] + row[2] - 1))
    # Make our lives easier by filling in missing intervals
    # e.g. if all we have is [(5, 10)] then update
    # it so we have [(0, 4), (5, 10), (11, 999999999999999)]
    bm_dests = fill_missing_intervals(bm_dests)
    um_sources = fill_missing_intervals(um_sources)
    # Create new set of non-overlapping intervals from these.
    # Because we filled in gaps, the resulting intervals will just 
    # be the sorted start and end dates, paired up
    starts = sorted(list(set([tup[0] for tup in bm_dests + um_sources])))
    ends = sorted(list(set([tup[1] for tup in bm_dests + um_sources])))
    new_intervals = [(start, end) for start, end in zip(starts, ends)]
    # It's key to remember these are soil-to-fertilizer source intervals!
    # Let's put them back into the usual map format: [dest, orig, len]
    subdivided_update_map = []
    for start, end in new_intervals:
        added = False
        # Check if new interval is within update_map:
        for row in update_map:
            if start >= row[1] and end <= row[1] + row[2] - 1:
                subdivided_update_map.append(
                    [start - (row[1] - row[0]), start, end - start + 1]
                )
                added = True
                break
        if not added:
            subdivided_update_map.append([start, start, end - start + 1])
    # Now we have a subdivided soil-to-fertilizer map in the standard format
    # Finally we translate back to seed-to-fertilizer maps in standard format
    # by checking if intervals fall in seed-to-fert destination intervals
    subdivided_base_map = []
    for update_row in subdivided_update_map:
        added = False
        for base_row in base_map:
            # Check if soil-to-fertilizer source interval
            # is contained by seed-to-soil dest interval, if so, translate
            if (update_row[1] >= base_row[0] and 
                update_row[1] + update_row[2] - 1 <= base_row[0] + base_row[2] - 1):
                subdivided_base_map.append([
                    update_row[0],
                    update_row[1]  + (base_row[1] - base_row[0]),
                    update_row[2] # Interval sizes need no modification
                ])
                added = True
                break
        # If an interval is not covered by seed-to-soil
        # we use raw soil-to-fertilizer mapping
        if not added:
            subdivided_base_map.append(update_row) 
    return subdivided_base_map


# Analysis
example = 'advent_of_code/2023/day5/example.txt'
input_txt = 'advent_of_code/2023/day5/input.txt'
with open(input_txt) as file:
    lines = [line.strip() for line in file]
seeds, sts_map, stf_map, ftw_map, wtl_map, ltt_map, tth_map, htl_map = get_maps(lines)

seed_to_fert_map = get_combined_map(sts_map, stf_map)
seed_to_water_map = get_combined_map(seed_to_fert_map, ftw_map)
seed_to_light_map = get_combined_map(seed_to_water_map, wtl_map)
seed_to_temp_map = get_combined_map(seed_to_light_map, ltt_map)
seed_to_humid_map = get_combined_map(seed_to_temp_map, tth_map)
seed_to_loc_map = get_combined_map(seed_to_humid_map, htl_map)

# PT 1
min([translate(i, seed_to_loc_map) for i in seeds])

# PT 2
# Since within each interval of the soil_to_loc_map, the lowest seed value
# represents the lowest loc value, we only need to check the edges
# of seed ranges, and edges of soil_to_loc_map intervals.
interval_edges = []
for row in seed_to_loc_map:
    l_edge = row[1]
    r_edge = row[1] + row[2] - 1
    interval_edges += [l_edge, r_edge]
    
seed_ranges = []
for i in range(0, len(seeds), 2):
    seed_ranges.append((seeds[i], seeds[i] + seeds[i + 1 ] - 1))
    
valid_interval_edges = []
for edge in interval_edges:
    for rng in seed_ranges:
        if edge >= rng[0] and edge <= rng[1]: # <= since we subtract 1 above
            valid_interval_edges.append(edge)

seed_edges = [element for tup in seed_ranges for element in tup]

min([translate(i, seed_to_loc_map) for i in seed_edges + valid_interval_edges])
