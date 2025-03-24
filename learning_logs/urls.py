from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('topics/', views.topics, name='topics'),
    path('topics/<topic_id>/', views.topic, name='topic'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('new_entry/<topic_id>/', views.new_entry, name='new_entry'),
    path('edit_entry/<entry_id>/', views.edit_entry, name='edit_entry'),
    
    path('public_topics/', views.public_topics, name='public_topics'),
    path('public_topics/<topic_id>/', views.public_topic, name='public_topic'),

    path('x/', views.x, name='x'),
]
