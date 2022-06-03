from multiprocessing import AuthenticationError
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import math
import praw
import config
import requests
from io import BytesIO
import pprint

HEIGHT = 560
WIDTH = 900
DIMESIONS = (WIDTH, HEIGHT)
BACKGROUND_COLOR = (17,17,17)
FONT_SIZE = 50
FONT_WIDTH = 30
FONT_HEIGHT = 40
FONT_PATH = 'Video_Components\Courier\CourierPrime-Regular.ttf'
FONT_COLOR = (255,255,255)
#Other good user colors
#(137, 207, 240) 
USER_COLOR = (74, 163, 217)

#reddit stories uses 720 by 360 
def make_title_slide(sub):
    #collect important info of sub
    title = sub.title
    submission_id = sub.fullname
    subreddit_name = f'r/{sub.domain[5:]}'
    sub_poster = f'u/{sub.author}'

    #get sub icon
    sub_icon_link = subreddit.icon_img
    response = requests.get(sub_icon_link)
    sub_icon = Image.open(BytesIO(response.content))

    image = Image.new('RGB', DIMESIONS, BACKGROUND_COLOR)
    image = add_title_text(image, title)
    

    #make sub icon a circle
    icon_border = Image.open('Video_Components\SubBorder.png')
    icon_border = icon_border.resize((sub_icon.height, sub_icon.width))
    sub_icon.paste(icon_border, (0,0), icon_border.convert('RGBA')) #third param makes a transparent mask

    #resize sub icon
    sub_icon = sub_icon.resize((100,100))

    #paste icon onto slide
    image.paste(sub_icon, (40,40))

    #add subreddit name
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    draw.text((160,60), subreddit_name, FONT_COLOR,font=font)

    #add poster
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE - 20)
    draw.text((160,120), sub_poster, USER_COLOR ,font=font)




    image.save(f'{submission_id}.png') #save image to its 'fullname.png'


def add_title_text(image, title):
    char_per_line = (WIDTH - 2 * FONT_WIDTH) // FONT_WIDTH

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
        
        draw.text((FONT_WIDTH, ((HEIGHT - 200) / 2) + FONT_HEIGHT*i), line,FONT_COLOR,font=font)

        i += 1

    return image.crop((0, 0, WIDTH, 200 + i*FONT_HEIGHT ))



reddit = praw.Reddit(username = config.username,
                     password = config.password,
                     client_id = config.client_id,
                     client_secret = config.client_secret,
                     user_agent = config.user_agent)

subreddit = reddit.subreddit('AmItheAsshole')
top_of_week = subreddit.top(limit=5, time_filter='week')

for top in top_of_week:
    make_title_slide(top)
