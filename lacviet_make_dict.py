import json

from tools_configs import pleco_make_bold, pleco_make_dark_gray, pleco_make_new_line

MAX_LINES = 20000000

HANVIET_KEY = "Hán Việt"
with open("lv/parsed.json", "r", encoding="utf-8") as file:
    data_array = json.load(file)

    with open("lv/lacviet_small.txt", "w", encoding="utf-8") as pfile:
        for item in data_array[:MAX_LINES]:
            char = item["character"]

            for pro in item["pronunciations"]:
                pleco = ""
                pinyin = pro["pronunciation"]
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
            pfile.write(pleco_make_new_line(pleco, make_pleco=True) + "\n")

        print(f"Finished writing {len(data_array)} definitions to filefile")
