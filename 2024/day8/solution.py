# input_txt = 'example.txt'
input_txt = 'input.txt'
with open(input_txt) as file:
    lines = [line.strip() for line in file]
