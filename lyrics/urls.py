from django.urls import path
from . import views

##urlpatterns는 이름을 바꿔서는 안된다.

urlpatterns = [
    path('', views.mysite, name="mysite"),            # Main
    path('findLyrics/', views.findLyrics, name="findLyrics"),
    path('list/', views.list, name="list"),
    path('inputJ/', views.inputJ, name="inputJ"),
    path('lottopage/', views.lottopage, name="lottopage"),
    path('lottoresult/', views.lottoresult, name="lottoresult"),
]