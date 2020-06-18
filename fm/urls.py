from django.urls import path
from .views import *

urlpatterns = [
    path('', main_page, name='main_page'),
    path('delete/', delete_thing.as_view(), name='delete_thing'),
    path('change/', change_thing.as_view(), name='change_thing'),
    path('move/', move_thing.as_view(), name='move_thing'),
    path('copy/', copy_thing.as_view(), name='copy_thing'),
    path('create_dir/', create_dir.as_view(), name='create_dir'),
    path('create_file/', create_file.as_view(), name='create_file'),
    path('<str:slug>/', click_thing.as_view(), name='click_thing'),
]