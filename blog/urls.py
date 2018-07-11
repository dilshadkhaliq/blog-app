from django.urls import path
from . import views
from .feeds import LatestPostsFeed


app_name = 'blog'

urlpatterns = [
	path('', views.post_list, name='post_list'),
	path('tag/<slug:tag_slug>', views.post_list, name='post_list_by_tags'),
	path('search', views.post_list, name='search_post'),
	path('<int:year>/<int:month>/<int:day>/<slug:post>', views.post_detail, name='post_detail'),
	path('feed', LatestPostsFeed(), name='post_feed'),
	path('share/<int:id>', views.share_email, name='share_post'),
]
