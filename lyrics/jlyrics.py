import requests
from bs4 import BeautifulSoup as Soup
import re
from googletrans import Translator as tr
from furigana.furigana import print_plaintext
import xlrd

def get_lyrics(inputInfo):

    keyword = "J-Lyric "+ inputInfo +" 歌詞"
    url = "https://google.com/search?q="
    google_result = requests.get(url+keyword)
    google_result_page = google_result.content
    google_analysis = Soup(google_result_page, "html.parser")

    get_address = re.compile("http://")
    link = google_analysis.find("a",{"href":get_address})
    get_address_only = link.get("href")
    first_address = re.compile("http://j-lyric.net/\w+/\w+/\w+[.]html")
    get_lyric_page = first_address.search(get_address_only)
    lyricPage = get_lyric_page.group()
    lyrics = requests.get(lyricPage)
    lyricsCode = lyrics.content
    lyricsCore = Soup(lyricsCode, "html.parser")

    lyricsFinal = lyricsCore.find("p",{"id":"Lyric"}).get_text(separator="\n")
    SingerSong = lyricsCore.find("h1").get_text(separator="\n")
    ly = lyricsFinal.split("\n")
    trans = tr()

    excel_open = xlrd.open_workbook('/home/conansjh20/lyric/words-book.xlsx')
    excel_sheet = excel_open.sheet_by_name('1')

    list_jap = []
    list_kor = [] 

    yield SingerSong
    yield "\n\n"

    for a in range(excel_sheet.nrows):
        list_jap.append(excel_sheet.cell_value(a,0))
        list_kor.append(excel_sheet.cell_value(a,1))

    list_sub1 = ["ゃ","ゅ","ょ","ャ","ュ","ョ"]
    list_sub2 = ["っ","ッ"]
    list_sub3 = ["ん","ン"]
    
    for lyric in ly:
        transLyrics = trans.translate(lyric, dest="ko").text
        
        lyric_furi = print_plaintext(lyric)
        
        key_word_lists = []

        for lyfu in lyric_furi:
            yield lyfu
            key_word_lists.append(lyfu)

        key_word_list = "".join(key_word_lists)

        key_index = []
        
        for n in range(0, len(key_word_list)):

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
            # print(list_kor[key],end="")

        yield "\n" + transLyrics + "\n\n"
