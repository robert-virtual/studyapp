


from django.urls import path
from base.views import about, createRoom, deleteRoom, home, logoutUser, register, room, signin, updateRoom


urlpatterns = [
    path('', home,name="home",),
    path('register/', register,name="register"),
    path('signin/', signin,name="signin"),
    path('logout/', logoutUser,name="logout"),
    path('room/<int:id>/', room,name="room"),
    path('create-room/', createRoom,name="create-room"),
    path('update-room/<int:id>', updateRoom,name="update-room"),
    path('delete-room/<int:id>', deleteRoom,name="delete-room"),
    path('about/', about,name="about"),
]

