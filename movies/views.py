from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie
from .serializers import MovieListSerializer, MovieDetailSerializer


class MovieListView(APIView):
    """Вивід списку фільмів"""

    def get(self, request):
        movies = Movie.objects.filter(draft=False)
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)


class MovieDetailView(APIView):
    """Детальна інформація про фільм"""

    def get(self, request, *args, **kwargs):
        movie = Movie.objects.get(id=kwargs['pk'], draft=False)
        serializers = MovieDetailSerializer(movie)
        return Response(serializers.data)
