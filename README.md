# RedditShorts
Makes the Reddit post text to speech videos that are common and popular on short video streaming platforms like TikTok and YouTube Shorts

Outputs go to output folder and are named based on the id of the post they came from (ex. t3_v2ahu9_final.mp4)

Subreddits are randomly chosen from a two lists.  The first list is subreddits where only the post will be in the final video
and the second are those which will include comments (post_lists vs comments_list in reddit_download)

To run, include the path to the video you want to use as background footage for the next short.
Ex. python reddit_download.py Video_Components\MCParkour.mp4