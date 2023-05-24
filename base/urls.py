from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'), 
    path('room/<str:pk>/',views.room,name='room'),
    path('create-room/',views.createRoom,name='create-room'),
    path('update-room/<str:pk>/',views.updateRoom,name='update-room'),
    path('delete-room/<str:pk>/',views.deleteRoom,name='delete-room'),
    path('login/',views.Loginview,name='login'),
    path('logout/',views.Logoutview,name='logout'),
    path('register/',views.Register,name='register'),
    path('delete-message/<str:pk>/',views.deleteMessage,name='delete-message'),
    path('room-profile/<str:pk>/',views.room_profile,name='room-profile'),
    path('update-user/',views.updateUser,name='update-user')
]