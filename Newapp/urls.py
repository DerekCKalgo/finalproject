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
    path('like/<int:photo_id>', views.like),
    path('comment/<int:photo_id>', views.comment),
    path('logout', views.logout),
    path('ranking', views.ranking),
]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

