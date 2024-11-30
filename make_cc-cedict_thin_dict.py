# Create a "thin" version of the CC CE Dictionary, that saves spaces, 
# compared with the default version in Pleco's dictionary.
import csv
import enum
from dragonmapper.transcriptions import numbered_to_accented
from tools_configs import *
# def replace_num_pinyin(match_obj):


with open('data/hanzilearn_dedups.json', 'r', encoding='utf-8') as f:
    dictionary = json.load(f)


# Print the result
PATTERN_PY = r"\[(.+)\]"

MAX_ITEMS = 10000000
# MAX_ITEMS = 100

with open("dict/opencc_pleco.txt", "w", encoding="utf-8") as fwrite:
    check_dups = set()
    num = 0
    for key in dictionary:
        if num >= MAX_ITEMS:
            break
        num += 1

        for item in dictionary[key]:
            pinyin = item["pinyin"]
            meanings = item["meaning"]

            pleco_text = f"{key}\t{pinyin}\t"

            if len(meanings) > 1:
                pleco_text += f"{"\n".join([f"{pleco_make_bold(num)} {item}" for num, item in enumerate(meanings, start=1)])}"
            else:
                pleco_text += f"{"\n".join([f"{item}" for _, item in enumerate(meanings, start=1)])}"
                
            fwrite.write(f"{pleco_make_new_line(pleco_text, make_pleco=True)}\n")

        pass

print(f"Writing {num} items")

