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
