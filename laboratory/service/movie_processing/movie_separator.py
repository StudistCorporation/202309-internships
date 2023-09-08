
import argparse
import os
import datetime
import json
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


def split_video_segments(transcribed_data):
    """動画セグメントを取得します。"""
    video_segments = []
    current_step = None

    for item in transcribed_data["results"]["items"]:
        if item["type"] == "pronunciation":
            start_time = float(item["start_time"])
            end_time = float(item["end_time"])

            # 新しいセグメントを作成
            if current_step is None:
                current_step = {"start_time": start_time, "end_time": end_time}
            else:
                # セグメントが既に存在する場合、終了時間を更新
                current_step["end_time"] = end_time

        elif item["type"] == "punctuation" and current_step:
            # 句読点が見つかった場合、セグメントを保存
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

def is_json_file(file_path):
    """ファイルがJSONファイルかどうかを確認します。"""
    return file_path.endswith(".json")

def main(transcribe_file, video_file, output_directory, title):
    # JSONファイルを読み込みます
    transcribed_data = json.load(open(transcribe_file, "r", encoding="utf-8"))

    # 動画セグメントを取得（提供されたデータを使用）
    video_segments = split_video_segments(transcribed_data)

    # 動画セグメントを表示
    for i, step in enumerate(video_segments):
        print(f"Step {i + 1}: Start Time: {step['start_time']}, End Time: {step['end_time']}")

    split_video_by_steps(video_file, output_directory, video_segments, title)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="AWS Transcribeの結果（JSON）を使用して動画を分割します。")
    
    parser.add_argument("-t", "--transcribe", required=True, help="AWS Transcribeの結果（JSON）のファイルパスを指定します。")
    parser.add_argument("-v", "--video", required=True, help="動画ファイルのパスを指定します。")
    parser.add_argument("-o", "--output", required=False, default="output_steps/", help="動画セグメントの出力ディレクトリを指定します。")
    parser.add_argument("-t", "--title", required=False, default="non_title", help="マニュアル名を指定します。")
    
    # 入力動画ファイルと出力ディレクトリを指定します
    transcribe_file = parser.parse_args().transcribe
    video_file = parser.parse_args().video
    output_directory = parser.parse_args().output
    title = parser.parse_args().title
    
    if not is_json_file(video_file):
        print("入力ファイルはJSONファイルである必要があります。")
        exit(1)
        
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        
    main(transcribe_file, video_file, output_directory, title)