from add_text_to_image import ImageGenerator, ImageTypes
from config import BACKGROUND_VIDEO, POST_AUDIO, POST_TEMPLATE, POST_OUTPUT,COMMENT_TEMPLATE, SUBREDDIT,\
    LIMIT_POST, LIMIT_COMMENT, OUTPUT_FOLDER, Extensions, POST_NAME, COMMENT_NAME
from reddit_facade import get_posts, fetch_comments
from sqllite_facade import Post, add_post
from text_to_voice import text_to_speech
from utils import empty_folder
from video_generator import export_video,create_video,resize_bg_video,merge_video_clips,append_video_clips
import os


image_gen = ImageGenerator(post_template=POST_TEMPLATE, comment_template=COMMENT_TEMPLATE)

# generate background video
bg_clip = resize_bg_video(BACKGROUND_VIDEO)

# fetch post and comments
posts = get_posts(subreddit_name=SUBREDDIT, limit=LIMIT_POST)
for post in posts:

    # save to db
    try:

        add_post(Post(id=post.id, name=post.title, author=post.author.name))
        if len(post.media_embed.keys()) > 0:
            # if media is there then we will use that post.
            continue

        comments = fetch_comments(post, limit=LIMIT_COMMENT)

        # convert post to images
        image_gen.generate_image(text=post.selftext,
                                 image_type=ImageTypes.Post,
                                 output_dir=POST_OUTPUT,
                                 output_file_name=POST_NAME.format(post.id))
        # generate voice for post
        text_to_speech(post.selftext, POST_AUDIO+POST_NAME.format(post.id)+Extensions.Audio.value)
        # convert comment to images
        counter = 0
        for comment in comments:
            image_gen.generate_image(text=comment.body,
                                     image_type=ImageTypes.Comment,
                                     output_dir=POST_OUTPUT,
                                     output_file_name=COMMENT_NAME.format(post.id, str(counter)))
            # generate voice for comments
            text_to_speech(post.selftext, POST_AUDIO+COMMENT_NAME.format(post.id, str(counter))+Extensions.Audio.value)

            counter += 1

        # convert images to videos
        post_images = [POST_OUTPUT+filename for filename in os.listdir(POST_OUTPUT)
                       if filename.startswith(POST_NAME.format(post.id))
                       ]
        post_clip = create_video(image_files=post_images,
                                 audio_path=POST_AUDIO+POST_NAME.format(post.id)+Extensions.Audio.value)
        comment_clips = []
        for comment in comments:
            comment_images = [POST_OUTPUT + filename for filename in os.listdir(POST_OUTPUT)
                           if filename.startswith(COMMENT_NAME.format(post.id, str(counter)))
                           ]
            comment_clips.append(create_video(
                image_files=comment_images,
                audio_path=POST_AUDIO + COMMENT_NAME.format(post.id, str(counter))+Extensions.Audio.value)
            )
        # merge the videos
        merged_clip = append_video_clips(post_clip, *comment_clips)

        # merge background and post video
        result_clip = merge_video_clips(bg_clip, merged_clip)

        output_path = OUTPUT_FOLDER+f'post_{post.id}.mp4'
        export_video(result_clip, output_path)
        print(f'video exported at -> {output_path}')

        print('starting cleaning up ....')
        # cleaning up temp data
        empty_folder(POST_OUTPUT)
        empty_folder(POST_AUDIO)

        print('clean up done')


    except Exception as e:
        print(e)
