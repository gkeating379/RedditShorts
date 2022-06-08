from moviepy.editor import AudioFileClip, ImageClip, VideoFileClip, CompositeVideoClip
import moviepy
from PIL.PngImagePlugin import PngInfo
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import praw
from torch import true_divide
import config
import requests
from io import BytesIO
import os
import random
import shutil
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

def make_text_slides(subreddit, sub):
    if not os.path.exists(sub.fullname):
        os.makedirs(sub.fullname)

    make_title_slide(subreddit, sub)
    make_body_cards(sub)

#reddit stories uses 720 by 360 
def make_title_slide(subreddit, sub):
    #collect important info of sub
    title = sub.title
    submission_id = sub.fullname
    subreddit_name = f'r/{sub.domain[5:]}'
    sub_poster = f'u/{sub.author}'

    #get sub icon
    sub_icon_link = subreddit.community_icon
    if sub_icon_link != '':
        response = requests.get(sub_icon_link)
        sub_icon = Image.open(BytesIO(response.content))
    else:
        sub_icon = Image.open('Video_Components\SubDefaultBackground.png')

    image = Image.new('RGB', DIMESIONS, BACKGROUND_COLOR)
    image = add_title_text(image, title)
    
    #resize sub icon
    sub_icon = sub_icon.resize((100,100))
    
    #make sub icon a circle
    icon_border = Image.open('Video_Components\SubBorder.png')
    icon_border = icon_border.resize((sub_icon.height, sub_icon.width))
    sub_icon.paste(icon_border, (0,0), icon_border.convert('RGBA')) #third param makes a transparent mask

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
    line_break = False
    while(text != ''): 

        #if too many lines have been written to fit
        #or a line break has been reached
        #make a new slide
        if (i+1)*FONT_HEIGHT > HEIGHT or line_break:
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

        #if a linebreak is the start of the slide just skip it
        while (line_break_index == 0):
            line = line[1:]
            line_break_index = line.find('\n')
                
        #if a linebreak is somewhere in the text body then go to next slide
        if line_break_index != -1:
            line = text[:line_break_index]
            end = line_break_index + 1

            line_break = True

        #keep track of text on this slide
        this_slide_text += text[:end]

        #keep going with remaining text
        text = text[end:]
        
        draw.text((FONT_WIDTH, FONT_HEIGHT*i), line, FONT_COLOR, font=font)

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
        video_clip = video_clip.set_duration(audio_clip.duration) #Remove slight gap at end of mp3
        video_clip.write_videofile(output_path, fps=10)

        i += 1 

def get_random_bRoll(submission_id):
    '''Get a randomly selected broll clip as long as 
    the TTS for a given post'''
    
    output_path = f'{submission_id}/{submission_id}_bRoll.mp4'
    title_path = f'{submission_id}/{submission_id}_title.mp4'
    vid_path_frame = f'{submission_id}/{submission_id}_body'

    title = VideoFileClip(title_path)

    #add each duration to get total length of TTS
    i = 1
    duration = title.duration
    while ( exists(f'{vid_path_frame}_{i}.mp4') ):
        video_clip = VideoFileClip(f'{vid_path_frame}_{i}.mp4')
        duration += video_clip.duration
        i += 1

    bRoll_path = 'Video_Components\MCParkour.mp4'
    bRoll = VideoFileClip(bRoll_path)
    bRoll_length = bRoll.duration

    start = random.uniform(0, bRoll_length - duration) 
    end = start + duration

    #output cut video to output_path
    moviepy.video.io.ffmpeg_tools.ffmpeg_extract_subclip(bRoll_path, start, end, targetname=output_path)

def make_final_video(submission_id):
    get_random_bRoll(submission_id)

    title_path = f'{submission_id}/{submission_id}_title.mp4'
    vid_path_frame = f'{submission_id}/{submission_id}_body'
    bRoll_path = f'{submission_id}/{submission_id}_bRoll.mp4'
    output_path = f'Output/{submission_id}_final.mp4'

    bRoll = VideoFileClip(bRoll_path)
    title = VideoFileClip(title_path)

    #start the title at start of video
    title = title.set_pos(('center', 'center'))
    title = title.set_start(0)

    clip_array = [bRoll, title]

    #for each body slide
    #add to clip_array in order
    #set start to the end of last clip
    i = 1
    used_duration = title.duration
    while ( exists(f'{vid_path_frame}_{i}.mp4') ):
        video_clip = VideoFileClip(f'{vid_path_frame}_{i}.mp4')
        video_clip = video_clip.set_pos(('center', 'center'))
        video_clip = video_clip.set_start(used_duration) 
        used_duration += video_clip.duration
        clip_array.append(video_clip)
        i += 1

    output_vid = CompositeVideoClip(clip_array)

    output_vid.write_videofile(
        output_path,
        fps=60,
        remove_temp=True,
        codec="libx264",
        audio_codec="aac",
        threads = 16,
    )

    #delete frame files to make final video
    #shutil.rmtree(f'{submission_id}')

def video_from_submission(subreddit, sub):
    make_text_slides(subreddit, sub)
    make_all_slides_mp4(sub.fullname)
    make_final_video(sub.fullname)

#testing
# reddit = praw.Reddit(username = config.username,
#                      password = config.password,
#                      client_id = config.client_id,
#                      client_secret = config.client_secret,
#                      user_agent = config.user_agent)

# subreddit = reddit.subreddit('AmItheAsshole')
# top_of_week = subreddit.top(limit=5, time_filter='week')

# i = 0
# for top in top_of_week:
#     if i == 4:
#         video_from_submission(top)

#     i += 1