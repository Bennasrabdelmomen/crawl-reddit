from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os

driver = webdriver.Chrome()

with open("url_keywords.txt", "r", encoding="utf-8") as file:
    keywords_url = ["https://www.reddit.com/search/?q="+line.strip() for line in file.readlines()]

output_folder = 'reddit_crawled_urls'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


file_counter = 1
for url in keywords_url:
    driver.get(url)
    scroll_pause_time = 2
    screen_height = driver.execute_script("return window.screen.height;")
    i = 1

    while True:
        driver.execute_script(f"window.scrollTo(0, {screen_height * i});")
        i += 1
        time.sleep(scroll_pause_time)

        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        if screen_height * i > scroll_height:
            break

    soup = BeautifulSoup(driver.page_source, "html.parser")

    posts = soup.find_all('a', href=True)

    post_urls = [post['href'] for post in posts if '/r/' in post['href']]

    file_name = f"urls_to_crawl{file_counter}.txt"
    file_path = os.path.join(output_folder, file_name)

    with open(file_path, "w", encoding="utf-8") as file:
        for post_url in post_urls:
            file.write("https://www.reddit.com" + post_url + "\n")

    file_counter += 1

driver.quit()

print(f"Results saved in the folder: {output_folder}")
