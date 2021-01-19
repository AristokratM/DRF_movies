from rest_framework import serializers
from .models import Movie, Review


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Додавання відгуку"""

    class Meta:
        model = Review
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Вивід відгуків"""

    class Meta:
        model = Review
        fields = ('name', 'text', 'parent')


class MovieListSerializer(serializers.ModelSerializer):
    """Список фільмів"""

    class Meta:
        model = Movie
        fields = ('title', 'tagline', 'category')


class MovieDetailSerializer(serializers.ModelSerializer):
    """Детельна інформація про фільм"""
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    directors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    actors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ('draft',)
