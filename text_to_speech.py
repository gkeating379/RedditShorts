import pyttsx3
import praw 

def make_mp3_from_submission(submission):
    '''takes a submission and creates an mp3 
        reading the title and body of post
    '''
    
    engine = pyttsx3.init()
    engine.save_to_file(submission.title , f'{submission.fullname}_title.mp3')
    engine.save_to_file(submission.selftext , f'{submission.fullname}_body.mp3')
    engine.runAndWait()