# input_txt = 'advent_of_code/2024/day2/example.txt'
input_txt = 'advent_of_code/2024/day2/input.txt'
with open(input_txt) as file:
    lines = [[int(i) for i in line.strip().split()] for line in file]

# Part 1
def is_report_valid_increasing(report: list[int]) -> bool:
    for i in range(len(report) - 1):
        difference = report[i + 1] - report[i]
        if difference < 1 or difference > 3:
            return False
    return True

def is_report_valid(report: list[int]) -> bool:
    return (
        is_report_valid_increasing(report) or 
        is_report_valid_increasing(report[::-1])
    )

total_safe = 0
for report in lines:
    total_safe += 1 if is_report_valid(report) else 0
print(f'Part 1: {total_safe}')

# Part 2
def get_report_variations(report: list[int]) -> list[list[int]]:
    """Returns report plus variations of report with one level removed."""
    variations = [report]
    for i in range(len(report)):
        variations.append(report[:i] + report[i + 1:])
    return variations

total_safe = 0
for report in lines:
    for v in get_report_variations(report):
        if is_report_valid(v):
            total_safe += 1
            break
print(f'Part 2: {total_safe}')