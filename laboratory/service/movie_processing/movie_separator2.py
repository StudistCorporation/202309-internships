import os
import datetime
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


def split_video_segments(transcribed_data):
    """動画セグメントを取得します。"""
    video_segments = []
    current_step = None

    for item in transcribed_data["results"]["items"]:
        if item["type"] == "pronunciation":
            start_time = float(item["start_time"])
            end_time = float(item["end_time"])

            
            if current_step is None: # 新しいセグメントの場合
                current_step = {"start_time": start_time, "end_time": end_time}
            else: #　セグメントがすでに存在する場合
                current_step["end_time"] = end_time

        elif item["type"] == "punctuation" and current_step: # 句読点が見つかった場合
            video_segments.append(current_step)
            current_step = None

    # 最後のセグメントを保存
    if current_step:
        video_segments.append(current_step)

    return video_segments


def split_video_by_steps(input_video_file, output_directory, video_segments, title):
    current_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    for i, step in enumerate(video_segments):
        start_time = step['start_time']
        end_time = step['end_time']

        # 動画を分割して保存
        output_name = f'{title}_manual_step_{i + 1}_{current_datetime}.mp4'
        output_file = os.path.join(output_directory, output_name)
        ffmpeg_extract_subclip(input_video_file, start_time, end_time, targetname=output_file)