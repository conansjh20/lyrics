from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from lyrics.models import Post
from .jlyrics import get_lyrics
from .lotto import lotto

# Create your views here.
def mysite(req):
    context = {}
    return render(req, 'lyrics/mysite.html', context)

def lottopage(req):
    context = {}
    return render(req, 'lyrics/lottopage.html', context)

def lottoresult(req):
    inputLotto = str(req.POST['inputVal'])
    print(inputLotto)
    result_all = lotto(inputLotto)
    this_time = next(result_all)
    this_date = next(result_all)
    win_numbers = next(result_all)
    bonus_number = next(result_all)
    my_numbers = next(result_all)
    my_rank = next(result_all)
    context = {
        'tt' : this_time,
        'td' : this_date,
        'wns' : win_numbers,
        'bon' : bonus_number,
        'mns' : my_numbers,
        'mr' : my_rank,
    }
    return render(req, 'lyrics/lottoresult.html', context)

def findLyrics(req):
    inputInfo = str(req.POST['inputValue'])
    keywords = get_lyrics(inputInfo)
    keyword = "".join(keywords)
    context = {
        'keyword' : keyword
    }
    post = Post.objects.create(singersong=inputInfo)
    post.save()
    return render(req, 'lyrics/findLyrics.html', context)

def inputJ(req):
    context = {}
    return render(req, 'lyrics/inputJ.html', context)

def list(req):
    context = {
        'words' : Post.objects.all()
    }
    return render(req, 'lyrics/list.html', context)