import csv
import json
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
file_path = "data/hanlearn-words.csv"  # Replace with the actual path to your file
data_as_tuples = read_csv_to_tuples(file_path)

# Print the result
PATTERN_PY = r"\[(.+)\]"

MAX_ITEMS = 10000000
# MAX_ITEMS = 100

from collections import defaultdict

# Creating a defaultdict with default type list
clean_dict = defaultdict(dict)

dups = 0
check_dups = set()
for num, row in enumerate(data_as_tuples):
    if num >= MAX_ITEMS:
        break
    headword = row[1]
    pinyin = numbered_to_accented(row[2][1:-1]).replace(" ", "")

    nocase_key = f"{headword}-{pinyin.lower()}"

    if nocase_key in check_dups:
        print(f"Duplicate entry: {nocase_key}")
        dups+=1
    else:
        check_dups.add(nocase_key)

    meanings = remove_chinese_with_pipe(replace_num_pinyin_fs(row[3][:-1])).split("/")

    if pinyin in clean_dict[nocase_key]:
        for meaning in meanings:
            if meaning not in clean_dict[nocase_key][pinyin]:
                clean_dict[nocase_key][pinyin].append(meaning)
    else:
        clean_dict[nocase_key][pinyin] = meanings
    pass

hanzilearn_dict = defaultdict(list)

with open("data/hanzilearn_dedups.json", "w", encoding="utf-8") as dictfile:
    for word_pinyin in clean_dict:
        word, _ = word_pinyin.split("-")

        keys = sorted(list(clean_dict[word_pinyin].keys()), reverse=True) # sorts so that the lower case pinyin will come first
        key0 = keys[0]

        meanings = clean_dict[word_pinyin][key0]

        if len(keys) > 1: # Merge all meanings from different pinyins
            for key in keys[1:]:
                meanings.extend(clean_dict[word_pinyin][key])
            pass
        
        hanzilearn_dict[word].append({"pinyin": key0, "meaning": meanings})

    json.dump(hanzilearn_dict, dictfile, ensure_ascii=False, indent=4)

print(f"Writing {len(clean_dict)} items, after cleaning {dups} dups")

