from django.urls import path
from post import views


urlpatterns = [
    path('<int:id>/', views.post_detail, name='post_detail'),
    path('add/', views.make_post, name='make_post'),
]