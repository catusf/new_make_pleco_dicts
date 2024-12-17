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
    wordlist_file = "redownload-first.txt"
    words_to_redownload = load_frequent_words(wordlist_file)
    new_urls = set([headword_to_url(word) for word in words_to_redownload])

    remove_existing_items(new_urls)

    with open(os.path.join(WORDLIST_DIR, wordlist_file), "w", encoding="utf-8") as file:
        file.writelines([url_to_headword(item) + "\n" for item in sorted(new_urls)])

    cpu_count = os.cpu_count()
    spared_cpus = 5 if is_running_on_windows() else 0
    max_workers = max(1, cpu_count - spared_cpus)  # Leave 2 cores free
    print(f"Using {max_workers} threads for parallel processing")

    new_urls_list = sorted(new_urls, reverse=True)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(process_url, new_urls_list)

    # print(f"=== Finished processing {len(done_urls)} URLs")
