"""Fixes data of Lacviet Dictionary with the data from Hanzii.net

"""

import copy
import html
import json
import re

import pinyin_jyutping_sentence


def only_word_chars(text):
    return "".join([char for char in text if char.isalpha()])


PATTERN_ZH = r"[一-龥]+"


def is_chinese_char(char):
    pattern = re.compile(PATTERN_ZH)
    return bool(pattern.match(char))


def only_chinesechinese_chars(text):
    return "".join([char for char in text if is_chinese_char(char)])


def mostly_chinese(text, check_len=2, threshold=0.8):
    words = only_word_chars(text)
    chinese = only_chinesechinese_chars(words)

    return len(words) > check_len and len(chinese) / len(words) >= threshold


exceptions = set(
    [
        "Yile",
        "Joe là",
        "Lầu năm góc",
        "Phật; bụt",
        "Internet，mạng xã hội"
    ]
)

appearances = [
    "(tên",
    "(thương hiệu)",
    "(họ)",
    "(thành phố)",
    "(thành ngữ)",
    "(thẻ tín dụng)"
]

def correct_wrong_sentence_case(text):
    if (
        len(text) < 2
        or not text[0].isupper()
        or mostly_chinese(text)
        or text in exceptions
    ):
        return text

    for app in appearances:
        if app in text:
            return text
    
    words = text.split(" ")

    if len(words) < 2:  # One word => proper name
        return text

    word_chars = only_word_chars(text)

    upper_chars = "".join([item for item in word_chars if item.isupper()])

    if len(upper_chars) == 1:  # Only first char is uppercase, highly needs to fix
        new_text = text[0].lower() + text[1:]
        # print(f"Fixed: {text} => {new_text}")

        return new_text

    return text


# s1 = " 指文辞丰富，意气雄健"
# s2 = "xem〖踔〗"
# s3 = "xem 二郎神"

# print(f"{mostly_chinese(s1)}=")
# print(f"{mostly_chinese(s2)}=")
# print(f"{mostly_chinese(s3)}=")

# exit()

