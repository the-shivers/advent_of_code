import os
import sys

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def create_new_day_folder(advent_root, year, day):
    year_folder = os.path.join(advent_root, year)
    day_folder = os.path.join(year_folder, f'day{day}')

    create_folder_if_not_exists(year_folder)
    create_folder_if_not_exists(day_folder)

    solution_file_path = os.path.join(day_folder, 'solution.py')
    with open(solution_file_path, 'w') as file:
        file.write("# input_txt = 'advent_of_code/{}/day{}/example.txt'\n".format(year, day))
        file.write("input_txt = 'advent_of_code/{}/day{}/input.txt'\n".format(year, day))
        file.write("with open(input_txt) as file:\n")
        file.write("    lines = [line.strip() for line in file]\n")

    open(os.path.join(day_folder, 'input.txt'), 'a').close()
    open(os.path.join(day_folder, 'example.txt'), 'a').close()

    print(f"Created new folder and files for year {year}, day {day}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python create_day_folder.py <year> <day>")
        sys.exit(1)

    year, day = sys.argv[1], sys.argv[2]
    advent_root = os.path.expanduser('~/advent_of_code')
    create_new_day_folder(advent_root, year, day)
