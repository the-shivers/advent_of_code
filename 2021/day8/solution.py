def get_lines(filename):
    with open(filename) as raw:
        return [[i.split(), o.split()] for i, o in (line.strip().split(' | ') for line in raw)]

def count_easy(lines):
    return sum(len(s) in [2, 3, 4, 7] for _, output in lines for s in output)

def decypher(input):
    decoder = {}
    length_map = {2: 1, 3: 7, 4: 4, 7: 8}
    six_segment_digits = []
    five_segment_digits = []

    for s in input[:]:
        if len(s) in length_map:
            decoder[length_map[len(s)]] = set(s)
            input.remove(s)
        elif len(s) == 6:
            six_segment_digits.append(set(s))
        elif len(s) == 5:
            five_segment_digits.append(set(s))

    for s in six_segment_digits[:]:
        if decoder[4].issubset(s):
            decoder[9] = s
            six_segment_digits.remove(s)
        elif decoder[7].issubset(s):
            decoder[0] = s
            six_segment_digits.remove(s)
        else:
            decoder[6] = s

    for s in five_segment_digits[:]:
        if decoder[7].issubset(s):
            decoder[3] = s
            five_segment_digits.remove(s)
        elif s.issubset(decoder[6]):
            decoder[5] = s
            five_segment_digits.remove(s)
        else:
            decoder[2] = s

    return decoder

def decode_output(output, decoder):
    return int(''.join(str(k) for s in output for k, v in decoder.items() if v == set(s)))

def solve_part_2(lines):
    return sum(decode_output(output, decypher(input.copy())) for input, output in lines)

if __name__ == '__main__':
    filename = 'input.txt'
    lines = get_lines(filename)
    print(f'Answer to Part 1 is: {count_easy(lines)}')
    print(f'Answer to Part 2 is: {solve_part_2(lines)}')
