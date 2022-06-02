from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import math
import praw
import config

HEIGHT = 560
WIDTH = 900
DIMESIONS = (WIDTH, HEIGHT)
BACKGROUND_COLOR = (17,17,17)
FONT_SIZE = 50
FONT_WIDTH = 30
FONT_HEIGHT = 40
FONT_PATH = 'Video_Components\Courier\CourierPrime-Regular.ttf'

#reddit stories uses 720 by 360 
image = Image.new('RGB', DIMESIONS, BACKGROUND_COLOR)
draw = ImageDraw.Draw(image)

# font = ImageFont.truetype(<font-file>, <font-size>)
font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
# draw.text((x, y),"Sample Text",(r,g,b))
#draw.text((FONT_WIDTH, HEIGHT - 220),"Sample Text But I really love balls lol lol lol lol lol lol lol",(255,255,255),font=font)



image.save('png.png')

def make_title_slide(title):
    length = len(title)
    char_per_line = (WIDTH - 2 * FONT_WIDTH) // FONT_WIDTH
    num_lines = int(math.ceil(length / char_per_line))

    image = Image.new('RGB', DIMESIONS, BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    #wraps the text around the size of the fake reddit card
    i = 0
    while(title != ''): 
        line = title[:char_per_line + 1]
        end = char_per_line + 1

        #end line on the last space if it exists and
        #if the phrase is too long for one line
        if len(title) > char_per_line:
            last_space = line.rfind(' ')
            if last_space != -1:
                line = title[:last_space + 1]
                end = last_space + 1

        #keep going with remaining text
        title = title[end:]
        
        draw.text((FONT_WIDTH, HEIGHT - 220 + FONT_HEIGHT*i), line,(255,255,255),font=font)

        i += 1

    image.save('png.png')


reddit = praw.Reddit(username = config.username,
                     password = config.password,
                     client_id = config.client_id,
                     client_secret = config.client_secret,
                     user_agent = config.user_agent)

subreddit = reddit.subreddit('AmItheAsshole')
top_of_week = subreddit.top(limit=1, time_filter='week')

for top in top_of_week:
    make_title_slide(top.title)
