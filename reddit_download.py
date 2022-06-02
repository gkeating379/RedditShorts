#praw docs
#https://praw.readthedocs.io/en/stable/
import praw
import pandas as pd
import config
from text_to_speech import make_mp3_from_submission

# Create an instance of reddit class

reddit = praw.Reddit(username = config.username,
                     password = config.password,
                     client_id = config.client_id,
                     client_secret = config.client_secret,
                     user_agent = config.user_agent)

subreddit = reddit.subreddit('AmItheAsshole')

df = pd.DataFrame() # creating dataframe for displaying scraped data

# creating lists for storing scraped data
posts = []

# looping over posts and scraping it
for submission in subreddit.top(time_filter='week'):
    temp = {
        'title' : submission.title,
        'upvotes' : submission.score,
        'id' : submission.fullname,
        'body_text' : submission.selftext
    }
    posts.append(temp)

df = pd.DataFrame.from_dict(posts)

print(df.shape)
print(df.head(10))

top_of_week = subreddit.top(limit=1, time_filter='week')

for top in top_of_week:
    make_mp3_from_submission(top)