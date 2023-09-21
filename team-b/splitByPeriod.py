import subprocess
import json
import os

input_video_path = "./data/Edge.mp4"

with open('./data/transcribe-s3.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

transcript = data["results"]["transcripts"][0]["transcript"]
sentences = transcript.split("。")

start_times = ["0"]
end_times = []

for i in range(len(data["results"]["items"]) - 1):
    if data["results"]["items"][i]["alternatives"][0]["content"] == "。":
        start_times.append(data["results"]["items"][i + 1]["start_time"])
        end_times.append(data["results"]["items"][i - 1]["end_time"])

output_folder = "outputs2"
os.makedirs(output_folder, exist_ok=True)

# 各セグメントを分割して出力
for index, sentence in enumerate(sentences):

    output_filename = os.path.join(output_folder, f"step{index+1}.mp4")
    end_time = end_times[index] if index < len(end_times) else '50'

    # FFmpegコマンドを生成
    ffmpeg_command = [
        "ffmpeg",
        "-i",
        input_video_path,
        "-ss",
        start_times[index],
        "-to",
        end_time,
        "-c:v",
        "copy",
        "-c:a",
        "copy",
        output_filename,
    ]

    subprocess.call(ffmpeg_command)
    print(sentence, start_times[index], end_times[index])