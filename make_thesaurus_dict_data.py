import argparse
from collections import defaultdict
import re
import time
import io
import json

from tools_configs import ChineseDictionary
from dragonmapper.transcriptions import numbered_to_accented
from pinyin_jyutping_sentence import pinyin as pinyinget

# from chin_dict.chindict import ChinDict


# Constants
BIG_ITEMS = 50  # For debug purposes

PC_NEWLINE = chr(0xEAB1)
PC_RIGHT_TRIANGLE = "»"  # ▸
PC_SEPARATOR_1 = " "
PC_SEPARATOR_2 = "、"
PC_MIDDLE_DOT = "·"


def remove_chinese_with_pipe(text):
    """
    Remove the Traditional Chinese characters before the '|' and the '|' itself in the input string.

    Args:
        text (str): The input text to be cleaned.

    Returns:
        str: The cleaned text.
    """
    return re.sub(r"[\u4e00-\u9fff]+\|", "", text)


def convert_to_mark_pinyin(text):
    # Define the regex as a constant
    BRACKETS_REGEX = r"(\[[^\]]+\])"

    # Function to convert matched text to uppercase
    def replace_with_uppercase(match):
        # return match.group(1)
        return f" {numbered_to_accented(match.group(1))[1:-1]}"

    return re.sub(BRACKETS_REGEX, replace_with_uppercase, text)


class Timer:
    """
    A Timer class to measure elapsed time with start, stop, and display functionalities.
    """

    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        """Start the timer."""
        self.start_time = time.time()
        self.end_time = None
        print("Timer started.")

    def stop(self):
        """Stop the timer."""
        if self.start_time is None:
            raise ValueError("Timer has not been started.")
        self.end_time = time.time()
        print("Timer stopped.")

    def elapsed_time(self):
        """Calculate and return the elapsed time in minutes, seconds, and milliseconds."""
        if self.start_time is None:
            raise ValueError("Timer has not been started.")
        if self.end_time is None:
            raise ValueError("Timer has not been stopped.")

        elapsed_time = self.end_time - self.start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        milliseconds = int((elapsed_time * 1000) % 1000)

        return {"minutes": minutes, "seconds": seconds, "milliseconds": milliseconds}

    def display_elapsed(self):
        """Display the elapsed time."""
        elapsed = self.elapsed_time()
        print(f"Elapsed time: {elapsed['minutes']}:{elapsed['seconds']}.{elapsed['milliseconds']}s")


def circled_number(n):
    """Returns circled numbers, maxes out at 35"""
    if 1 <= n <= 20:
        return chr(9311 + n)  # Unicode offset for circled digits ① to ⑳
    elif 21 <= n <= 35:  # Circled numbers 21–35
        return chr(12881 + n - 20)  # Unicode offset for Ⓐ-Ⓙ and beyond
    else:
        return str(n)  # Fallback to normal numbers


def pleco_make_dark_gray(text):  # Light Slate Gray
    return f"{text}"


def pleco_make_italic(text):
    return f"{chr(0xEAB4)}{text}{chr(0xEAB5)}"


def pleco_make_bold(text):
    return f"{chr(0xEAB2)}{text}{chr(0xEAB3)}"


def pleco_make_link(text):
    return f"{chr(0xEAB8)}{text}{chr(0xEABB)}"


DEF_SEPERATOR = "/"

# dictionary = ChineseDictionary()

with open("data/hanzilearn_dedups.json", "r", encoding="utf-8") as f:
    dictionary = json.load(f)


def get_def_contents(item, dict_size, has_marker=False):
    """
    Generate a string containing the definitions and Pinyin (if applicable) for a given word.

    Parameters:
    item (str): The headword for which to retrieve definitions and Pinyin.
    dict_size (str): The size of the dictionary. It can be one of the following: "small", "mid", "big".
    has_marker (bool): A flag indicating whether to include a marker for the definition section.
                        Defaults to False.

    Returns:
    str: A string containing the definitions and Pinyin (if applicable) for the given word.
         If the dictionary size is "mid" or "big", the Pinyin is included.
         If the dictionary size is "small", only the definitions are included.
         If the word is not found in the dictionary, the function returns an empty string.
    """

    definitions = []

    if item in dictionary:
        definitions = dictionary[item]

    if not definitions:
        return f"{pleco_make_italic(pinyinget(item))}\n" if dict_size in ["mid", "big"] else "\n"

    contents = ""
    if has_marker:
        contents += f"{pleco_make_bold('DEFINITION')}\n"

    count = len(definitions)

    for definition in definitions:
        if dict_size in ["mid", "big"]:  # Adds Pinyin
            contents += f"{pleco_make_italic(numbered_to_accented(definition['pinyin']).replace(' ', ''))} "

        contents += f"{'; '.join([remove_chinese_with_pipe(convert_to_mark_pinyin(item.strip())) for item in definition['meaning']])}{DEF_SEPERATOR}"

    if contents[-1] == DEF_SEPERATOR:
        contents = contents[:-1]

    contents += "\n"

    return contents


