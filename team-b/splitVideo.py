import subprocess
import os

input_video_path = "./data/Edge.mp4"

segments_info = [
    {"start_time": "0", "end_time": "20"},
    {"start_time": "25", "end_time": "35"},
]

output_folder = "outputs1"
os.makedirs(output_folder, exist_ok=True)

# 各セグメントを分割して出力
for index, segment in enumerate(segments_info):
    start_time = segment["start_time"]
    end_time = segment["end_time"]

    output_filename = os.path.join(output_folder, f"step{index+1}.mp4")

    # FFmpegコマンドを生成
    ffmpeg_command = [
        "ffmpeg",
        "-i",
        input_video_path,
        "-ss",
        start_time,
        "-to",
        end_time,
        "-c:v",
        "copy",
        "-c:a",
        "copy",
        output_filename,
    ]

    subprocess.call(ffmpeg_command)