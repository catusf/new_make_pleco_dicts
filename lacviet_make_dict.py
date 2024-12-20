import json

from tools_configs import pleco_make_bold, pleco_make_dark_gray, pleco_make_new_line

MAX_LINES = 20000000

HANVIET_KEY = "Hán Việt"
with open("data/lacviet_parsed_fixed_pinyin.json", "r", encoding="utf-8") as file:
    data_array = json.load(file)

    count = 0
    with open("dict/lacviet_small.txt", "w", encoding="utf-8") as pfile:
        for char in data_array:
            count += 1

            if count > MAX_LINES:
                break

            # char = item["character"]
            items = data_array[char]

            for pro in items:
                pleco = ""
                pinyin = pro["pinyin"]
                meta = pro["metadata"]

                pleco += f"{char}\t{pinyin}\t"
                if HANVIET_KEY in meta:
                    pleco += (
                        pleco_make_dark_gray(pleco_make_bold(meta[HANVIET_KEY].lower()))
                        + "\n"
                    )

                viet_defs = []
                chin_defs = []

                for defin in pro["definitions"]:
                    viet_defs.append(defin["vietnamese"])
                    chin_defs.append(defin["chinese"])

                pleco += "\n".join(viet_defs)

                # print(pleco)
                pfile.write(pleco_make_new_line(pleco) + "\n")

        print(f"Finished writing {count} definitions to filefile")
