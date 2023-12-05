# input_txt = 'advent_of_code/2022/day6/example.txt'
input_txt = 'advent_of_code/2022/day6/input.txt'
with open(input_txt) as file:
    signal = file.readline().strip()

for i, char in enumerate(signal):
    if i < 3:
        continue
    if len(set(signal[i-4:i])) == 4:
        break

print("Pt 1:", i) # 1896

for i, char in enumerate(signal):
    if i < 13:
        continue
    if len(set(signal[i-14:i])) == 14:
        break
    
print("Pt 2:", i) # 3452