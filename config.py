from enum import Enum

import pyttsx3
import yaml

# reddit
secrets = yaml.safe_load(open('secret.yaml', 'r'))
SUBREDDIT = 'python'
LIMIT_POST = 2
LIMIT_COMMENT = 3

# storage
POST_NAME = 'post_{post_id}'
COMMENT_NAME = 'comment_{post_id}{counter}'
BACKGROUND_VIDEO = r'templates/bg_videos/bg1.mkv'
COMMENT_TEMPLATE = r'templates/comment.png'
POST_TEMPLATE = r'templates/post.png'
OUTPUT_FOLDER = r'output/result_videos/'
POST_OUTPUT = r'output/post_images/'
POST_AUDIO = r'output/post_audio/'

# video
VIDEO_RATIO = 9/16
FPS = 60
FONT_SIZE = 20
FONT = 'arial.ttf'

# voice
engine = pyttsx3.init()
VOICE_RATE = engine.getProperty('rate')-30
VOICE_VOLUME = engine.getProperty('volume')+2


class ImageTypes(Enum):
    Comment = 'Comment'
    Post = 'Post'


class CommentsTextLimit(Enum):
    MaxLines = 12
    MaxChars = 79


class PostTextLimit(Enum):
    MaxLines = 21
    MaxChars = 70


class Extensions(Enum):
    Audio = '.mp3'
    Video = '.mp4'
    Image = '.png'

