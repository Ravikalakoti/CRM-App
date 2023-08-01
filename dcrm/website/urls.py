from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('record/<int:pk>', views.customer_record, name='record'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    path('add_record/', views.add_record, name='add_record'),
    path('update_record/<int:pk>', views.update_record, name='update_record'),
    path('blog/', views.blog_post_list, name='blog_post_list'),
    path('blog/<int:pk>/', views.blog_post_detail, name='blog_post_detail'),
    path('blog/add/', views.add_blog_post, name='add_blog_post'),
    path('author_profile/<int:author_id>/', views.author_profile, name='author_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]