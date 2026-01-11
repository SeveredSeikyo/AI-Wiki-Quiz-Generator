from django.urls import path
from . import views

urlpatterns = [
    path('scrape', views.scrape_wiki, name='scrape_wiki'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('scrapes/', views.get_scrapes, name='get_scrapes'),
    path('scrapes/<int:scrape_id>/', views.get_scrape_detail, name='get_scrape_detail')
]