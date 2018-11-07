from django.urls import path
from django.conf.urls import include
from main_app import views


urlpatterns = [
        path('index/<page_number>', views.IndexView.as_view(), name='index'),
        path('', views.redirect_to_index),
        path('thread/<int:pk>', views.ThreadView.as_view(), name='thread'),
        path('create_thread', views.CreateThreadView.as_view(), name='create_thread'),
        path('profile', views.ProfileView.as_view(), name='profile'),
        path('register', views.ForumUserFormView.as_view(), name='register'),
        path('delete_post/', views.delete_post, name='delete_post'),
        path('delete_thread/<int:pk>', views.delete_thread, name='delete_thread'),
        path('like_and_dislike/', views.like_and_dislike, name='like_and_dislike'),
        path('about/<int:pk>', views.AboutForumUserView.as_view(), name='about')

]