def get_headword_def_contents(item, pinyin, dict_size, has_marker=False):
    """
    Generate a string containing the definitions and Pinyin (if applicable) for a given HEADWORD.

    Parameters:
    item (str): The headword for which to retrieve definitions and Pinyin.
    dict_size (str): The size of the dictionary. It can be one of the following: "small", "mid", "big".
    has_marker (bool): A flag indicating whether to include a marker for the definition section.
                        Defaults to False.

    Returns:
    str: A string containing the definitions and Pinyin (if applicable) for the given word.
         If the dictionary size is "mid" or "big", the Pinyin is included.
         If the dictionary size is "small", only the definitions are included.
         If the word is not found in the dictionary, the function returns an empty string.
    """

    definitions = []

    if item in dictionary:
        definitions = dictionary[item]

    # if not definitions:
    #     return f"{pleco_make_italic(pinyinget(item))}\n" if dict_size in ["mid", "big"] else "\n"

    contents = ""

    count = len(definitions)

    for definition in definitions:
        contents += f"{'; '.join([remove_chinese_with_pipe(convert_to_mark_pinyin(item.strip())) for item in definition['meaning']])}{DEF_SEPERATOR}"

    if contents[-1] == DEF_SEPERATOR:
        contents = contents[:-1]

    contents += "\n"

    return contents


def make_linked_items(cur_item, lines, dict_size):
    """
    Generate a formatted string of linked items with definitions or Pinyin based on the dictionary size.

    Parameters:
    cur_item (str): The current headword to exclude from the linked items.
    lines (list of str): A list of strings, each representing a line of related words.
    dict_size (str): The size of the dictionary, which determines the level of detail in the output.
                     It can be "small", "mid", or "big".

    Returns:
    str: A formatted string containing linked items with definitions or Pinyin, separated by appropriate separators.
    """
    contents = ""

    for index, line in enumerate(lines, start=1):
        tokens = set(line.split(" "))
        tokens.discard(cur_item)  # Don't repeat the headword
        tokens = sorted(list(tokens))

        words = []

        for token in tokens:
            if dict_size in ["big"]:
                word = pleco_make_link(token) + " " + get_def_contents(token, dict_size=dict_size, has_marker=False)
            else:
                word = pleco_make_link(token) + (" " + pinyinget(token) if dict_size in ["mid", "big"] else "")

            words.append(word)

        sep = PC_SEPARATOR_1 if dict_size in ["mid", "big"] else PC_SEPARATOR_2

        if len(words) > 1:
            contents += f"{circled_number(index)} {sep.join(words)}\n"
        else:
            contents += f"{sep.join(words)}\n"

    return contents


def main():
    """
    Generates a json data file for thesaurus making.

    """

    parser = argparse.ArgumentParser(description="Process a thesaurus dictionary and generate output.")
    parser.add_argument(
        "--num-items",
        type=int,
        default=1000000,
        required=False,
        help="Maximum number of items to process (default: MAX_ITEMS).",
    )
    args = parser.parse_args()

    # Use the --num-items argument to limit processing
    max_items = args.num_items

    # Initialize the synonym dictionary with defaultdict
    thesaurus_dict = defaultdict(
        lambda: {"SynonymSet": [], "RelatedSet": [], "IndependentSet": [], "AntonymSet": [], "NegationSet": []}
    )

    # Process thesaurus files
    with open("data/dict_synonym.txt", "r", encoding="utf-8") as file:
        count = 0
        print("Reading dict_synonym.txt...")
        for line in file:
            line = line.strip()
            if not line:
                continue
            if count > max_items:
                break
            count += 1
            try:
                category, words = line.split(" ", 1)
            except ValueError:
                print(f"Invalid format line: {line}")
                continue

            type_char = category[-1]
            thesaurus_type = {"=": "SynonymSet", "#": "RelatedSet", "@": "IndependentSet"}.get(type_char, None)
            if not thesaurus_type:
                print(f"Incorrect line: {line}")
                continue

            word_list = words.split()
            for word in word_list:
                thesaurus_dict[word][thesaurus_type].append(words)

    with open("data/dict_antonym.txt", "r", encoding="utf-8") as file:
        count = 0
        print("Reading dict_antonym.txt...")
        for line in file:
            line = line.strip()
            if not line:
                continue
            count += 1
            if count > max_items:
                break
            try:
                word1, word2 = line.split("-", 1)
            except ValueError:
                print(f"Invalid format line: {line}")
                continue

            if (
                "," in word2
            ):  # ignores the case "没有反义词,可以参考孤独的反义词" = has no antonym. You can refer to the antonym of loneliness
                continue

            thesaurus_dict[word1]["AntonymSet"].append(word2)
            thesaurus_dict[word2]["AntonymSet"].append(word1)

    ignore_negations = {"不", "没"}
    with open("data/dict_negative.txt", "r", encoding="utf-8") as file:
        count = 0
        print("Reading dict_negative.txt...")
        negations = []
        for line in file:
            line = line.strip()
            if not line:
                continue
            count += 1
            if count > max_items:
                break
            try:
                word, _ = line.split("\t", 1)
            except ValueError:
                print(f"Invalid format line: {line}")
                continue
            negations.append(word)

        for word in thesaurus_dict:
            if word in ignore_negations:
                continue
            for negation in negations:
                if word != negation and word in negation:
                    thesaurus_dict[word]["NegationSet"].append(negation)

    # Write JSON output
    with open("data/thesaurus_dict.json", "w", encoding="utf-8") as json_file:
        json.dump(thesaurus_dict, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    timer = Timer()
    timer.start()
    main()
    timer.stop()
    timer.display_elapsed()
