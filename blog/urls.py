from django.urls import path
from blog import views

urlpatterns =[
    path('', views.home, name='home'),
    path('post/new/', views.post_create, name="post-create"),
    path('post/edit/', views.post_edit_form, name="post-edit"),
    path('post/edit-success/', views.post_edit, name="post-edited"),
    path('post/form/', views.post_form, name="post-form"),
    path('post/<str:slug>/', views.post_detail, name='post-detail'),
    path('post/<str:slug>/delete/', views.post_delete, name='post-delete'),
    path('post/<str:slug>/delete/confirm/', views.post_delete_confirm, name="post-delete-confirm"),

    path('my-posts', views.my_posts, name="my-posts"),
]