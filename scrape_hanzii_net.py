import os

# import json
from concurrent.futures import ThreadPoolExecutor
from tools_configs import (
    headword_to_url,
    load_frequent_words,
    url_to_headword,
    # is_non_zero_file,
    process_url,
    is_running_on_windows,
    WORDLIST_DIR,
    HTML_FOLDER,
    remove_existing_items,
)

os.makedirs(HTML_FOLDER, exist_ok=True)


# Parallel processing
if __name__ == "__main__":
    wordlist_file = "redownload-orgiginal.txt"
    words_to_redownload = load_frequent_words(wordlist_file)
    new_urls = set([headword_to_url(word) for word in words_to_redownload])

    remove_existing_items(new_urls)

    new_urls_list = sorted(new_urls, reverse=True)

    half = int(len(new_urls_list)/2)

    list_first = new_urls_list[:half]
    list_second = new_urls_list[half:]

    print(f"{len(list_first)=}")
    print(f"{len(list_second)=}")


    with open(os.path.join(WORDLIST_DIR, "redownload-first.txt"), "w", encoding="utf-8") as file:
        file.writelines([url_to_headword(item) + "\n" for item in list_first])

    with open(os.path.join(WORDLIST_DIR, "redownload-second.txt"), "w", encoding="utf-8") as file:
        file.writelines([url_to_headword(item) + "\n" for item in list_second])

