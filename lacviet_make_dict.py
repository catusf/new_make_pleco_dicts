import json

from tools_configs import pleco_make_bold, pleco_make_dark_gray, pleco_make_new_line

MAX_LINES = 500
MAX_LINES = 20000000

HANVIET_KEY = "Hán Việt"
with open("data/lacviet_parsed_fixed_pinyin.json", "r", encoding="utf-8") as file:
    data_array = json.load(file)

    count = 0
    count_hanviet = 0

    outfile = "dict/lacviet_small.txt"
    with open(outfile, "w", encoding="utf-8") as pfile:
        for char in data_array:
            count += 1

            if count > MAX_LINES:
                break

            # char = item["character"]
            items = data_array[char]

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

                viet_defs = []
                chin_defs = []

                for defin in pro["definitions"]:
                    viet_defs.append(defin["vietnamese"])
                    chin_defs.append(defin["chinese"])

                if len(viet_defs) == 1:
                    pleco += viet_defs[0]
                elif len(viet_defs) > 1:
                    pleco += "\n".join(
                        [
                            f"{pleco_make_bold(num)} {text}"
                            for num, text in enumerate(viet_defs, start=1)
                        ]
                    )

                # print(pleco)
                pfile.write(pleco_make_new_line(pleco) + "\n")

        print(f"Amhanviet {count_hanviet} found")
        print(f"Finished writing {count} definitions to {outfile}")
