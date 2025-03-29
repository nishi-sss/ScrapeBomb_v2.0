import streamlit as st
import pandas as pd
from scraper.main import scrape_jobs

st.title("ScrapeBomb 🍋 v2.0")
st.markdown("レモンをポチると、求人サイトを🍋がスクレイピングします。")

# URL入力
url = st.text_input("🔗 求人検索URL（例：https://求人ボックス.com/〜）")

# 除外ワード入力
raw_keywords = st.text_input("🧹 除外ワード（カンマ区切り・全角入力OK・カンマは半角で）", value="人材,派遣")
exclude_keywords = [kw.strip() for kw in raw_keywords.replace("　", " ").split(",") if kw.strip()]

if st.button("🍋 レモンを絞る！") and url:
    with st.spinner("レモン絞り中..."):
        df = scrape_jobs(url, exclude_keywords)
        st.success("🍋 レモン絞り完了！データ取得しました。")
        st.dataframe(df)

        # ダウンロード
        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("📥 CSVをダウンロード", data=csv, file_name="job_list.csv", mime="text/csv")

