from moviepy.video.io.VideoFileClip import VideoFileClip

from add_text_to_image import ImageGenerator, ImageTypes
from config import BACKGROUND_VIDEO, POST_AUDIO, POST_TEMPLATE, POST_OUTPUT,COMMENT_TEMPLATE, SUBREDDIT,\
    LIMIT_POST, LIMIT_COMMENT, OUTPUT_FOLDER, Extensions, POST_NAME, COMMENT_NAME, PREPROCESSED_BACKGROUND_VIDEO
from reddit_facade import get_posts, fetch_comments
from sqllite_facade import Post, add_post
from text_to_voice import text_to_speech
from utils import empty_folder
from video_generator import export_video,create_video,resize_bg_video,merge_video_clips,append_video_clips
from traceback import print_exc
import os


print('starting cleaning up ....')
# cleaning up temp data
empty_folder(POST_OUTPUT)
empty_folder(POST_AUDIO)
print('clean up done')

image_gen = ImageGenerator(post_template=POST_TEMPLATE, comment_template=COMMENT_TEMPLATE)

# generate background video
bg_clip = VideoFileClip(PREPROCESSED_BACKGROUND_VIDEO)

# fetch post and comments
posts = get_posts(subreddit_name=SUBREDDIT, limit=LIMIT_POST)
for post in posts:
    print(f'started {post.id}')
    # save to db
    try:

        add_post(Post(id=post.id, name=post.title, author=post.author.name))
        if len(post.media_embed.keys()) > 0:
            # if media is there then we will use that post.
            print('found media. skipping ...')
            continue

        comments = fetch_comments(post, limit=LIMIT_COMMENT)

        # convert post to images
        post_text = image_gen.generate_image(text=post.selftext,
                                 image_type=ImageTypes.Post,
                                 output_dir=POST_OUTPUT,
                                 output_file_name=POST_NAME.format(post_id=post.id), title=post.title)
        # generate voice for post
        page = 1
        post_clips = []
        for text in post_text:
            text_to_speech(text, POST_AUDIO+POST_NAME.format(post_id=post.id)+str(page)+Extensions.Audio.value)
            page+=1

        # convert images to videos

        post_images = [os.path.abspath(POST_OUTPUT + filename)
                       for filename in os.listdir(POST_OUTPUT)
                       if filename.startswith(POST_NAME.format(post_id=post.id))
                       ]
        for post_image in post_images:
            audio_path = [os.path.abspath(POST_AUDIO + filename)
                          for filename in os.listdir(POST_AUDIO)
                          if filename.startswith('.'.join(os.path.basename(post_image).split('.')[0:-1])) and
                          filename.endswith(Extensions.Audio.value)
                          ][0]
            post_clips.append(create_video(image_file=post_image, audio_path=audio_path))

        # convert comment to images
        counter = 0
        for comment in comments:
            comment_text = image_gen.generate_image(text=comment.body,
                                     image_type=ImageTypes.Comment,
                                     output_dir=POST_OUTPUT,
                                     output_file_name=COMMENT_NAME.format(post_id=post.id, counter=str(counter)))
            # generate voice for comments
            page = 1
            for text in comment_text:
                text_to_speech(text, POST_AUDIO+COMMENT_NAME.format(
                    post_id=post.id,
                    counter=str(counter))+str(page)+Extensions.Audio.value)
                page += 1




###########
        # convert comment images to videos
            comment_clips = []

            comment_images = [os.path.abspath(POST_OUTPUT + filename)
                              for filename in os.listdir(POST_OUTPUT)
                              if filename.startswith(COMMENT_NAME.format(post_id=post.id, counter=str(counter)))
                           ]
            for comment_image in comment_images:
                audio_path = [os.path.abspath(POST_AUDIO+filename)
                       for filename in os.listdir(POST_AUDIO)
                       if filename.startswith('.'.join(os.path.basename(comment_image).split('.')[0:-1])) and
                              filename.endswith(Extensions.Audio.value)
                       ][0]

                comment_clips.append(create_video(
                    image_file=comment_image,
                    audio_path=audio_path))
            # merge the videos
            merged_clip = append_video_clips(*post_clips, *comment_clips)

            # merge background and post video
            result_clip = merge_video_clips(bg_clip, merged_clip)

            output_path = OUTPUT_FOLDER+f'post_{post.id}_{counter}.mp4'
            export_video(result_clip, output_path)
            print(f'video exported at -> {output_path}')
            counter += 1
        print('starting cleaning up ....')
        # cleaning up temp data
        empty_folder(POST_OUTPUT)
        empty_folder(POST_AUDIO)
        print(f'ended {post.id}')
        print('clean up done')


    except Exception as e:
        print(e)
        print(print_exc())


## delete from DB on the basis f order of insertion
#  delete from posts where id  == (select id from (select *, row_number() OVER (
#   PARTITION BY 1
#   ORDER BY 1 DESC
# ) as row_no from posts) where row_no =13);
