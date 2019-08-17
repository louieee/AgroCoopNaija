from django.urls import path
from post import views


urlpatterns = [
    path('<int:id_>/', views.post_detail, name='post_detail'),
    path('<id_>/add/', views.make_post, name='make_post'),
    path('<int:post_id>/comment/<int:id_>/', views.comment_detail, name='comment_detail'),
    path('<letter>-<int:id_>/likes/?page=<int:page>/', views.who_liked, name='likes'),
    path('<letter>-<int:id_>/dislikes/?page=<int:page>/', views.who_disliked, name='dislikes'),
    path('react/$', views.react, name='react'),
    path('all_posts/?tag=<tag>&page=<int:page>/', views.all_posts, name='all_post'),
    path('<int:id_>/edit', views.edit_post, name='edit_post' ),
    path('delete/', views.delete_post, name='delete_post'),
    path('/attachment/delete/', views.delete_attachment, name="delete_attachment")


]
