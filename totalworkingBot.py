import requests
from bs4 import BeautifulSoup
import telegram
import asyncio
import time

#================뉴스크롤링 ========================
# 검색 키워드
search_word = '부동산'
#기존에 보냈던걸 담아둘 리스트
old_links = []

def extract_links(old_links=[]) :
    # 해당 url의 html문서를 soup 객체로 저장
    url = f'https://m.search.naver.com/search.naver?where=m_news&sm=mtb_jum&query={search_word}'
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    search_result = soup.select_one('#news_result_list')
    news_list = search_result.select('.bx > .news_wrap > a')
    links = []
    for news in news_list[:5]:
        link = news['href']
        links.append(link)

    new_links = []
    for link in links:
        if link not in old_links:
            new_links.append(link)

    links = []
    for news in news_list[:10]:
        link = news['href']
        links.append([news.get_text(), link])

    new_links = []
    for link in links:
        if link[1] not in old_links:
            new_links.append(link)
    result = ''
    for new_link in new_links:
        result += f'{new_link[0]} : {new_link[1]}' +'\n'

    return result


#================텔레그램봇제어 ========================

contents = extract_links(old_links)


async def main() :
    # 텔레그램 봇 토큰
    my_token = '5909311694:AAEhJcEhFnL7Rw0XLdC-Lb1vnjqDD6angm4'
    chat_id = 93432349
    # 텔레그램 봇 생성
    bot = telegram.Bot(token=my_token)
    await bot.sendMessage(chat_id, text=contents)

while True :
    asyncio.run(main())
    time.sleep(60*60*6)


