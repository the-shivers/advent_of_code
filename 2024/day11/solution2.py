from collections import Counter
with open('input.txt') as file:
    stone_dict = Counter(map(int, file.readline().split()))

def dict_blink(d):
    for k, v in list(d.items()):
        d[k] -= v
        if k == 0:
            d[1] += v
        elif len(str(k)) % 2 == 0:
            d[int(str(k)[:len(str(k)) // 2])] += v
            d[int(str(k)[len(str(k)) // 2:])] += v
        else:
            d[k * 2024] += v
        if d[k] == 0:
            del d[k]
    return d

for i in range(75):
    dict_blink(stone_dict)
    if i == 24:
        print("Part 1:", sum(stone_dict.values()))
print("Part 2:", sum(stone_dict.values()))