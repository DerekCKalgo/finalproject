from django.urls import path     
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('showimage', views.showimage),
    path('todatabase', views.store),
]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

