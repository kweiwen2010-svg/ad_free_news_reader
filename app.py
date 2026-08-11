import streamlit as st
from newspaper import Article
import requests
from bs4 import BeautifulSoup

# 設定頁面配置
st.set_page_config(
    page_title="無廣告新聞閱讀器",
    page_icon="📰",
    layout="centered"
)

st.markdown("""
    <h1 style='text-align: center;'>📰 無廣告新聞閱讀器</h1>
    <p style='text-align: center; color: #888;'>貼上充滿廣告的新聞網址，一鍵還你乾淨的純文字閱讀體驗！</p>
""", unsafe_allow_html=True)

# 支援透過網址參數自動帶入 (例如 ?url=...)
query_params = st.query_params
default_url = query_params.get("url", "")

# 輸入框
news_url = st.text_input("請輸入新聞網址：", value=default_url)

# 模擬真實瀏覽器的 User-Agent，避免被網站阻擋或逾時
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7'
}

if news_url:
    with st.spinner('正在為您清除廣告並擷取文章...'):
        try:
            # 建立 Article 物件，帶入自訂 Headers 與拉長逾時時間
            article = Article(news_url, language='zh')
            
            # 使用 requests 先抓取內容並帶入 headers，解決 Read timed out 與反爬蟲問題
            response = requests.get(news_url, headers=HEADERS, timeout=15)
            response.raise_for_status()
            
            article.download(input_html=response.text)
            article.parse()
            
            title = article.title
            text = article.text
            publish_date = article.publish_date
            authors = article.authors

            # 備援機制：如果 newspaper 抓出來的內文太短（可能被誤判切斷），改用 BeautifulSoup 把所有 <p> 段落補回來
            if not text or len(text.strip()) < 100:
                soup = BeautifulSoup(response.text, 'html.parser')
                paragraphs = soup.find_all('p')
                fallback_text = "\n\n".join([p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 10])
                if len(fallback_text) > len(text):
                    text = fallback_text

            if title or text:
                st.success("解析成功！")
                st.markdown(f"## {title}")
                
                # 顯示來源與作者資訊
                meta_info = f"來源網站：{news_url.split('/')[2]}"
                if authors:
                    meta_info += f" | 作者：{', '.join(authors)}"
                if publish_date:
                    meta_info += f" | 發布日期：{publish_date}"
                st.caption(meta_info)
                
                st.markdown("---")
                
                # 顯示淨化後的內文（保留段落排版）
                for paragraph in text.split('\n'):
                    if paragraph.strip():
                        st.write(paragraph.strip())
            else:
                st.warning("無法有效解析此網址的內文，可能是該網站結構特殊。")

        except Exception as e:
            st.error(f"發生錯誤：{e}")
