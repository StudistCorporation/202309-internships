import streamlit as st

# Streamlitアプリのタイトルを設定
st.title("画像アップロードアプリ")

# 画像をアップロードするフォームを作成
uploaded_image = st.file_uploader("画像をアップロードしてください", type=["jpg", "png", "jpeg"])

# フォームから画像がアップロードされた場合
if uploaded_image is not None:
    # 画像を表示
    st.image(uploaded_image, caption="アップロードされた画像", use_column_width=True)
