import requests
from bs4 import BeautifulSoup as Soup
import re
from furigana.furigana import print_plaintext
import xlrd

def get_lyrics(input_song, input_singer):

    keyword = "J-Lyric "+ input_singer + input_song +" 歌詞"
    url = "https://google.com/search?q="
    google_result = requests.get(url+keyword)
    google_result_page = google_result.content
    google_analysis = Soup(google_result_page, "html.parser")

    get_address = re.compile("http://")
    link = google_analysis.find("a",{"href":get_address})
    get_address_only = link.get("href")
    first_address = re.compile("http://j-lyric.net/\w+/\w+/\w+[.]html")
    get_lyric_page = first_address.search(get_address_only)
    try: 
        lyricPage = get_lyric_page.group()
        lyrics = requests.get(lyricPage)
        lyricsCode = lyrics.content
        lyricsCore = Soup(lyricsCode, "html.parser")

        lyricsFinal = lyricsCore.find("p",{"id":"Lyric"}).get_text(separator="\n")
        lyricsFinal = lyricsFinal.split("\n")   #가사 한줄마다 리스트의 요소로 만든다.

        info_song = lyricsCore.find("div", {"class":"cap"}).text
        info_song = info_song[:-3]  #곡명정보
        yield info_song + "\n"

        info_singer = lyricsCore.find("p", {"class":"sml"}).text    
        info_singer = info_singer[2:]   #가수정보
        yield info_singer + "\n"

        excel_open = xlrd.open_workbook('/home/conansjh20/lyric/words-book.xlsx')
        excel_sheet = excel_open.sheet_by_name('1')

        list_jap = []
        list_kor = [] 

        for a in range(excel_sheet.nrows):
            list_jap.append(excel_sheet.cell_value(a,0))    #일본어 리스트 생성
            list_kor.append(excel_sheet.cell_value(a,1))    #한글 리스트 생성

        list_sub1 = ["ゃ","ゅ","ょ","ャ","ュ","ョ"]          #야유요 리스트
        list_sub2 = ["っ","ッ"]                             #촉음 리스트
        list_sub3 = ["ん","ン"]                             #응 리스트

        for lyric in lyricsFinal:                           #가사 한줄마다 for문으로 반복
            lyric_furi = print_plaintext(lyric)             #후리가나 들어간 가사 한줄
            
            key_word_lists = []
            
            for lyfu in lyric_furi:                         #한줄에서 한자씩 for문으로 반복
                yield lyfu
                key_word_lists.append(lyfu)                 #key_word_lists에 추가

            key_word_list = "".join(key_word_lists)         #리스트를 하나의 string으로 전환 -> 일본어 가사

            key_index = []

            for n in range(0, len(key_word_list)):          #독음작성위한 for문으로 반복
                if key_word_list[n] in list_jap:
                    key_index.append(list_jap.index(key_word_list[n]))
                elif key_word_list[n] in list_sub1:
                    key_index.append(list_jap.index(list_jap[key_index.pop()]+key_word_list[n]))
                elif key_word_list[n] in list_sub2:
                    key_index.append(list_jap.index(list_jap[key_index.pop()]+key_word_list[n]))
                elif key_word_list[n] in list_sub3:
                    key_index.append(list_jap.index(list_jap[key_index.pop()]+key_word_list[n]))

            key_iter = iter(key_index)

            yield "\n"

            for key in key_iter:
                yield list_kor[key]

            yield "\n\n"

        #    reading_sound.append("\n")

        # key_word_lists = ''.join(key_word_lists)    #전체 한글 가사
        # reading_sounds = ''.join(reading_sound)     #전체 독음 가사
    except:
        yield "error!"
