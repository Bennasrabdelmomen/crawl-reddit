import praw
import pandas as pd
import os


reddit = praw.Reddit(user_agent=True, client_id="sss",
                     client_secret="sss",
                     user_name="sss", password="sss")


folder_path = 'reddit_crawled_urls'

save_folder = 'datasets_unprocessed'
if not os.path.exists(save_folder):
    os.makedirs(save_folder)  
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)
        
        keyword = filename.replace('urls_to_crawl_', '').replace('.txt', '')

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

        csv_path = os.path.join(save_folder, f"{keyword}.csv")
        df.to_csv(csv_path, index=False)
        print(f"Dataset saved to '{csv_path}'.")
