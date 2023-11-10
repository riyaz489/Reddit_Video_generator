from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import VideoFileClip, TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip, clips_array


def create_video(image_file, voice_text, output_video):
    # Text-to-speech

    # Create a video clip from an image
    image_clip = VideoFileClip(image_file, audio=False)

    # Create a text clip with the voice narration
    audio_clip = AudioFileClip('temp_audio.mp3')
    voice_clip = TextClip(voice_text, fontsize=24, color='white', bg_color='black').set_audio(audio_clip)

    # Combine the image and voice clips
    final_clip = CompositeVideoClip([image_clip.set_duration(voice_clip.duration), voice_clip])

    # Write the video file
    final_clip.write_videofile(output_video, codec='libx264', audio_codec='aac', temp_audiofile='temp_audio.m4a', remove_temp=True)


def merge_video_clips(video_clip1_path, video_clip2_path, output_path):
    # Load video clips
    clip1 = VideoFileClip(video_clip1_path)
    clip2 = VideoFileClip(video_clip2_path)

    # Ensure both clips have the same duration
    duration = min(clip1.duration, clip2.duration)
    clip1 = clip1.subclip(0, duration)
    clip2 = clip2.subclip(0, duration)

    # Combine the video clips side by side
    final_clip = clips_array([[clip1, clip2]])

    # Write the merged video to a file
    final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac', temp_audiofile='temp_audio.m4a', remove_temp=True)


if __name__ == "__main__":
    image_file = 'input_image.jpg'
    voice_text = "Hello, this is a voice narration example for a video with an image."
    output_video = 'output_video.mp4'

    create_video(image_file, voice_text, output_video)