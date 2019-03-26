# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Profile, Image, Follow
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
import datetime as dt
from .forms import ImagePostForm, ProfileForm
from .email import send_welcome_email
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


def welcome(request):
    ''' welcome'''
    # images = Image.objects.all()
    current_user = request.user
    profiles = Profile.get_profiles

    following = Follow.get_following(current_user.id)

    images = []
    for followed in following:
        # get profile id for each and use it to find user id
        profiles = Profile.objects.filter(id=followed.followee.id)
        for profile in profiles:
            post = Image.objects.filter(user=profile.user)

            for image in post:
                images.append(image)

    # print(images)
    # return render(request, 'all-news/home.html', {"profiles": profiles})
    return render(request, 'all-news/home.html', {"images": images, "following": following, "user": current_user, "profiles": profiles})


# def new_post(request):
#     '''
#     View function to display a form for creating a post to a logged in authenticated user
#     '''
#     current_user = request.user

#     if request.method == 'POST':

#         form = PostForm(request.POST, request.FILES)

#         if form.is_valid():
#             image = form.cleaned_data['image']
#             image_name = form.cleaned_data['image_name']
#             image_caption = form.cleaned_data['image_caption']
#             post_image = Image(
#                 image=image, image_name=image_name, image_caption=image_caption, user=current_user)
#             post_image.save()
#             HttpResponseRedirect('Home')
#     else:
#         form = PostForm()
#     return render(request, 'all-news/new-post.html', {"imageForm": form})


def new_post(request):
    '''
    View function to display a form for creating a post to a logged in authenticated user
    '''
    current_user = request.user

    if request.method == 'POST':

        form = ImagePostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = current_user
            post.save()
            return redirect('Home')
    else:
        form = ImagePostForm()
    return render(request, 'all-news/new-post.html', {"form": form})

# def search_results(request):

#     if 'article' in request.GET and request.GET["article"]:
#         search_term = request.GET.get("article")
#         searched_articles = Article.search_by_title(search_term)
#         message = "{search_term}"

#         return render(request, 'all-news/search.html', {
#             "message": message,
#             "articles": searched_articles
#         })

#     else:
#         message = "You haven't searched for any term"
#         return render(request, 'all-news/search.html', {"message": message})


@login_required(login_url='/accounts/login')
def create_profile(request):
    '''
    View function to create and update the profile of the user
    '''
    current_user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            new_profile = form.save(commit=False)
            new_profile.user = current_user
            new_profile.save()
            # print(new_profile.fields.profile_picture)
            return redirect('Home')
    else:
        form = ProfileForm()
    return render(request, 'all-news/profile.html', {"form": form})


@login_required(login_url='/accounts/login')
def different_profile(request, profile_id):
    '''
    View function to display a profile information of other users
    '''
    current_user = request.user

    try:

        profile = Profile.objects.filter(id=profile_id)

        follow_profile = Profile.objects.get(id=profile_id)

        check_if_following = Follow.objects.filter(user=current_user, follower=follow_profile).count()

        images = Image.objects.all().filter(user_id=profile_id)
        images_number = images.count()

        title = f'{request.user.username}\'s'

    except ObjectDoesNotExist:
        raise Http404()

    return render(request, 'all-news/different-profile.html', {"title": title, "images_number": images_number, "current_user": current_user, "profile": profile, "images": images, "check_if_following": check_if_following})



@login_required(login_url='/accounts/login')
def follow(request, id):
    '''
    View function add frofiles of other users to your timeline
    '''
    current_user = request.user

    follow_profile = Profile.objects.get(id=id)

    check_if_following = Follow.objects.filter(
        user=current_user, follower=follow_profile).count()

    if check_if_following == 0:

        following = Follow(user=current_user, followee=follow_profile, follower=current_user.profile)
        following.save()
    else:
        pass

    return redirect(welcome)