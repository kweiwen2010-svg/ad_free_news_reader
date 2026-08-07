import streamlit as st
from newspaper import Article

# 頁面基本設定
st.set_page_config(
    page_title="無廣告新聞閱讀器",
    page_icon="📰",
    layout="centered"
)

st.title("📰 無廣告新聞閱讀器")

# 自動抓取網址列帶入的 ?url= 參數
query_params = st.query_params
target_url = query_params.get("url", "")

# 顯示輸入框（如果沒有從書籤帶參數進來，就手動輸入）
url = st.text_input("請輸入新聞網址：", value=target_url)

# 判斷：如果網址列本身就帶有 url 參數，或者使用者點了按鈕，就直接執行解析
if target_url or st.button("開始淨化", type="primary"):
    active_url = target_url if target_url else url
    
    if not active_url.strip():
        st.warning("請先輸入有效的網址！")
    else:
        with st.spinner("正在努力抓取並過濾廣告中..."):
            try:
                article = Article(active_url, language='zh')
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
                    st.markdown(f"## {title}")
                    st.caption(f"來源網站：{active_url.split('/')[2]} | 作者：{authors} | 發布日期：{publish_date}")
                    st.divider()
                    st.markdown(text)
                    
            except Exception as e:
                st.error(f"發生錯誤：{str(e)}")
