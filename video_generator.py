from moviepy.editor import AudioFileClip, ImageClip
from PIL.PngImagePlugin import PngInfo
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import praw
import config
import requests
from io import BytesIO
import os
from os.path import exists

from text_to_speech import make_mp3_from_text

#parkour video link
#https://www.youtube.com/watch?v=875A5jdmn8k

HEIGHT = 540
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

def make_text_slides(sub):
    if not os.path.exists(sub.fullname):
        os.makedirs(sub.fullname)

    make_title_slide(sub)
    make_body_cards(sub)

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

    metadata = PngInfo()
    metadata.add_text("Content", title)




    image.save(f'{submission_id}/{submission_id}_titleslide.png',  pnginfo=metadata) #save image to its 'fullname.png'


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

def make_body_cards(sub):
    body = sub.selftext
    submission_id = sub.fullname
    
    new_img = Image.new('RGB', DIMESIONS, BACKGROUND_COLOR)
    make_single_body(body, new_img, submission_id, 1)


def make_single_body(text, image, submission_id, iteration):
    char_per_line = (WIDTH - 2 * FONT_WIDTH) // FONT_WIDTH

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    #wraps the text around the size of the fake reddit card
    i = 0
    this_slide_text = ''
    while(text != ''): 

        if (i+1)*FONT_HEIGHT > HEIGHT:
            print( (i+1)*FONT_HEIGHT)
            new_img = Image.new('RGB', DIMESIONS, BACKGROUND_COLOR)
            make_single_body(text, new_img, submission_id, iteration + 1)
            break

        line = text[:char_per_line + 1]
        end = char_per_line + 1

        #end line on the last space if it exists and
        #if the phrase is too long for one line
        if len(text) > char_per_line:
            last_space = line.rfind(' ')
            if last_space != -1:
                line = text[:last_space + 1]
                end = last_space + 1

        #remove break characters
        line_break_index = line.find('\n')
        if line_break_index != -1:
            line = text[:line_break_index]
            end = line_break_index + 2

        #keep track of text on this slide
        this_slide_text += text[:end]

        #keep going with remaining text
        text = text[end:]
        
        draw.text((FONT_WIDTH, FONT_HEIGHT*i), line,FONT_COLOR,font=font)

        i += 1

        

    metadata = PngInfo()
    metadata.add_text("Content", this_slide_text)

    cropped_img =  image.crop((0, 0, WIDTH, 20 + i*FONT_HEIGHT ))
    cropped_img.save(f'{submission_id}/{submission_id}_body_{iteration}.png',  pnginfo=metadata) #save image to its 'fullname.png'

def make_all_slides_mp4(submission_id):
    '''Build mp4 combining slides with the TTS recording of 
    their content'''
    make_title_mp4(submission_id)
    make_body_mp4(submission_id)

def make_title_mp4(submission_id):
    '''Create mp4 combining title slide with TTS reading of it'''
    img_path = f'{submission_id}/{submission_id}_titleslide.png'
    audio_path = f'{submission_id}/{submission_id}_title.mp3'
    output_path = f'{submission_id}/{submission_id}_title.mp4'

    
    #make audio
    title_slide = Image.open(img_path)
    text = title_slide.text['Content']
    make_mp3_from_text(text, audio_path)

    img_clip = ImageClip(img_path) 
    audio_clip = AudioFileClip(audio_path)

    video_clip = img_clip.set_audio(audio_clip)
    video_clip.duration = audio_clip.duration
    video_clip.write_videofile(output_path, fps=24)

def make_body_mp4(submission_id):
    '''Make mp4 for each body slide present'''
    #frame for while loop
    img_path_frame = f'{submission_id}/{submission_id}_body'

    #loop for each body slide 1-X
    i = 1
    while ( exists(f'{img_path_frame}_{i}.png') ):
        img_path = f'{img_path_frame}_{i}.png'
        audio_path = f'{submission_id}/{submission_id}_body_{i}.mp3'
        output_path = f'{submission_id}/{submission_id}_body_{i}.mp4'

        
        #make audio
        title_slide = Image.open(img_path)
        text = title_slide.text['Content']
        make_mp3_from_text(text, audio_path)

        img_clip = ImageClip(img_path) 
        audio_clip = AudioFileClip(audio_path)

        video_clip = img_clip.set_audio(audio_clip)
        video_clip.duration = audio_clip.duration
        video_clip.write_videofile(output_path, fps=24)

        i += 1 


#testing
reddit = praw.Reddit(username = config.username,
                     password = config.password,
                     client_id = config.client_id,
                     client_secret = config.client_secret,
                     user_agent = config.user_agent)

subreddit = reddit.subreddit('AmItheAsshole')
top_of_week = subreddit.top(limit=1, time_filter='week')

for top in top_of_week:
    make_text_slides(top)
    make_all_slides_mp4(top.fullname)