from pydub import AudioSegment
import pyttsx3
import praw 

#en_us_010 for male
#en_au_001 for female
def make_mp3_from_submission(submission):
    '''takes a submission and creates an mp3 
        reading the title and body of post
    '''

    engine = pyttsx3.init()
    engine.save_to_file(submission.title , f'{submission.fullname}_title.mp3')
    engine.save_to_file(submission.selftext , f'{submission.fullname}_body.mp3')
    engine.runAndWait()

def make_mp3_from_text(text, output_path):
    '''Create a TTS recording of given text string
    Output it to output_path'''

    engine = pyttsx3.init()
    engine.save_to_file(text , output_path)
    engine.runAndWait()

    change_end_silence(text, output_path)

def change_end_silence(text, path):
    '''Modifies silence at end of mp3
    Adds 1 second of silence when end is a period
    Add 0.5 for all other cases
    Requires text read in mp3'''
    
    silence = -50.0 #dB
    sound = AudioSegment.from_file(path)
    duration = len(sound)
    trim = 0 #ms

    #check in 0.1 second intervals if clip is still silent
    #get the silent part at end of clip
    rev_sound = sound.reverse()
    while rev_sound[0:trim].dBFS < silence:
        trim += 0.1
    
    #adding delay as specified above
    if text[:-1] == '.':
        trim -= 1000
    else:
        trim -= 300

    sound = sound[:duration - trim] #cut the clip

    sound.export(path, format='mp3')