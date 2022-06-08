#praw docs
#https://praw.readthedocs.io/en/stable/
import praw
from yarg import get
import video_generator
import random
import pandas as pd
import config
from text_to_speech import make_mp3_from_submission

#subreddit list for post only
post_list = ['confession', 'offmychest', 'AmItheAsshole', 'TrueOffMyChest']

#subreddit list for comment only
comment_list =['AskReddit']

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
    top.comments.replace_more(limit=0)
    for comment in top.comments[1:5]:
        print(comment.body)
        print('----------------')

#everything above this point is testing
#TODO change above

def get_random_submission(subreddits, timeframe='week', sample_size=10):
    '''Randomly get a submission from a post-only subreddit
    Returns subreddit obj, post obj
    subreddits -> list of subreddits to pick from
    timeframe -> the top of all (timeframe) 
    sample_size -> number of top posts within time frame to pick from'''

    subreddit_name = random.choice(subreddits) #pick a random subreddit

    #initalize the reddit class
    reddit = praw.Reddit(username = config.username,
                     password = config.password,
                     client_id = config.client_id,
                     client_secret = config.client_secret,
                     user_agent = config.user_agent)

    subreddit = reddit.subreddit(subreddit_name)
    top = subreddit.top(limit=sample_size, time_filter=timeframe)
    
    rand_index = random.randint(0,sample_size - 1)
    i = 0
    for sub in top:
        if i==rand_index:
            print(sub.title)
            return subreddit, sub
        i+=1

    
rand_sub, rand_submission = get_random_submission(post_list)
video_generator.video_from_submission(rand_sub, rand_submission)