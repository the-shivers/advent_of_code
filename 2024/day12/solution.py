import time

input_txt = 'input.txt'
with open(input_txt) as file:
    lines = [list(line.strip()) for line in file]

height = len(lines)
width = len(lines[0])

# Part 1
def get_region(curr, area, bounds, lines):
    x, y = curr
    for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
        new_x, new_y = x + dx, y + dy
        if (new_x, new_y) in area or ((new_x, new_y), (dx, dy)) in bounds:
            continue
        if 0 <= new_x < width and 0 <= new_y < height:
            if lines[new_y][new_x] == lines[y][x]:
                area.add((new_x, new_y))
                get_region((new_x, new_y), area, bounds, lines)
            else:
                bounds.add(((new_x, new_y), (dx, dy)))
        else:
            bounds.add(((new_x, new_y), (dx, dy)))
    return area, bounds

def get_leftmost_upper_bound(bounds_set):
    min_y = 9999
    for (x, y), (dx, dy) in bounds_set:
        if (dx, dy) == (0, -1): # Indicates top boundary
            if y < min_y:
                min_y = y
    best_bound_so_far = ((99999, 99999), (0, -1))
    for (x, y), (dx, dy) in bounds_set:
        if (dx, dy) == (0, -1) and y == min_y:
            if x < best_bound_so_far[0][0]:
                best_bound_so_far = ((x, y), (dx, dy))
    return best_bound_so_far

def get_continuous_sides(bounds_set):
    curr = get_leftmost_upper_bound(bounds_set)
    bounds_set.remove(curr)
    sides = 1
    while bounds_set:
        # time.sleep(0.5)
        (curr_x, curr_y), (dx, dy) = curr
        print(curr, len(bounds_set), "sides:", sides)
        if (dx, dy) == (0, 1):
            # Crossed this boundary from above i.e. we're on bottom. Move left.
            # AAAA
            # ....
            if ((curr_x - 1, curr_y), (0, 1)) in bounds_set:
                curr = ((curr_x - 1, curr_y), (0, 1))
                bounds_set.remove(curr)
                # print('going left')
                continue
            elif ((curr_x - 1, curr_y - 1), (-1, 0)) in bounds_set: 
                # Turn right (up) as a corner
                # .AAA
                # ....
                curr = ((curr_x - 1, curr_y - 1), (-1, 0))
                bounds_set.remove(curr)
                # print('turning right (was going left, now going up)')
                sides += 1
                continue
            elif ((curr_x, curr_y), (1, 0)) in bounds_set: 
                # Turn left (down) as a corner
                # AAAA
                # A...
                curr = ((curr_x, curr_y), (1, 0))
                bounds_set.remove(curr)
                # print('turning left (was going left, now going down)')
                sides += 1
                continue
        elif (dx, dy) == (-1, 0):
            # Crossed this boundary from right to left, we're on left. Move up.
            # ..AA
            # ..AA
            if ((curr_x, curr_y - 1), (-1, 0)) in bounds_set:
                curr = ((curr_x, curr_y - 1), (-1, 0))
                bounds_set.remove(curr)
                # print('going up')
                continue
            elif ((curr_x + 1, curr_y - 1), (0, -1)) in bounds_set: 
                # Turn right (right) as a corner
                # ....
                # .AAA
                curr = ((curr_x + 1, curr_y - 1), (0, -1))
                bounds_set.remove(curr)
                # print('turning right (was going up, now going right)')
                sides += 1
                continue
            elif ((curr_x, curr_y), (0, 1)) in bounds_set: 
                # Turn left (left) as a corner
                # AAAA
                # .AAA
                curr = ((curr_x, curr_y), (0, 1))
                bounds_set.remove(curr)
                # print('turning left (was going up, now going left)')
                sides += 1
                continue
        elif (dx, dy) == (0, -1):
            # Crossed this boundary from below i.e. we're on top. Move right.
            # ....
            # AAAA
            if ((curr_x + 1, curr_y), (0, -1)) in bounds_set:
                curr = ((curr_x + 1, curr_y), (0, -1))
                bounds_set.remove(curr)
                # print('going right')
                continue
            elif ((curr_x + 1, curr_y + 1), (1, 0)) in bounds_set: 
                # Turn right (down) as a corner
                # ....
                # AAA.
                curr = ((curr_x + 1, curr_y + 1), (1, 0))
                bounds_set.remove(curr)
                # print('turning right (was going right, now going down)')
                sides += 1
                continue
            elif ((curr_x, curr_y), (-1, 0)) in bounds_set: 
                # Turn left (down) as a corner
                # ...A
                # AAAA
                curr = ((curr_x, curr_y), (-1, 0))
                bounds_set.remove(curr)
                # print('turning left (was going right, now going up)')
                sides += 1
                continue
        elif (dx, dy) == (1, 0):
            # Crossed this boundary from left to right, we're on right. Move down.
            # AA..
            # AA..
            if ((curr_x, curr_y + 1), (1, 0)) in bounds_set:
                curr = ((curr_x, curr_y + 1), (1, 0))
                bounds_set.remove(curr)
                # print('going down')
                continue
            elif ((curr_x - 1, curr_y + 1), (0, 1)) in bounds_set: 
                # Turn right (left) as a corner
                # AA..
                # ....
                curr = ((curr_x - 1, curr_y + 1), (0, 1))
                bounds_set.remove(curr)
                # print('turning right (was going down, now going left)')
                sides += 1
                continue
            elif ((curr_x, curr_y), (0, -1)) in bounds_set: 
                # Turn left (right) as a corner
                # AA..
                # AAAA
                curr = ((curr_x, curr_y), (0, -1))
                bounds_set.remove(curr)
                # print('turning left (was going up, now going left)')
                sides += 1
                continue
        curr = get_leftmost_upper_bound(bounds_set)
        bounds_set.remove(curr)
        sides += 1
        continue
    return sides

pt1 = pt2 = 0
area_coords = {}
for y, line in enumerate(lines):
    for x, chr in enumerate(line):
        if (x, y) not in area_coords:
            a, b = get_region((x, y), {(x, y)}, set(), [l[:] for l in lines])
            pt1_sides = len(b)
            pt2_sides = get_continuous_sides(b)
            print('a', len(a), a)
            print('b', len(b), b)
            area_coords.update({(x, y): chr for (x, y) in a})
            print('Sides', pt2_sides)
            pt1 += len(a) * pt1_sides
            pt2 += len(a) * pt2_sides

print("Part 1:", pt1) # 1434856
print("Part 2:", pt2) # 891106
