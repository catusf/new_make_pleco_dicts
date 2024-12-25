import copy
import json

import pinyin_jyutping_sentence

with open("data/hanzilearn_dedups.json", "r", encoding="utf-8") as file:
    ccdict = json.load(file)

with open("data/lacviet_parsed.json", "r", encoding="utf-8") as file:
    lacviet = json.load(file)

with open("data/HanziiData.json", "r", encoding="utf-8") as file:
    hanzii = json.load(file)

ccdict_dict = {}
ccdict_dict_pinyins = {}
ccdict_dict_defs = {}

for char in ccdict:
    ccdict_dict_pinyins[char] = []
    ccdict_dict_defs[char] = []
    for item in ccdict[char]:
        ccdict_dict[(char, item["pinyin"])] = item["meaning"]
        ccdict_dict_pinyins[char].append(item["pinyin"])
        ccdict_dict_defs[char].append(item["meaning"])

lacviet_dict = {}
lacviet_dict_pinyins = {}

for char in lacviet:
    lacviet_dict_pinyins[char] = []
    for pro in lacviet[char]:
        lacviet_dict[(char, pro["pinyin"])] = pro["definitions"]

        lacviet_dict_pinyins[char].append(pro["pinyin"])

hanzii_dict = {}

hanzii_dict_pinyins = {}
hanzii_dict_amhanviet = {}

for item in hanzii:
    hanzii_dict[(item["chinese"], item["pinyin"])] = item["definitions"]
    hanzii_dict_pinyins[item["chinese"]] = item["pinyin"]
    hanzii_dict_amhanviet[item["chinese"]] = item["amhanviet"]

print(f"{len(ccdict_dict)=}")

print(f"{len(lacviet_dict)=}")

print(f"{len(hanzii_dict)=}")


def list_not_in_first(first, second, show=False, msg=""):
    first_set = set(first.keys())
    second_set = set(second.keys())

    diff = second_set - first_set

    print(f"{msg + ": " if msg else ""}{len(diff)=}")

    if show:
        " ".join(sorted(diff))

    return diff


list_not_in_first(lacviet_dict, ccdict_dict, msg="In ccdict but not in lacviet")

list_not_in_first(ccdict_dict, lacviet_dict, msg="In lacviet but not in ccdict")

list_not_in_first(lacviet_dict, hanzii_dict, msg="In hanzii but not in lacviet")

list_not_in_first(hanzii_dict, lacviet_dict, msg="In lacviet but not in hanzii")

list_not_in_first(ccdict_dict, hanzii_dict, msg="In hanzii but not in ccdict")

list_not_in_first(hanzii_dict, ccdict_dict, msg="In ccdict but not in hanzii")

common_set = set(ccdict_dict) & set(hanzii_dict) & set(lacviet_dict)

lc_hanzii_set = set(ccdict_dict) | set(hanzii_dict)

lc_hanzii_char_set = set([item[0] for item in lc_hanzii_set])

total_set = set(ccdict_dict) | set(hanzii_dict) | set(lacviet_dict)

print(f"Common {len(common_set)=}")

print(f"HV | HZHZ {len(lc_hanzii_set)=}")

print(f"HV | HZHZ CharChar {len(lc_hanzii_char_set)=}")

print(f"Total {len(total_set)=}")

###

print("===== Keys are chinese only ===")
list_not_in_first(
    lacviet_dict_pinyins, ccdict_dict_pinyins, msg="In ccdict but not in lacviet"
)

list_not_in_first(
    ccdict_dict_pinyins, lacviet_dict_pinyins, msg="In lacviet but not in ccdict"
)

list_not_in_first(
    lacviet_dict_pinyins, hanzii_dict_pinyins, msg="In hanzii but not in lacviet"
)

list_not_in_first(
    hanzii_dict_pinyins, lacviet_dict_pinyins, msg="In lacviet but not in hanzii"
)

list_not_in_first(
    ccdict_dict_pinyins, hanzii_dict_pinyins, msg="In hanzii but not in ccdict"
)

list_not_in_first(
    hanzii_dict_pinyins, ccdict_dict_pinyins, msg="In ccdict but not in hanzii"
)

