import concurrent.futures
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from tools_configs import *
import signal
import readchar
import sys

HTML_FOLDER = "html"


# Function to process a single URL
def fetch_url(driver_options, url, headword, done_urls):
    filename = f"{headword}.html"
    filepath = os.path.join(HTML_FOLDER, filename)

    if is_non_zero_file(filepath):
        print(f"Restoring {headword}")
        return url  # URL is already processed

    print(f"Downloading {headword}")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=driver_options)
    try:
        driver.get(url)
        time.sleep(WAIT_TIME)

        html = driver.page_source
        done_urls.add(url)

        with open(filepath, "w", encoding="utf-8") as fout:
            fout.write(html)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    finally:
        driver.quit()

    return url


import glob


def remove_existing_items(new_urls, folder=HTML_FOLDER):
    files = glob.glob(f"{folder}/*.html")
    print(f"There are existing {len(files)} files")

    done_urls = set()

    for num, filepath in enumerate(files):
        headword, ext = os.path.splitext(os.path.split(filepath)[1])
        # filename = f'{HTML_FOLDER}/{headword}.html'
        url = headword_to_url(headword)

        check_file_exists = True

        if check_file_exists:
            if is_non_zero_file(filepath):
                done_urls.add(url)

                if url in new_urls:
                    new_urls.remove(url)

                # See if file contains any new words
            else:
                new_urls.add(url)

        else:
            new_urls.add(url)

    return new_urls


def keyboard_handler(signum, frame):
    msg = "Ctrl-c was pressed. Do you really want to exit? y/n "
    print(msg, end="", flush=True)
    res = readchar.readchar()
    if res == "y":
        sys.exit(1)
    else:
        print("", end="\r", flush=True)
        print(" " * len(msg), end="", flush=True)  # clear the printed line
        print("    ", end="\r", flush=True)


# Main parallel processing logic
def main():

    signal.signal(signal.SIGINT, keyboard_handler)

    os.makedirs(HTML_FOLDER, exist_ok=True)

    # Initialize Selenium driver options
    options = webdriver.ChromeOptions()
    # options.headless = True
    options.add_argument("--headless=new")

    # Load the list of URLs to process
    words_to_redownload = load_frequent_words("redownload.txt")
    new_urls = set([headword_to_url(word) for word in words_to_redownload])

    remove_existing_items(new_urls)

    with open("redownload-remains.txt", "w", encoding="utf-8") as file:
        file.writelines([url_to_headword(item) + "\n" for item in sorted(new_urls)])

    print(f"Total URLs to fetch: {len(new_urls)}")
    done_urls = set()
    cpu_count_used = os.cpu_count() - 1
    print(f"Using {cpu_count_used} CPU cores")

    with concurrent.futures.ThreadPoolExecutor(max_workers=cpu_count_used) as executor:  # Adjust max_workers as needed
        future_to_url = {
            executor.submit(fetch_url, options, url, url_to_headword(url), done_urls): url for url in sorted(new_urls)
        }

        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
                print(f"Completed: {result}")
            except Exception as e:
                print(f"Error processing {url}: {e}")

    print(f"Finished processing {len(done_urls)} URLs")


if __name__ == "__main__":
    main()
