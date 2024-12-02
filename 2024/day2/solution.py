# input_txt = 'advent_of_code/2024/day2/example.txt'
input_txt = 'advent_of_code/2024/day2/input.txt'
with open(input_txt) as file:
    lines = [[int(i) for i in line.strip().split()] for line in file]

# Part 1
def is_increasing_report(report: list[int]) -> bool:
    """Returns true if report is valid and increasing"""
    for i in range(len(report) - 1):
        difference = report[i + 1] - report[i]
        if difference < 1 or difference > 3:
            return False
    return True

def is_decreasing_report(report: list[int]) -> bool:
    """Returns true if report is valid and decreasing"""
    for i in range(len(report) - 1):
        difference = report[i] - report[i + 1]
        if difference < 1 or difference > 3:
            return False
    return True

def evaluate_report(report: list[int]) -> bool:
    """Returns true if report is valid."""
    assert len(report) > 1, "Report length must be greater than 1."
    return is_increasing_report(report) or is_decreasing_report(report)

total_safe = 0
for report in lines:
    total_safe += 1 if evaluate_report(report) else 0
print(total_safe)

