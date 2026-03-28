from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('author/<str:author_name>/', views.author_profile, name='author_profile'),
    path('category/<slug:slug>/', views.category_view, name='category_view'),
]
