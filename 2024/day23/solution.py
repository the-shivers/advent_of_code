def part1(pairs):
    t_pairs, trios = set(), set()
    for pair in pairs:
        if any(s[0] == 't' for s in pair):
            t_pairs.add(pair)
    for pair1 in t_pairs:
        for pair2 in t_pairs:
            if pair1 == pair2:
                continue
            if any(s[0] == 't' for s in pair1 & pair2):
                if pair1 ^ pair2 in pairs:
                    trios.add(pair1 | pair2)
    print("Part 1:", len(trios))

def part2(pairs):
    clusters = []
    for pair in pairs:
        clusters.append(set(pair))
        for cluster in clusters:
            for item in pair:
                if item not in cluster:
                    if all(frozenset({cluster_item, item}) in pairs for cluster_item in cluster):
                        cluster.add(item)
    print("Part 2:", ",".join(sorted(max(clusters, key=len))))

with open('input.txt') as file:
    pairs = set([frozenset(line.strip().split('-')) for line in file])
part1(pairs)
part2(pairs)



