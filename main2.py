from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os

def try_load_url_and_save(url, file_path, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            
            driver = webdriver.Chrome()

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

            
            with open(file_path, "w", encoding="utf-8") as file:
                for post_url in post_urls:
                    file.write("https://www.reddit.com" + post_url + "\n")

            
            if os.path.getsize(file_path) == 0:
                print(f"Attempt {attempt + 1} failed for URL: {url} (empty file). Retrying...")
                time.sleep(2)  
            else:
                driver.quit()  
                return True 
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for URL: {url}. Error: {e}")
            time.sleep(2) 
        finally:
            driver.quit() 
    print(f"URL unavailable after {max_attempts} attempts or file is still empty: {url}")
    return False

with open("url_keywords.txt", "r", encoding="utf-8") as file:
    keywords_url = ["https://www.reddit.com/search/?q=" + line.strip() for line in file.readlines()]

output_folder = 'reddit_crawled_urls'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for url in keywords_url:
    keyword = url.split("?q=")[-1]

    file_name = f"urls_to_crawl_{keyword}.txt"
    file_path = os.path.join(output_folder, file_name)

    try_load_url_and_save(url, file_path)

print(f"Results saved in the folder: {output_folder}")
