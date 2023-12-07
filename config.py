from enum import Enum

import pyttsx3
import yaml

# reddit
secrets = yaml.safe_load(open('secret.yaml', 'r'))
SUBREDDIT = ''
LIMIT_POST = 20
LIMIT_COMMENT = 5

# storage
POST_NAME = 'post_{post_id}'
COMMENT_NAME = 'comment_{post_id}{counter}'
COMMENT_TEMPLATE = r'templates/comment.png'
POST_TEMPLATE = r'templates/post.png'
OUTPUT_FOLDER = r'output/result_videos/'
POST_OUTPUT = r'output/post_images/'
POST_AUDIO = r'output/post_audio/'

# video
BACKGROUND_VIDEO = r'templates/bg_videos/bg1.mkv'
PREPROCESSED_BACKGROUND_VIDEO = r'templates/preprocessed_bg_video/bg1.mkv'
VIDEO_RATIO = 9/16
FPS = 60
FONT_SIZE = 22
FONT = 'arial.ttf'
TITLE_MAX_CHARS = 34
TITLE_FONT = r"templates\fonts\cardigan titling bd it.otf"
TITLE_FONT_SIZE = FONT_SIZE+2
# voice
engine = pyttsx3.init()
VOICE_RATE = engine.getProperty('rate')-23
VOICE_VOLUME = engine.getProperty('volume')+2


class ImageTypes(Enum):
    Comment = 'Comment'
    Post = 'Post'


class CommentsTextLimit(Enum):
    MaxLines = 12
    MaxChars = 65


class PostTextLimit(Enum):
    MaxLines = 19
    MaxChars = 55


class Extensions(Enum):
    Audio = '.mp3'
    Video = '.mp4'
    Image = '.png'

