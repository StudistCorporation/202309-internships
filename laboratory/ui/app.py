import streamlit as st

# サイドバーに表示するページリンクを設定
pages = {
    "ホーム": "home",
    "設定": "settings",
    "情報": "about"
}

# サイドバーにページ選択用のラジオボタンを表示
selected_page = st.sidebar.radio("ページを選択", list(pages.keys()))

# ページごとのコンテンツを表示
if selected_page == "ホーム":
    st.title("ホームページ")
    # ホームページのコンテンツをここに追加
elif selected_page == "設定":
    st.title("設定ページ")
    # 設定ページのコンテンツをここに追加
elif selected_page == "情報":
    st.title("情報ページ")
    # 情報ページのコンテンツをここに追加
