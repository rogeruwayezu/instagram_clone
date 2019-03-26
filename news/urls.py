from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^$', views.welcome, name='Home'),
    # url(r'^archives/(\d{4}-\d{2}-\d{2})/$',
    #     views.past_days_news,
    #     name='pastNews'),
    url(r'^post/', views.new_post, name='post_image'),
    url(r'^profile/', views.create_profile, name='profileView'),
    url(r'^different/profile/(\d+)', views.different_profile, name='differentProfile'),
    url(r'^follow/(\d+)$', views.follow, name='follow'),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
