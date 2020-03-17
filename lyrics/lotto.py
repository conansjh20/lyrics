import requests
from bs4 import BeautifulSoup
import re

def lotto(numbers):
    get_address = requests.get("https://www.dhlottery.co.kr/common.do?method=main") 
    get_content = get_address.content 
    get_html = BeautifulSoup(get_content, "html.parser") 
    get_time = get_html.find("strong",{"id":"lottoDrwNo"}).text
    get_date = get_html.find("span",{"id":"drwNoDate"}).text
    num_filter = re.compile('drwtNo.*') 
    wn = [] 
    for get_num in get_html.find_all("span",{"id": num_filter}): 
        wn.append(get_num.get_text()) 
    bonus_num = get_html.find("span",{"id":"bnusNo"}).text 
    bn = bonus_num
    wn = list(wn)
    get_mynum = str.split(numbers)

    yield get_time
    yield get_date

    yield wn
    yield bn
    yield get_mynum

    k = 0
    for i in wn:
        if i in get_mynum:
            k = k + 1

    if k == 5:
        if bn in get_mynum:
            yield "2등"
        else:
            yield "3등"
    elif k == 6:
        yield "1등"
    elif k == 4:
        yield "4등"
    elif k == 3:
        yield "5등"
    else:
        yield "꽝"



print(lotto("30 19 23 24 36 39"))