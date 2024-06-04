with open('input.txt') as lines:
    depths = [int(line.strip()) for line in lines]

def get_pt1_result(depths):
    pt1_result = 0
    for i in range(1, len(depths)):
        if depths[i] > depths[i - 1]:
            pt1_result += 1
    return pt1_result

def get_pt2_result(depths):
    pt2_result = 0
    for i in range(3, len(depths)):
        sum_a = sum(depths[i - 3 : i])
        sum_b = sum(depths[i - 2 : i + 1])
        if sum_b > sum_a:
            pt2_result += 1
    return pt2_result

if __name__ == '__main__':
    print(f'"Answer to pt1: {get_pt1_result(depths)}')
    print(f'"Answer to pt1: {get_pt2_result(depths)}')