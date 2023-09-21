from flask import Flask, request, render_template, redirect, url_for
from dotenv import load_dotenv
import subprocess
import os
import boto3

load_dotenv()

app = Flask(__name__)

# S3の設定
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    # アップロードされたファイルを取得
    video_file = request.files["videoFile"]

    # ファイルの保存先ディレクトリを作成
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    # ファイルを保存
    video_path = os.path.join(upload_dir, "input.mp4")
    video_file.save(video_path)

    # 動画の分割処理（ffmpegを使用）
    segments_info = [
        {"start_time": "0", "end_time": "20"},
        {"start_time": "25", "end_time": "35"},
    ]

    segment_urls = []

    for index, segment in enumerate(segments_info):
        start_time = segment["start_time"]
        end_time = segment["end_time"]

        output_filename = f"output_{start_time}-{end_time}.mp4"
        output_path = os.path.join(upload_dir, output_filename)

        # FFmpegコマンドを生成
        ffmpeg_command = [
            "ffmpeg",
            "-i",
            video_path,
            "-ss",
            start_time,
            "-to",
            end_time,
            "-c:v",
            "copy",
            "-c:a",
            "copy",
            output_path,
        ]

        subprocess.call(ffmpeg_command)

        # S3にアップロード
        s3.upload_file(output_path, "YOUR_S3_BUCKET_NAME", output_filename)

        # 分割した動画のURLを保存
        segment_url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": "YOUR_S3_BUCKET_NAME", "Key": output_filename},
            ExpiresIn=3600,  # URLの有効期限（秒）
        )
        segment_urls.append(segment_url)

    return render_template("index.html", segment_urls=segment_urls)


if __name__ == "__main__":
    app.run(debug=True)
