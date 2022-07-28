#praw docs
#https://praw.readthedocs.io/en/stable/
import pickle
import shutil
import praw
import video_generator
import random
import config
import sys

bRoll_path = sys.argv[1]

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

def get_random_submission(subreddits, timeframe='week', sample_size=10):
    '''Randomly get a submission from a post-only subreddit
    Returns subreddit obj, post obj, subreddit name str
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
            return subreddit, sub, subreddit_name
        i+=1

def generate_random_video(post_list, comments_list):
    '''Take a list of all post and comment subreddits and 
    randomly selects a post from them to make into a video'''
    comment_post = False
    subreddits = post_list + comments_list

    rand_sub, rand_submission, rand_subreddit_name = get_random_submission(subreddits)

    #set if its a comment sub
    if rand_subreddit_name in comments_list:
        comment_post = True

    #check if video has already been made for this post
    video_ids = pickle.load(open('video_ids.pkl', 'rb'))
    
    if rand_submission.fullname in video_ids:
        generate_random_video(post_list, comments_list)
    else:
        #create video
        video_generator.video_from_submission(rand_sub, rand_submission, comment_post, bRoll_path)

        #add submission id to list to not reuse content
        video_ids.append(rand_submission.fullname)
        pickle.dump(video_ids, open('video_ids.pkl', 'wb'))

    shutil.rmtree(rand_submission.fullname)

generate_random_video(post_list, comment_list)