from bs4 import BeautifulSoup
from urllib import parse
from collections import OrderedDict #중복제거용
import requests
import os
import telegrambot_1

token = '5857904437:AAFZWE3xOCNEhPikSuisK3qgXP3s8Io6Fo8'

def site_on() :
    search = parse.urlparse('https://search.naver.com/search.naver?where=news&sm=tab_jum&query=부동산') #복잡한 글자였던걸 한글로 변경함
    query = parse.parse_qs(search.query)
    S_query = parse.urlencode(query, encoding='euc-kr', doseq=True) #인코딩값을 바꿔야될수도있음
    url ='https://search.naver.com/search.naver?{}'.format(S_query)
    #원래는  "https://www.boannews.com/search/news_list.asp?search=title&find=취약점 이것을
    #"https://www.boannews.com/search/news_list.asp?{}".format(S_query) 이렇게 바꿔서 넣는것이었음
    Article_Crawll(url)

def Article_Crawll(url) :
    news_link = []
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a', href = True) :
        notice_link = link['href']
        if 'media/view.asp?idx=' in notice_link : #뉴스의 제목 html을 뒤져봤을때 a href= 으로 되어있는 부분이다
            news_link.append(notice_link)
    news_link = list(OrderedDict.fromkeys(news_link)) #중복제거
    Compare(news_link)

def Compare(news_link) :
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    temp = []
    cnt = 0
    with open(os.path.join(BASE_DIR, 'compare.txt'),'r') as f_read :
        before = f_read.readlines()
        before = [line.rstrip() for line in before]

        f_read.close()
        for i in news_link  :
            if i not in before  :
                temp.append(i)
                cnt +=1
                with open(os.path.join(BASE_DIR, 'compare.txt'),'a') as f_write :
                    f_write.write(i+'\n')
                    f_write.close()

        if cnt > 0 :
            Maintext_Crawll(temp,cnt)

def Maintext_Crawll(temp, cnt) :
    bot = telegram.Bot(token = token)
    chat_id = bot.getUpdates()[-1].message.chat.id
    NEW = '[+] 금일의 부동산뉴스는 {}개입니다'.format(cnt)
    bot.sendMessage(chat_id= chat_id, text = NEW)
    for n in temp :
        Main_url = "https://www.naver.com{}".format(n.strip()) #원래는 https://boannews.com{}이었음
        bot.sendMessage(chat_id=chat_id, text = Main_url)
        #본문메시지나 사진 기사제목 글까지 크롤링 해야된다면 이걸쓰면된다 아니면 필요없다 
        response = requests.get(Main_url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find_all("div", {'id' : "news_title02"})
        contents = soup.find_all("div", {'id' : "news_content"})
        date = soup.find_all("div", {'id' : "news_util01"})
        photos = soup.find_all("div", {'class' : "news_image"})
        for n in contents :
            text = n.text.strip()

if __name__ == "main" :
    site_on()


