import PIL
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import VideoFileClip, TextClip, ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip, clips_array
from moviepy.video.compositing.concatenate import concatenate
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip


def create_video(image_file, audio_path):
    image_clip = ImageClip(image_file)

    audio_clip = AudioFileClip(audio_path)
    final_clip = CompositeVideoClip([image_clip.set_duration(audio_clip.duration)])

    final_clip.audio = audio_clip
    return final_clip
    # final_clip.write_videofile(output_video, codec='libx264', audio_codec='aac',
    #                            fps=60, temp_audiofile='temp_audio.m4a', remove_temp=True,)


def merge_video_clips(clip1, clip2):
    # Load video clips
    # clip1 = VideoFileClip(video_clip1_path)
    # clip2 = VideoFileClip(video_clip2_path)

    duration = min(clip1.duration, clip2.duration)
    clip1 = clip1.subclip(0, duration)
    clip2 = clip2.subclip(0, duration)

    # resizing second clip
    clip2 = clip2.resize(width=clip1.w * 0.95)

    # aligning clip to center
    clip2.pos = lambda t: ((clip1.w - clip2.w) // 2, (clip1.h - clip2.h) // 2)

    # Combine the video clips
    final_clip = CompositeVideoClip([clip1, clip2], use_bgclip=True)

    # Write the merged video to a file
    return final_clip
    # final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac', temp_audiofile='temp_audio.m4a', remove_temp=True)

def append_video_clips(*args):
    # Load video clips
    # clip1 = VideoFileClip(video_clip1_path)
    # clip2 = VideoFileClip(video_clip2_path)

    final_clip = concatenate([*args], method="compose")

    # Write the merged video to a file
    return final_clip
    # final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac', temp_audiofile='temp_audio.m4a', remove_temp=True)

def resize_bg_video(video_clip1_path):
    clip1 = VideoFileClip(video_clip1_path)
    clip1 = clip1.subclip(180, clip1.duration)
    clip1 = clip1.crop(x1=int(clip1.w * 0.3), y1=0, x2=int(clip1.w - (clip1.w * 0.3)), y2=clip1.h - int(clip1.h * 0.3))
    clip1 = clip1.resize(((clip1.h * 9) // 16, clip1.h))
    return clip1
    # clip1.write_videofile(video_clip1_path, codec='libx264', audio_codec='aac', temp_audiofile='temp_audio.m4a',
    #                            remove_temp=True)


def export_video(clip, output_path):

    clip.write_videofile(output_path, codec='libx264', audio_codec='aac', temp_audiofile='temp_audio.m4a',
                          remove_temp=True, fps=60)


if __name__ == "__main__":
    image_file = r'image_output/out.png'
    bg = 'bg.mkv'
    audio = 'temp_audio.mp3'

    output_clips = []
    # create videos
    for i in range(2):
        output_clips.append(create_video(image_file, audio))
    post_clip = append_video_clips(*output_clips)


    # resize bg video
    bg_clip = resize_bg_video(bg)

    result = merge_video_clips(bg_clip, post_clip)

    export_video(result, 'result.mp4')

