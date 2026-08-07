import streamlit as st
from newspaper import Article

# 頁面基本設定
st.set_page_config(
    page_title="無廣告新聞閱讀器",
    page_icon="📰",
    layout="centered"
)

st.Title("📰 無廣告新聞閱讀器")
st.write("貼上充滿廣告的新聞網址，一鍵還你乾淨的純文字閱讀體驗！")

# 接收網址輸入（支援網址列帶入參數，方便未來做自動化）
query_params = st.query_params
default_url = query_params.get("url", "")

url = st.text_input("請輸入新聞網址：", value=default_url)

if st.button("開始淨化", type="primary"):
    if not url.strip():
        st.warning("請先輸入有效的網址！")
    else:
        with st.spinner("正在努力抓取並過濾廣告中..."):
            try:
                # 使用 newspaper3k 解析新聞
                article = Article(url, language='zh')
                article.download()
                article.parse()
                
                title = article.title
                authors = ", ".join(article.authors) if article.authors else "未知"
                publish_date = str(article.publish_date) if article.publish_date else "未知"
                text = article.text
                
                if not text:
                    st.error("無法有效解析此網頁內容，可能是該網站有嚴格的反爬蟲保護。")
                else:
                    st.success("解析成功！")
                    
                    # 顯示文章資訊
                    st.markdown(f"## {title}")
                    st.caption(f"來源網站：{url.split('/')[2]} | 作者：{authors} | 發布日期：{publish_date}")
                    st.divider()
                    
                    # 顯示乾淨內文
                    st.markdown(text)
                    
            except Exception as e:
                st.error(f"發生錯誤：{str(e)}")
