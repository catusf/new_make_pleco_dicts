import hanzidentifier
from playwright.sync_api import sync_playwright
import re
import urllib
import time
import os
import glob
import json
from concurrent.futures import ThreadPoolExecutor

from tools_configs import *

HTML_FOLDER = "html"

# Words to process
words_to_redownload = load_frequent_words("redownload-new.txt")
list_to_read = words_to_redownload

# Website URL template
base_url = "https://hanzii.net/search/word/"

print(f"{len(list_to_read)=}")

done_urls = set()
new_urls = set([headword_to_url(word) for word in list_to_read])

files = glob.glob(f"{HTML_FOLDER}/*.html")
print(f"There are existing {len(files)} files")

files_checked = set()
broken_files = []
has_nodef_files = []

trad_count = 0

find_all_chinese = True

for num, filepath in enumerate(files):
    headword, ext = os.path.splitext(os.path.split(filepath)[1])
    url = headword_to_url(headword)

    check_file_exists = True

    if check_file_exists:
        if is_non_zero_file(filepath):
            done_urls.add(url)

            if url in new_urls:
                new_urls.remove(url)

            check_file_contents = False

            if check_file_contents:
                if filepath not in files_checked:
                    with open(filepath, "r", encoding="utf-8") as fin:
                        html = fin.read()
                        files_checked.add(filepath)

                        if html.find(MARKER_GOOD_FILE) == -1:
                            broken_files.append(filepath)

                        if html.find(MARKER_HAS_DEF_FILE) == -1:
                            has_nodef_files.append(filepath)

                        if find_all_chinese:
                            chinese_words = get_chinese_words(html)

                            for headword in chinese_words:
                                url = headword_to_url(headword)

                                if url not in done_urls:
                                    new_urls.add(url)

                    if num % 100 == 0:
                        print(f"File num {num} urls {len(new_urls)=} {len(broken_files)=} {len(has_nodef_files)=}")

        else:
            new_urls.add(url)

    else:
        new_urls.add(url)

with open("broken_file_list.txt", "w", encoding="utf-8") as fout:
    fout.writelines([(line + "\n") for line in broken_files])

with open("has_nodef_list.txt", "w", encoding="utf-8") as fout:
    fout.writelines([(line + "\n") for line in has_nodef_files])

print(f"Traditional count {trad_count}")

print(f"{len(new_urls)=}")

if not new_urls:
    print("No more urls to search")
    exit(0)


def process_url(url):
    headword = url_to_headword(url)

    if not headword:
        print(f"Wrong headword {headword}")
        return

    filename = os.path.join(HTML_FOLDER, f"{headword}.html")

    html = ""
    if is_non_zero_file(filename):
        print(f"Restoring {headword}")
        with open(filename, "r", encoding="utf-8") as fin:
            html = fin.read()
    else:
        print(f"Downloading {headword}")
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()

                page.goto(url)
                time.sleep(WAIT_TIME)

                html = page.content()
                done_urls.add(url)

                with open(filename, "w", encoding="utf-8") as fout:
                    fout.write(html)

                browser.close()
        except Exception as e:
            print(f"Error downloading {headword}: {e}")


# Split the URLs into a sorted list
new_urls_list = sorted(new_urls, reverse=True)

# Parallel processing
if __name__ == "__main__":
    cpu_count = os.cpu_count()
    max_workers = max(1, cpu_count)  # Leave 2 cores free
    print(f"Using {max_workers} threads for parallel processing")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(process_url, new_urls_list)

    print(f"=== Finished processing {len(done_urls)} URLs")
