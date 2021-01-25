from rest_framework import generics
from django.db import models
from .models import Movie, Review, Actor
from .serializers import MovieListSerializer, MovieDetailSerializer, ReviewCreateSerializer, ReviewSerializer, \
    RatingSerializer, ActorListSerializer, ActorDetailSerializer
from .service import get_client_ip


class MovieListView(generics.ListAPIView):
    """Вивід списку фільмів"""
    serializer_class = MovieListSerializer

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Avg("ratings__star")
        )
        return movies


class MovieDetailView(generics.RetrieveAPIView):
    """Детальна інформація про фільм"""
    serializer_class = MovieDetailSerializer
    queryset = Movie.objects.filter(draft=False)


class ReviewCreateView(generics.CreateAPIView):
    """Додавання відгуку до фільму"""
    serializer_class = ReviewCreateSerializer


class ReviewListView(generics.ListAPIView):
    """Перегляд всіх відгуків"""
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()


class AddStarRatingView(generics.CreateAPIView):
    """Додавання рейтингу до фільму"""
    serializer_class = RatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorListView(generics.ListAPIView):
    """Вивід списку акторів"""
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorDetailView(generics.RetrieveAPIView):
    """Вивід інформації про актора"""
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