common_set_pinyins = (
    set(ccdict_dict_pinyins) & set(hanzii_dict_pinyins) & set(lacviet_dict_pinyins)
)

total_set_pinyins = (
    set(ccdict_dict_pinyins) | set(hanzii_dict_pinyins) | set(lacviet_dict_pinyins)
)

print(f"Common {len(common_set_pinyins)=}")

print(f"Total {len(total_set_pinyins)=}")

common_cc_or_hz_pinyins = set(ccdict_dict_pinyins) | set(hanzii_dict_pinyins)

only_in_lv = set(lacviet_dict_pinyins) - common_cc_or_hz_pinyins

print(f"Only in LV {len(only_in_lv)=}")

""" Strategy for correct pinyin:
- Dont trust lv's pinyins
- Find in CCDict first
- If not found, find in Hanzii
- If not found, use pinyin_jyutping_sentence
- If not, mark as errors
"""

exit()

new_lacviet = {}
pinyin_issues = {}

for char in lacviet:
    lacviet_dict_pinyins[char] = []
    new_lacviet[char] = []

    for pro in lacviet[char]:
        new_pro = {
            "definitions": pro["definitions"],
            "oldpinyin": pro["pinyin"].replace("·", " ").replace("…", " "),
            "metadata": pro["metadata"],
            "notes": pro["notes"],
        }

        if char in hanzii_dict_amhanviet:
            new_pro["amhanviet"] = hanzii_dict_amhanviet[char]
            print(new_pro["amhanviet"])

        new_pinyin = ""

        if char in ccdict_dict_pinyins:
            if len(ccdict_dict_pinyins[char]) == 1:
                new_pinyin = ccdict_dict_pinyins[char][0]
                new_pro["newpinyin"] = "<" + new_pinyin
            else:
                new_pinyin = "|".join(ccdict_dict_pinyins[char])
                new_pro["newpinyin"] = new_pinyin
        elif char in hanzii_dict_pinyins:
            new_pinyin = hanzii_dict_pinyins[char]
            new_pro["newpinyin"] = "~" + new_pinyin
        else:
            new_pinyin = (
                pinyin_jyutping_sentence.pinyin(char).replace(" ，", ",").strip()
            )
            new_pro["newpinyin"] = ">" + new_pinyin

        if new_pinyin.replace(" ", "") == new_pro["oldpinyin"].replace(" ", ""):
            new_pro["pinyin"] = new_pro["oldpinyin"]

            del new_pro["newpinyin"]
            del new_pro["oldpinyin"]

        else:
            if "|" in new_pinyin:
                new_case_items = sorted(
                    [item for item in new_pinyin.split("|")], reverse=True
                )  # Sort so that propernames will come later
                new_items = [item.lower() for item in new_case_items]

                if new_pro["oldpinyin"].replace(" ", "").lower() in new_items:
                    new_pro["pinyin"] = new_pro["oldpinyin"]
                    del new_pro["newpinyin"]
                    del new_pro["oldpinyin"]
                else:
                    # Temporarily select the first pinyin for now. Add data below to check later
                    new_pro["pinyin"] = new_items[0]
                    new_pro["cc_def"] = ccdict_dict_defs[char]
                    key = char + "-" + new_pro["oldpinyin"]
                    pinyin_issues[key] = copy.deepcopy(new_pro)

                    for item in pinyin_issues[key]["definitions"]:
                        item.pop("examples", None)
                        item.pop("chinese", None)
            else:
                new_pro["pinyin"] = new_pinyin

        new_lacviet[char].append(new_pro)

with open("data/lacviet_parsed_fixed_pinyin.json", "w", encoding="utf-8") as file:
    json.dump(new_lacviet, file, ensure_ascii=False, indent=3)
    pass

# Write down this items to check later (192 cases)
with open("data/lacviet_parsed_issues.json", "w", encoding="utf-8") as file:
    json.dump(pinyin_issues, file, ensure_ascii=False, indent=3)

    print(f"Needs to fixe {len(pinyin_issues)} issues")
    pass
