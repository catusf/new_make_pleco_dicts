import argparse
import datetime
import json
import signal
import sys
from os.path import join

import readchar

from tools_configs import (
    DATA_DIR,
    DICT_DIR,
    PC_ARROW,
    PC_CLUB_SUIT,
    PC_DIAMOND,
    PC_RELATED_MARK,
    PC_VIDU_NEW_MARK,
    load_frequent_words,
    number_in_cirle,
    pleco_make_blue,
    pleco_make_bold,
    pleco_make_dark_gray,
    pleco_make_italic,
    pleco_make_link,
    pleco_make_new_line,
)


def keyboard_handler(signum, frame):
    msg = "Ctrl-c was pressed. Do you really want to exit? y/n "
    print(msg, end="", flush=True)
    res = readchar.readchar()
    if res == "y":
        sys.exit(1)
    else:
        print("", end="\r", flush=True)
        print(" " * len(msg), end="", flush=True)  # clear the printed line
        print("    ", end="\r", flush=True)


MAKE_PLECO = False


def main():
    parser = argparse.ArgumentParser(description="Dictionary processing tool")
    parser.add_argument(
        "--dict-size",
        choices=["small", "mid", "big"],
        default="small",
        required=False,
        help="Dictionary size: 'small' for Vietnamese definitions, 'mid' for definitions and examples, 'big' for all definitions including Chinese.",
    )
    parser.add_argument(
        "--num-items",
        type=int,
        default=100000000,
        required=False,
        help="Dictionary size: 'small' for Vietnamese definitions, 'mid' for definitions and examples, 'big' for all definitions including Chinese.",
    )

    args = parser.parse_args()
    print(args)

    dict_size = args.dict_size
    num_items = args.num_items
    MAKE_PLECO = True

    now_datetime = datetime.datetime.now()

    signal.signal(signal.SIGINT, keyboard_handler)

    if dict_size in ["big"]:
        print("Open new recommendation file")
        with open(
            join(DATA_DIR, "new_reccommendations.json"), "r", encoding="utf-8"
        ) as fread:
            new_recomend = json.load(fread)

    print("Open dictionary data file")
    with open(join(DATA_DIR, "dict_data.json"), "r", encoding="utf-8") as fread:
        dict_data = json.load(fread)

    this_dic_words_set = set(load_frequent_words("dic_words_set.txt"))
    current_word_list = this_dic_words_set

    # MAX_ITEMS = 1000000
    # MAX_ITEMS = 100
    REPORT_COUNT = 1000

    # clean_dict_data = {}
    dictionary_data = []
    related_data = []

    output_file = join(DICT_DIR, f"TrungViet-{dict_size}.txt")
    PC_DICT_NAME = f"//TrungViet Beta {dict_size} Dict"
    with open(output_file, "w", encoding="utf-8") as pleco_import_file:
        if MAKE_PLECO:
            pleco_import_file.write(f"{PC_DICT_NAME}\n")

        for num, headword in enumerate(sorted(dict_data)):
            dict_item = dict_data[headword]

            headword_data = {
                "chinese": headword,
                "pinyin": "",
                "amhanviet": "",
                "definitions": [],
            }

            headword_related = {}

            if num >= num_items:
                break

            if (num + 1) % REPORT_COUNT == 0:
                print(f"Processing item {num+1}...")

            # print(f"Processing {num+1}: {headword}...")
            pleco_string = ""

            if headword not in current_word_list:
                print(f"Item not in current_word_list: {headword}")
                # continue

            pleco_string += f"{dict_item['chinese']}\t"

            if MAKE_PLECO:
                pleco_string += f"{dict_item['pinyin']}\t"
                headword_data["pinyin"] = dict_item["pinyin"]

            headword_related["chinese"] = headword_data["chinese"]
            headword_related["pinyin"] = headword_data["pinyin"]

            if dict_item["amhanviet"]:
                pleco_string += (
                    f"{pleco_make_dark_gray(pleco_make_bold(dict_item['amhanviet']))}\n"
                )

                headword_data["amhanviet"] = dict_item["amhanviet"]

                # pleco_string += f"{pleco_make_dark_gray(pleco_make_bold(PC_HANVIET_MARK))} {pleco_make_italic(dict_item['amhanviet'])}\n"

            # if dict_size in ['mid', 'big'] and dict_item['amhanviet']:
            # if dict_size == 'big':
            total = 0

            for wordkind in dict_item["wordkinds"]["list_items"]:
                total += len(dict_item["wordkinds"]["list_items"][wordkind])

            num = 1

            for wordkind in dict_item["wordkinds"]["list_items"]:
                # pleco_string += f"{pleco_make_dark_gray(pleco_make_bold(wordkind))}\n"

                items = dict_item["wordkinds"]["list_items"][wordkind]
                for item in items:
                    definition_data = {}

                    if total > 1:
                        number = number_in_cirle(num)
                        num += 1
                        pleco_string += (
                            f"{pleco_make_dark_gray(pleco_make_bold(number))} "
                        )

                    if dict_size == "big":
                        pleco_string += (
                            f"{pleco_make_blue(item['definition']['chinese'])} "
                        )
                        definition_data["chinese"] = item["definition"]["chinese"]

                    pleco_string += f"{item['definition']['vietnamese']}\n"

                    definition_data["vietnamese"] = item["definition"]["vietnamese"]

                    if dict_size in ["mid", "big"]:
                        example = item["definition"]["example"]

                        if example:
                            pleco_string += f"{pleco_make_dark_gray(PC_DIAMOND + " " + PC_VIDU_NEW_MARK)}\n "
                            pleco_string += (
                                f"{pleco_make_blue(example['example_chinese'])} "
                            )
                            pleco_string += (
                                f"{pleco_make_italic(example['example_pron'])} "
                            )
                            pleco_string += f"{example['example_meaning']}\n"

                            definition_data["example"] = example

                    headword_data["definitions"].append(definition_data)
                
            if dict_size in ["big"]:
                reccs = new_recomend[headword]
                if reccs:

                    headword_related["related"] = reccs

                    pleco_string += f"\n{pleco_make_dark_gray(
                        PC_CLUB_SUIT)} {pleco_make_dark_gray(PC_RELATED_MARK)}\n"

                    for rec in reccs:
                        key = list(rec.keys())[0]

                        item = rec[key]

                        # print(f"{key} {item['mean']} {item['pinyin']}")

                        if key in dict_data:
                            pleco_string += f"{pleco_make_dark_gray(PC_ARROW)} {pleco_make_link(key)} {
                                pleco_make_italic(item['pinyin'])} {item['mean']}\n"
                        else:
                            pleco_string += f"{pleco_make_dark_gray(PC_ARROW)} {pleco_make_blue(key)} {
                                pleco_make_italic(item['pinyin'])} {item['mean']}\n"


            pleco_string = pleco_string.replace("\n\n", "\n")
            pleco_string = pleco_make_new_line(pleco_string)
            pleco_import_file.write(f"{pleco_string}\n")

            dictionary_data.append(headword_data)
            
            if "related" in headword_related: # Really have related words
                related_data.append(headword_related)

    with open("data/HanziiData.json", "w", encoding="utf-8") as file:
        json.dump(dictionary_data, file, ensure_ascii=False, indent=2)

    with open("data/HanziiData-related.json", "w", encoding="utf-8") as file:
        json.dump(related_data, file, ensure_ascii=False, indent=2)

    print(f"Written output to {output_file}")
    later_datetime = datetime.datetime.now()
    print(f"Time elapsed {later_datetime-now_datetime}")


if __name__ == "__main__":
    main()
