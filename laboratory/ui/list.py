import streamlit as st
import requests
from io import BytesIO

# Streamlitアプリのタイトルを設定
st.title("エンドポイントから動画を再生")

# エンドポイントのURLから動画ファイルを取得する関数
def get_video_from_endpoint(endpoint_url):
    try:
        response = requests.get(endpoint_url)
        if response.status_code == 200:
            video_data = response.content
            return video_data
        else:
            st.error(f"エラー：エンドポイントから動画を取得できませんでした (HTTPステータスコード: {response.status_code})")
            return None
    except Exception as e:
        st.error(f"エラー：{e}")
        return None

# エンドポイントから動画データを取得
video_data = get_video_from_endpoint("https://example.com/api/video")  # ここを実際のエンドポイントのURLに置き換えてください

# 動画データが取得できた場合、再生
if video_data:
    st.video(BytesIO(video_data), format="video/mp4")
