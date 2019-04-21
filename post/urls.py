from django.urls import path
from post import views


urlpatterns = [
    path('<int:id_>/', views.post_detail, name='post_detail'),
    path('add/', views.make_post, name='make_post'),
    path('<int:post_id>/comment/<int:id_>/', views.comment_detail, name='comment_detail'),
    path('<letter>/likes/<id_>/', views.who_liked, name='likes'),
    path('<letter>/dislikes/<id_>/', views.who_disliked, name='dislikes'),

]
