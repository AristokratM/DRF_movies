from django.urls import path, include
from . import views


urlpatterns = [
    path('movies/', views.MovieListView.as_view()),
    path('movie/<int:pk>', views.MovieDetailView.as_view()),
    path('review/', views.ReviewCreateView.as_view()),
    path('reviews/', views.ReviewListView.as_view()),
    path('rating/', views.AddStarRatingView.as_view()),
    path('actors/', views.ActorListView.as_view()),
    path('actor/<int:pk>', views.ActorDetailView.as_view()),


]
