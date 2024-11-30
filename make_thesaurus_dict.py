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
    return re.sub(r'[\u4e00-\u9fff]+\|', '', text)


def convert_to_mark_pinyin(text):
    # Define the regex as a constant
    BRACKETS_REGEX = r'(\[[^\]]+\])'
    
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

        return {
            'minutes': minutes,
            'seconds': seconds,
            'milliseconds': milliseconds
        }

    def display_elapsed(self):
        """Display the elapsed time."""
        elapsed = self.elapsed_time()
        print(f"Elapsed time: {elapsed['minutes']}:{elapsed['seconds']}.{elapsed['milliseconds']}s")


def circled_number(n):
    """ Returns circled numbers, maxes out at 35
    """
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

with open('data/hanzilearn_dedups.json', 'r', encoding='utf-8') as f:
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
        contents += f"{pleco_make_bold("DEFINITION")}\n"

    count = len(definitions)
    
    for definition in definitions:
        if dict_size in ["mid", "big"]: # Adds Pinyin
            contents += f"{pleco_make_italic(numbered_to_accented(definition["pinyin"]).replace(" ", ""))} "

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

    if not definitions:
        return ""

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
        tokens = set(line.split(' '))
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
    # Initialize argument parser
    parser = argparse.ArgumentParser(description="Process a thesaurus dictionary and generate output.")
    parser.add_argument("--dict-size", choices=['small', 'mid', 'big'], default="big", required=False,
                        help="Dictionary size: 'small' for Chinese thesaurus only, 'mid' adds Pinyin, 'big' adds definitions for words.")
    parser.add_argument("--num-items", type=int, default=1000000, required=False,
                        help="Maximum number of items to process (default: MAX_ITEMS).")
    args = parser.parse_args()

    # Use the --num-items argument to limit processing
    max_items = args.num_items
    dict_size = args.dict_size

    # Load JSON output
    with open('data/thesaurus_dict.json', 'r', encoding='utf-8') as json_file:
        thesaurus_dict = json.load(json_file)

        pleco_file = "dict/ChineseThesaurus-Pleco.txt"

        pleco_file = pleco_file.replace(".txt", f"-{dict_size}.txt")

        # Generate Pleco dictionary
        with open(pleco_file, 'w', encoding='utf-8') as snd_file:
            count = 0
            print("Generating Pleco dict...")
            for headword in thesaurus_dict:
                antonyms = set(thesaurus_dict[headword]["AntonymSet"]) # Removes dups
                synonyms = set(thesaurus_dict[headword]["SynonymSet"])
                negations = set(thesaurus_dict[headword]["NegationSet"])

                if not (len(antonyms) + len(synonyms) + len(negations)):
                    continue

                count += 1
                if count > max_items:
                    break

                pinyin = pinyinget(headword)
                contents = f'{headword}\t{pinyin}\t'

                contents += get_headword_def_contents(headword, pinyin, dict_size=dict_size, has_marker=False)

                for thesaurus_type, label in [("AntonymSet", "ANTONYM"), ("SynonymSet", "SYNONYM"), ("NegationSet", "NEGATION")]:
                    list_items = sorted(list(dict.fromkeys(thesaurus_dict[headword][thesaurus_type]))) # Removes duplicated but keeps order
                    if list_items:
                        contents += f"{pleco_make_dark_gray(pleco_make_bold(label))}\n"
                        contents += make_linked_items(headword, list_items, dict_size=dict_size)

                contents = contents.replace('\n', PC_NEWLINE)
                snd_file.write(f'{contents}\n')

            print(f"Created {count} items and saved to {pleco_file}")


if __name__ == "__main__":
    timer = Timer()
    timer.start()
    main()
    timer.stop()
    timer.display_elapsed()
