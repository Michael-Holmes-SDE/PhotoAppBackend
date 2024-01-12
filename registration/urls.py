from django.urls import path
from . import views

urlpatterns = [
    path('sign_in/', view=views.sign_in, name="sign in"),
    path('sign_up/', view=views.sign_up, name="sign up"),
    path('logout/', view=views.logout_view, name="logout view"),
    path('me/', view=views.me, name="logged in view"),
    path('albums/', view=views.create_album, name="create album"),
    path('albums/delete/', view=views.delete_album, name="delete album"),
    path('photos/', view=views.create_photo, name="create photo"),
    path('photos/delete/', view=views.delete_photo, name="delete photo"),
    path('photoStorage/<int:photoId>/', view=views.get_photo_by_id, name="get photo by id"),
]
