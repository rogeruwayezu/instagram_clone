from django import forms
from .models import Image, Profile


class ImagePostForm(forms.ModelForm):
    '''
    Class to create a form for an authenticated user to create Post
    '''
    class Meta:
        model = Image
        fields = ['image', 'image_name', 'image_caption']

# class PostForm(forms.Form):
#     image = forms.ImageField()
#     image_name = forms.CharField(label='First Name', max_length=30)
#     image_caption = forms.CharField(label='Image caption', max_length=30)


class ProfileForm(forms.ModelForm):
    '''
    classs that creates profile update form
    '''
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio']
