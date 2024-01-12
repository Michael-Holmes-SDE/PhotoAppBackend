from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse, FileResponse
from django.forms.models import model_to_dict
from .models import Album, Photo
import json
import os


def sign_up(req):
    if req.method == "POST":
        user = User.objects.create_user(
            username=req.POST.get("email"),
            password=req.POST.get("password"),
            email=req.POST.get("email"),
            first_name=req.POST.get("first_name"),
            last_name=req.POST.get("last_name")
        )
        login(req, user)
        return redirect("/")
    else:
        return render(req, "registration/sign_up.html")

def sign_in(req):
    if req.method == "POST":
        user = authenticate(req, username=req.POST.get("email"), password=req.POST.get("password"))
        if user is not None:
            login(req, user)
            return redirect("/")

        return render(req, "registration/sign_in.html")
    else:
        return render(req, "registration/sign_in.html")

def logout_view(req):
    logout(req)
    return JsonResponse({"success": True })

@login_required
def me(req):
    return JsonResponse({"user": model_to_dict(req.user)})

@login_required
def create_photo(req):
    if req.method == "POST":
        keywords = req.POST.get("keywords")
        photos = req.FILES.getlist("photos")
        for photo in photos:
            newPhoto = Photo(
                image=photo,
                keywords=keywords,
                User=req.user
            )
            newPhoto.save()

        return JsonResponse({"message": "photos added"})
    

    photos = Photo.objects.filter(User=req.user)
    photoData = [{'id': photo.id, 'keyword': photo.keywords} for photo in photos]
    return JsonResponse({'photos': photoData})

@login_required
@require_POST
def delete_photo(req):
    reqPhotos = req.POST.getlist("photos")
    photos = Photo.objects.filter(User=req.user, id__in=reqPhotos)

    try: 
        for photo in photos:
            photoRoute = f'./{photo.image}'
            os.remove(photoRoute)
            photo.delete()

        userAlbums = Album.objects.filter(User=req.user) # Remove albums with no photos in them
        for album in userAlbums:
            if album.photos.count() == 0:
                album.delete()
        return JsonResponse({"success": "Photos deleted successfully"})
    except Exception as e:
        return JsonResponse({"Error": f"Error deleting photos: {str(e)}"})

@login_required
def create_album(req):
    if req.method == "POST":
        body = json.loads(req.body)
        album = Album(
            title=body["title"],
            User=req.user
        )
        saveAlbum = album
        saveAlbum.save()
        photos = Photo.objects.filter(User=req.user, id__in=body["photoIds"])
        saveAlbum.photos.set(photos)
        return JsonResponse({"message": "album created"})
    

    userAlbums = Album.objects.filter(User=req.user)
    albums = []
    for album in userAlbums:
        photos = Photo.objects.filter(album=album, User=req.user)
        photoData = [{'id': photo.id, 'keyword': photo.keywords} for photo in photos]
        albumDict = model_to_dict(album)
        albumDict['photos'] = photoData
        albums.append(albumDict)

    return JsonResponse({"albums": albums})

@login_required
@require_POST
def delete_album(req):
    reqAlbums = req.POST.getlist("albums")
    albums = Album.objects.filter(User=req.user, id__in=reqAlbums)

    try: 
        albums.delete()
        return JsonResponse({"success": "Albums deleted successfully"})
    except Exception as e:
        return JsonResponse({"Error": f"Error deleting albums: {str(e)}"})

@login_required
def get_photo_by_id(req, photoId):
    photo = Photo.objects.get(User=req.user, id=photoId)
    fileName = os.path.basename(photo.image.name)

    file_extension = fileName.split(".")[-1].lower()

    return FileResponse(photo.image, 
                        content_type=f'image/{file_extension}',
                        as_attachment=True, 
                        filename=fileName, 
                        headers={'Content-Disposition':f'inline; filename="{fileName}"'}) 