def replace_html_entities_in_json(old_file_path, new_file_path):
    try:
        with open(old_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        def replace_entities(obj):
            if isinstance(obj, str):
                return html.unescape(obj)
            elif isinstance(obj, list):
                return [replace_entities(item) for item in obj]
            elif isinstance(obj, dict):
                return {key: replace_entities(value) for key, value in obj.items()}
            return obj
        
        converted_data = replace_entities(data)
        
        with open(new_file_path, 'w', encoding='utf-8') as file:
            json.dump(converted_data, file, ensure_ascii=False, indent=4)
        
        print("HTML entities replaced successfully in JSON file.")
    except Exception as e:
        print(f"Error: {e}")

with open("data/hanzilearn_dedups.json", "r", encoding="utf-8") as file:
    ccdict = json.load(file)

replace_html_entities_in_json("data/lacviet_parsed.json", "data/lacviet_fixed.json")

with open("data/lacviet_fixed.json", "r", encoding="utf-8") as file:
    lacviet = json.load(file)

with open("data/HanziiData.json", "r", encoding="utf-8") as file:
    hanzii = json.load(file)

ccdict_dict = {}
ccdict_dict_pinyins = {}
ccdict_dict_defs = {}

# pprint(lacviet["一"])

for char in ccdict:
    ccdict_dict_pinyins[char] = []
    ccdict_dict_defs[char] = []
    for item in ccdict[char]:
        ccdict_dict[(char, item["pinyin"])] = item["meaning"]
        ccdict_dict_pinyins[char].append(item["pinyin"])
        ccdict_dict_defs[char].append(item["meaning"])

hanzii_dict = {}

hanzii_new = {}
hanzii_dict_pinyins = {}
hanzii_dict_amhanviet = {}

added_to_lacviet = 0
for item in hanzii:
    char = item["chinese"]
    pinyin = item["pinyin"]
    definitions = item["definitions"]
    amhanviet = item["amhanviet"]

    hanzii_dict[(char, pinyin)] = definitions
    hanzii_dict_pinyins[char] = pinyin
    hanzii_dict_amhanviet[char] = amhanviet

    # print("Hanzii item")
    # pprint(item)

    hanzii_new[char] = []
    # hanzii_new[char]["pinyin"] = pinyin

    new_definitions = []

    for defin in definitions:
        vietnamese = correct_wrong_sentence_case(defin["vietnamese"])
        chinese = defin["chinese"] if "chinese" in defin else ""

        # if "<d-tab></d-tab>" in chinese:
        #     print(chinese)

        if mostly_chinese(vietnamese):
            # print(f"Skipped mostly chinese def: {vietnamese}")
            continue

        new_item = {
            "chinese": chinese,
            "vietnamese": vietnamese,
        }

        if "example" in defin:
            example = {
                "example": defin["example"]["example_chinese"],
                "translation": defin["example"]["example_meaning"],
            }
            new_item["examples"] = [example]

        new_definitions.append(new_item)

    hanzii_new[char].append(
        {
            "definitions": new_definitions,
            "pinyin": pinyin,
            "amhanviet": amhanviet,
        }
    )

# print("=========")
# print("Lacviet")
# pprint(lacviet["二"])
# print("Hanzii new")
# pprint(hanzii_new["二"])

print(f"{len(hanzii)=}")
print(f"{len(hanzii_new)=}")
# pass
# added_to_lacviet += 1

#     new_definitions = []

#     for defin in definitions:
#         new_definitions.append("")

#     lacviet[char]["definitions"].extend(new_definitions)

print(f"{added_to_lacviet=}")
lacviet_dict = {}
lacviet_dict_pinyins = {}

for char in lacviet:
    lacviet_dict_pinyins[char] = []
    for pro in lacviet[char]:
        lacviet_dict[(char, pro["pinyin"])] = pro["definitions"]

        lacviet_dict_pinyins[char].append(pro["pinyin"])


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

lv_hanzii_set = set(ccdict_dict) | set(hanzii_dict)

lv_hanzii_char_set = set([item["chinese"] for item in hanzii]) | set(lacviet.keys())

total_set = set(ccdict_dict) | set(hanzii_dict) | set(lacviet_dict)


print(f"Common {len(common_set)=}")

print(f"HV | HZ {len(lv_hanzii_set)=}")

print(f"HV | HZ Char {len(lv_hanzii_char_set)=}")

print(f"Total {len(total_set)=}")

cc_but_others = set(ccdict_dict) - lv_hanzii_set
print(f"In CCDICT but not other -  {len(cc_but_others)=}")

lv_hanzii_but_others = lv_hanzii_set -set(ccdict_dict) 
print(f"In lvhanzi but not ccdict -  {len(lv_hanzii_but_others)=}")

with open("data/cc_but_others.json", "w", encoding="utf-8") as file:
    json.dump(sorted(cc_but_others), file, ensure_ascii=False, indent=4)

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

# exit()

new_lacviet = {}
pinyin_issues = {}

def remove_leading_number(text):
    pattern1 = r"^[0-9a-z]\. ?"
    pattern2 = r"^[0-9a-z] "

    # Replace the matching substring
    new_text = re.sub(pattern1, "", text.strip())
    new_text = re.sub(pattern2, "", new_text).strip()
    
    return new_text

for char in lv_hanzii_char_set:

    if char in lacviet:  # If in Lacviet priotize it. Fixes issues if any
        lacviet_dict_pinyins[char] = []
        new_lacviet[char] = []

        for pro in lacviet[char]:

            for defin in pro["definitions"]:
                viet = defin["vietnamese"]

                # Remove leading number like "1.", "1. ", "a.", "a " etc.
                defin["vietnamese"] = remove_leading_number(viet)

                pass
            new_pro = {
                "definitions": [item for item in pro["definitions"] if item["vietnamese"]],
                
                "oldpinyin": pro["pinyin"].replace("·", " ").replace("…", " "),
                "metadata": pro["metadata"],
                "notes": pro["notes"],
            }

            if char in hanzii_dict_amhanviet:
                new_pro["amhanviet"] = hanzii_dict_amhanviet[char]
                # print(new_pro["amhanviet"])

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
    elif char in hanzii_new:  # Use Hanzii
        new_lacviet[char] = copy.deepcopy(hanzii_new[char])
    else:
        # raise KeyError(char)
        print(f"Key not found: {char}")

with open("data/lacviet_data.json", "w", encoding="utf-8") as file:
    print(f"Fixed count: {len(new_lacviet)}")
    json.dump(new_lacviet, file, ensure_ascii=False, indent=2)
    pass

# Write down this items to check later (192 cases)
with open("data/lacviet_parsed_issues.json", "w", encoding="utf-8") as file:
    json.dump(pinyin_issues, file, ensure_ascii=False, indent=3)

    print(f"Needs to fix {len(pinyin_issues)} issues")
    pass
