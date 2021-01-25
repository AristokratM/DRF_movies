from rest_framework import serializers
from .models import Movie, Review, Rating, Actor


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Додавання відгуку"""

    class Meta:
        model = Review
        fields = '__all__'


class FilterReviewSerializer(serializers.ListSerializer):
    """Фільтр відгуків, тільки parents"""

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """Вивід рекурсивно children"""

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ActorDetailSerializer(serializers.ModelSerializer):
    """Інформація про одного актора"""

    class Meta:
        model = Actor
        fields = '__all__'


class ActorListSerializer(serializers.ModelSerializer):
    """Вивід списку акторів і режисирів"""

    class Meta:
        model = Actor
        fields = ('id', 'name', 'image',)


class ReviewSerializer(serializers.ModelSerializer):
    """Вивід відгуків"""
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewSerializer
        model = Review
        fields = ('name', 'text', 'children')


class MovieListSerializer(serializers.ModelSerializer):
    """Список фільмів"""
    rating_user = serializers.BooleanField()
    middle_star = serializers.FloatField()

    class Meta:
        model = Movie
        fields = ('id', 'title', 'tagline', 'category', 'rating_user', 'middle_star')


class MovieDetailSerializer(serializers.ModelSerializer):
    """Детельна інформація про фільм"""
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    directors = ActorListSerializer(read_only=True, many=True)
    actors = ActorListSerializer(read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ('draft',)


class RatingSerializer(serializers.ModelSerializer):
    """Додавання рейтингу до користувачів"""

    class Meta:
        model = Rating
        fields = ('star', 'movie',)

    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={'star': validated_data.get('star')}
        )
        return rating
