from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .jlyrics import get_lyrics

# Create your views here.
def mysite(req):
    context = {}
    return render(req, 'lyrics/mysite.html', context)



def findLyrics(req):
    inputInfo = str(req.POST['inputValue'])
    keywords = get_lyrics(inputInfo)
    
    keyword = "".join(keywords)
    
    context = {
        'keyword' : keyword
    }
    return render(req, 'lyrics/findLyrics.html', context)