import os
import random
from concurrent.futures import ThreadPoolExecutor

from tools_configs import (
    HTML_FOLDER,
    WORDLIST_DIR,
    headword_to_url,
    is_running_on_windows,
    load_frequent_words,
    process_url,
    remove_existing_items,
    url_to_headword,
)

# List of 10 User-Agents (Desktop and Mobile)
USER_AGENTS = [
    # Desktop User-Agents
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/111.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Safari/604.1",
    # Mobile User-Agents
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-A505F) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/14.2 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.1",
]

os.makedirs(HTML_FOLDER, exist_ok=True)


# Function to select a random User-Agent
def get_random_user_agent():
    return random.choice(USER_AGENTS)


# Wrap the process_url function to include User-Agent rotation
def process_url_with_user_agent(url):
    user_agent = get_random_user_agent()
    headers = {"User-Agent": user_agent}
    # print(f"Processing URL: {url} with User-Agent: {user_agent}")
    process_url(url, headers=headers)


# Main execution
if __name__ == "__main__":
    wordlist_file = "redownload-first.txt"
    words_to_redownload = load_frequent_words(wordlist_file)
    new_urls = set([headword_to_url(word) for word in words_to_redownload])

    print(f"Wordlist len: {len(new_urls)}")

    remove_existing_items(new_urls)

    print(f"To download: {len(new_urls)}")

    with open(os.path.join(WORDLIST_DIR, wordlist_file), "w", encoding="utf-8") as file:
        file.writelines([url_to_headword(item) + "\n" for item in sorted(new_urls)])

    cpu_count = os.cpu_count()
    spared_cpus = 5 if is_running_on_windows() else 0
    max_workers = max(1, cpu_count - spared_cpus)  # Leave 2 cores free
    print(f"Using {max_workers} threads for parallel processing")

    new_urls_list = sorted(new_urls, reverse=True)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(process_url_with_user_agent, new_urls_list)

    # print(f"=== Finished processing {len(done_urls)} URLs")
