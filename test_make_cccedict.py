import csv
from dragonmapper.transcriptions import numbered_to_accented
# from tools_configs import *
# def replace_num_pinyin(match_obj):

def read_csv_to_tuples(file_path):
    """
    Reads a CSV file and returns its contents as a list of tuples.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        list of tuple: Each tuple represents a row in the CSV file.
    """
    data = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter=',')  # Tab-separated values
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            data.append(row)  # Convert row to a tuple and add to the list
    return data

# Example usage
file_path = "data/words.csv"  # Replace with the actual path to your file
data_as_tuples = read_csv_to_tuples(file_path)

# Print the result
PATTERN_PY = r"\[(.+)\]"

MAX_ITEMS = 1000000
# MAX_ITEMS = 5

from collections import Counter

class ItemCounter:
    def __init__(self):
        self.counter = Counter()

    def add_items(self, items):
        """Add items to the counter."""
        self.counter.update(items)

    def get_count(self, item):
        """Get the count of a specific item."""
        return self.counter.get(item, 0)

    def get_all_counts(self):
        """Get all items with their counts."""
        return dict(self.counter)

    def get_top_n(self, n=10):
        """Get the top `n` items by count."""
        return self.counter.most_common(n)

    def reset(self):
        """Reset the counter."""
        self.counter.clear()

items = []

with open("dict/opencc_pleco.txt", "w", encoding="utf-8") as fwrite:
    for num, row in enumerate(data_as_tuples):
        if num >= MAX_ITEMS:
            break

        item = row[1]
        items.append(f"{row[0]}-{row[1][1:-1]}")
        continue
        
        # definitions = dictionary.lookup(item)

        pinyin = numbered_to_accented(row[2][1:-1])
        meanings = [remove_chinese_with_pipe(regex.sub(PATTERN_PY, replace_num_pinyin_fs, item)) for item in row[3][:-1].split("/")]
        pleco_text = f"{simpl}\t{pinyin}\t{"\n".join([f"{pleco_make_bold(num)} {item}" for num, item in enumerate(meanings, start=1)])}"
        contents = get_def_contents(item)
        for content in contents:
            fwrite.write(f"{pleco_make_new_line(content, make_pleco=True)}\n")

        pass

# Example usage
if __name__ == "__main__":
    counter = ItemCounter()
    counter.add_items(items)
    print("Top 10 items:", counter.get_top_n(10))
    # Output: [('apple', 4), ('banana', 3), ('orange', 3), ('plum', 3), ('grape', 2), ('pineapple', 1), ('peach', 1), ('pear', 1)]

print(f"Writing {num} items")
