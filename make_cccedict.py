import csv
from dragonmapper.transcriptions import numbered_to_accented
from tools_configs import *
# def replace_num_pinyin(match_obj):

def read_csv_to_tuples(file_path):
    """
    Reads a CSV file and returns its contents as a list of tuples.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        list of tuple: Each tuple represents a row in the CSV file.
    """
    data = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter=',')  # Tab-separated values
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            data.append(row)  # Convert row to a tuple and add to the list
    return data

# Example usage
file_path = "data/words.csv"  # Replace with the actual path to your file
data_as_tuples = read_csv_to_tuples(file_path)

# Print the result
PATTERN_PY = r"\[(.+)\]"

MAX_ITEMS = 10000000
# MAX_ITEMS = 100

with open("dict/opencc_pleco.txt", "w", encoding="utf-8") as fwrite:
    check_dups = set()
    for num, row in enumerate(data_as_tuples):
        if num >= MAX_ITEMS:
            break
        item = row[1]
        pinyin = numbered_to_accented(row[2][1:-1]).replace(" ", "")

        key = f"{item}-{pinyin}"

        if key in check_dups:
            print(f"Duplicate entry: {key}")
        else:
            check_dups.add(key)

        meanings = row[3][:-1].split("/")

        meaning_text = [remove_chinese_with_pipe(replace_num_pinyin_fs(item)) for item in meanings]
        if len(meanings) > 1:
            pleco_text = f"{item}\t{pinyin}\t{"\n".join([f"{pleco_make_bold(num)} {item}" for num, item in enumerate(meaning_text, start=1)])}"
        else:
            pleco_text = f"{item}\t{pinyin}\t{"\n".join([f"{item}" for _, item in enumerate(meaning_text, start=1)])}"
            
        fwrite.write(f"{pleco_make_new_line(pleco_text, make_pleco=True)}\n")

        pass

print(f"Writing {num} items")

