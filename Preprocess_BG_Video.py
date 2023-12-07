from config import BACKGROUND_VIDEO, PREPROCESSED_BACKGROUND_VIDEO
from video_generator import resize_bg_video, export_video

bg_clip = resize_bg_video(BACKGROUND_VIDEO, start=180, end=180+300)
export_video(bg_clip, PREPROCESSED_BACKGROUND_VIDEO)
