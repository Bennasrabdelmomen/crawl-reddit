import praw
import pandas as pd
import os

reddit = praw.Reddit(user_agent=True, client_id="ssss",
                     client_secret="sss",
                     user_name="sss", password="sss")
folder_path = 'reddit_crawled_urls'
file_counter = 1
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)

        with open(file_path, 'r', encoding='utf-8') as file:
            valid_links = [line.strip() for line in file.readlines()]

        posts_data = []

        for full_url in valid_links:
            try:
                post = reddit.submission(url=full_url)

                post.comments.replace_more(limit=0)
                comments = [comment.body for comment in post.comments.list()]

                post_info = {
                    "title": post.title,
                    "post_content": post.selftext,
                    "num_comments": post.num_comments,
                    "comments": comments
                }

                posts_data.append(post_info)

            except Exception as e:
                print(f"An error occurred while processing {full_url}: {e}")

        df = pd.DataFrame(posts_data)

        df.to_csv(f"df{file_counter}.csv", index=False)
        print(f"Dataset saved to 'df{file_counter}.csv'.")

        file_counter += 1
