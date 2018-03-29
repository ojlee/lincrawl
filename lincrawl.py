#-*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os

import telegram

bot = telegram.Bot(token='')
url = 'http://linc.jejunu.ac.kr/info/notice'


chat_id = bot.getUpdates()[-1].message.chat.id

# 파일의 위치
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

req = requests.get(url)
req.encoding = 'utf-8'

html = req.text
soup = BeautifulSoup(html, 'html.parser')

titles = soup.select('body > div > section > div.sub_content > div.conArea > div.boardList > table > tbody > tr > td:nth-of-type(2) > p > a')


latest_title = titles[0].text.strip() # 첫번째 글 자리
second_title = titles[1].text.strip() # 두번째 글 자리
third_title = titles[2].text.strip() # 세번째 글 자리

with open(os.path.join(BASE_DIR, 'latest.txt'), 'r+') as f_read:
    before = f_read.readline()
    f_read.close()
    if before != latest_title:
        # 같은 경우는 에러 없이 넘기고, 다른 경우에만
        bot.sendMessage(chat_id=chat_id, text='새 글!\n\n제목 - '+ latest_title +
                        '\n\n둘째 - ' + second_title + '\n셋째 - ' + third_title
                        +'\n\n' + '\n목록\n'+url)
        with open(os.path.join(BASE_DIR, 'latest.txt'), 'w+') as f_write:
            f_write.write(latest_title)
            f_write.close()