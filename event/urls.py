from django.urls import path

from .views import *

urlpatterns = [
    path('home/', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    path('event/<int:id>/', event_detail, name='event-detail'),
    path('create-event/', create_event, name='create-event'),
    path('edit-event/<int:id>/', edit_event, name='edit-event'),
    path('delete-event/<int:id>/', event_delete, name='event-delete'),
    path('delete-message/<int:id>/', message_delete, name='message-delete'),
    
    path('join-event/<int:id>/', join_event, name='join-event'),
    path('leave-event/<int:id>/', leave_event, name='leave-event'),
    path('follow/<int:id>/', follow_user, name='follow-user'),
    path('unfollow/<int:id>/', un_follow_user, name='unfollow-user'),
    
    path('profile/<str:username>/<int:id>/', profile, name='profile'),
    path('settings/', settings_page, name='settings'),
    
    path('browse-topics/', topics, name='topics'),
    path('activities/', activities, name='activities'),
    
    
]
