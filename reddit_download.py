#praw docs
#https://praw.readthedocs.io/en/stable/
import praw
import pandas as pd
import config

# Create an instance of reddit class

#TODO remove personal info and passwords
reddit = praw.Reddit(username = config.username,
                     password = config.password,
                     client_id = config.client_id,
                     client_secret = config.client_secret,
                     user_agent = config.user_agent)

subreddit = reddit.subreddit('AmItheAsshole')

#TODO Change everything below until print statements

df = pd.DataFrame() # creating dataframe for displaying scraped data

# creating lists for storing scraped data
posts = []

# looping over posts and scraping it
for submission in subreddit.top():
    temp = {
        'title' : submission.title,
        'upvotes' : submission.score,
        'id' : submission.id,
        'body_text' : submission.selftext
    }
    posts.append(temp)

print(posts)
df = pd.DataFrame.from_dict(posts)

print(df.shape)
print(df.head(10))