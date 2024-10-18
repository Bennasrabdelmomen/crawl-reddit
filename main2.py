from bs4 import BeautifulSoup
from selenium import webdriver
import time



##get data from x link on reddit and store in txt file to be fed into le other main
driver = webdriver.Chrome()

url = "https://www.reddit.com/search/?q=%D8%A7%D9%84%D8%A7%D9%83%D8%AA%D8%A2%D8%A8&cId=c7c7e9b5-0f76-43a1-94dc-c2d45c31ede1&iId=8c9b6649-a4d5-4a29-a0af-73e6e9ed98be"
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

with open("reddit_results.txt", "w", encoding="utf-8") as file:
    for url in post_urls:
        file.write("https://www.reddit.com" + url + "\n")
driver.quit()

print("Results saved in reddit_results.txt")
