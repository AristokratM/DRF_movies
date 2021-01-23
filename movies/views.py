from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import models
from .models import Movie, Review, Actor
from .serializers import MovieListSerializer, MovieDetailSerializer, ReviewCreateSerializer, ReviewSerializer, \
    RatingSerializer, ActorListSerializer, ActorDetailSerializer
from .service import get_client_ip


class MovieListView(APIView):
    """Вивід списку фільмів"""

    def get(self, request):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(request)))
        ).annotate(
            middle_star=models.Avg("ratings__star")
        )
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)


class MovieDetailView(APIView):
    """Детальна інформація про фільм"""

    def get(self, request, pk):
        movie = Movie.objects.get(id=pk, draft=False)
        serializers = MovieDetailSerializer(movie)
        return Response(serializers.data)


class ReviewCreateView(APIView):
    """Додавання відгуку до фільму"""

    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)


class ReviewListView(APIView):
    """Перегляд всіх відгуків"""

    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class AddStarRatingView(APIView):
    """Додавання рейтингу до фільму"""

    def post(self, request):
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)


class ActorListView(generics.ListAPIView):
    """Вивід списку акторів"""
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorDetailView(generics.RetrieveAPIView):
    """Вивід інформації про актора"""
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
