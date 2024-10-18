import praw
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

with open('unique_valid_reddit_urls.txt', 'r', encoding='utf-8') as file:
    valid_links = [line.strip() for line in file.readlines()]

reddit = praw.Reddit(user_agent=True, client_id="sss ",
                     client_secret="sss",
                     user_name="sss", password="sss")

posts_data = []

for full_url in valid_links:
    try:
        post = reddit.submission(url=full_url)

        post.comments.replace_more(limit=0)
        comments = [comment.body for comment in post.comments.list()]

        post_info = {
            "title": post.title,
            "selftext": post.selftext,
            "num_comments": post.num_comments,
            "comments": comments
        }

        posts_data.append(post_info)

    except Exception as e:
        print(f"An error occurred while processing {full_url}: {e}")

df = pd.DataFrame(posts_data)
#df = df.drop_duplicates()

df.to_csv("reddit_posts.csv", index=False)
print("Posts and comments saved to 'reddit_posts.csv'.")
