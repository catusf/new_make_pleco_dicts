import argparse
import json
from os.path import join

from tools_configs import (
    DATA_DIR,
    DICT_DIR,
    PC_ARROW,
    PC_CLUB_SUIT,
    PC_DIAMOND,
    PC_MIDDLE_DOT,
    PC_RELATED_MARK,
    PC_VIDU_NEW_MARK,
    pleco_make_blue,
    pleco_make_bold,
    pleco_make_dark_gray,
    pleco_make_italic,
    pleco_make_link,
    pleco_make_new_line,
)

MAX_LINES = 500
MAX_LINES = 20000000
REPORT_COUNT = 1000


def main():
    parser = argparse.ArgumentParser(description="Dictionary processing tool")
    parser.add_argument(
        "--dict-size",
        choices=["small", "mid", "big"],
        default="big",
        required=False,
        help="Dictionary size: 'small' for Vietnamese definitions, 'mid' for definitions and examples, 'big' for all definitions including Chinese.",
    )
    parser.add_argument(
        "--num-items",
        type=int,
        default=MAX_LINES,
        required=False,
        help="Dictionary size: 'small' for Vietnamese definitions, 'mid' for definitions and examples, 'big' for all definitions including Chinese.",
    )

    args = parser.parse_args()
    print(args)

    dict_size = args.dict_size
    num_items = args.num_items

    if dict_size in ["big"]:
        print("Open new recommendation file")
        try:
            with open(join(DATA_DIR, "new_reccommendations.json"), "r", encoding="utf-8") as fread:
                new_recomend = json.load(fread)
        except Exception as e:
            print(f"Error: {e}")

    HANVIET_KEY = "Hán Việt"
    with open("data/lacviet_data.json", "r", encoding="utf-8") as data_file:
        dict_data = json.load(data_file)

        count = 0
        count_hanviet = 0

        outfile = join(DICT_DIR, f"TrungViet-{dict_size}.txt")
        # outfile = "dict/lacviet_small.txt"
        with open(outfile, "w", encoding="utf-8") as pleco_import_file:
            for char in dict_data:
                count += 1

                if count >= num_items:
                    break

                if (count + 1) % REPORT_COUNT == 0:
                    print(f"Processing item {count + 1}...")

                # char = item["character"]
                items = dict_data[char]

                related = {}

                for pro in items:
                    pleco = ""
                    pinyin = pro["pinyin"]
                    meta = pro["metadata"] if "metadata" in pro else None

                    pleco += f"{char}\t{pinyin}\t"
                    hanviet = ""

                    if meta and HANVIET_KEY in meta:
                        hanviet = meta[HANVIET_KEY].lower()
                    elif "amhanviet" in pro:
                        hanviet = pro["amhanviet"]

                    if hanviet:
                        count_hanviet += 1
                        pleco += pleco_make_dark_gray(pleco_make_bold(hanviet)) + "\n"

                    # viet_defs = []
                    # chin_defs = []

                    total = len(pro["definitions"])

                    for num, defin in enumerate(pro["definitions"]):
                        if total > 1:
                            pleco += f"{pleco_make_dark_gray(pleco_make_bold(num + 1))} "

                        pleco += f"{defin['vietnamese']}"

                        if dict_size == "big" and defin["chinese"]:
                            pleco += f"{PC_MIDDLE_DOT}{pleco_make_blue(defin['chinese'])}"

                        pleco += "\n"

                        if dict_size in ["mid", "big"] and "examples" in defin:
                            examples = defin["examples"]
                            if examples:
                                pleco += "\n"
                                pleco += f"{pleco_make_dark_gray(PC_DIAMOND + ' ' + PC_VIDU_NEW_MARK)}\n"

                                for example in examples:
                                    pleco += f"{pleco_make_blue(example['example'])}"
                                    pleco += f"{example['translation']}\n"

                if dict_size in ["big"] and char in new_recomend:
                    reccs = new_recomend[char]
                    if reccs:
                        related["related"] = reccs

                        pleco += f"\n{pleco_make_dark_gray(PC_CLUB_SUIT)} {pleco_make_dark_gray(PC_RELATED_MARK)}\n"

                        for rec in reccs:
                            key = list(rec.keys())[0]

                            item = rec[key]

                            # print(f"{key} {item['mean']} {item['pinyin']}")

                            if key in dict_data:
                                pleco += f"{pleco_make_dark_gray(PC_ARROW)} {pleco_make_link(key)} {
                                    pleco_make_italic(item['pinyin'])
                                } {item['mean']}\n"
                            else:
                                pleco += f"{pleco_make_dark_gray(PC_ARROW)} {pleco_make_blue(key)} {
                                    pleco_make_italic(item['pinyin'])
                                } {item['mean']}\n"

                pleco = pleco.replace("\n\n", "\n").replace("<d-tab></d-tab>", "")
                pleco = pleco_make_new_line(pleco)

                pleco_import_file.write(pleco_make_new_line(pleco) + "\n")

            print(f"Amhanviet {count_hanviet} found")
            print(f"Finished writing {count} definitions to {outfile}")


if __name__ == "__main__":
    main()
