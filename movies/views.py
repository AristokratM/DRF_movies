from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie, Review
from .serializers import MovieListSerializer, MovieDetailSerializer, ReviewCreateSerializer, ReviewSerializer


class MovieListView(APIView):
    """Вивід списку фільмів"""

    def get(self, request):
        movies = Movie.objects.filter(draft=False)
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
