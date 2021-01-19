from datetime import date

from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Категорії"""
    name = models.CharField("Категорія", max_length=150)
    description = models.TextField("Опис")
    slug = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


class Actor(models.Model):
    """Актори і Режисери"""
    name = models.CharField("Ім'я", max_length=150)
    birth_date = models.DateField("Дата народження")
    description = models.TextField("Опис")
    image = models.ImageField("Зображення", upload_to="actors/")

    def __str__(self):
        return self.name

    def get_age(self):
        return date.today().year - self.birth_date.year

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={'slug': self.name})

    class Meta:
        verbose_name = "Актор"
        verbose_name_plural = "Актори"


class Genre(models.Model):
    """Жанри"""
    name = models.CharField("Назва", max_length=150)
    description = models.TextField()
    slug = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанри"


class Movie(models.Model):
    """Фільми"""
    title = models.CharField("Назва", max_length=150)
    tagline = models.CharField("Гасло", max_length=150, default='')
    description = models.TextField("Опис")
    poster = models.ImageField("Постер", upload_to="movies/")
    year = models.PositiveSmallIntegerField("Рік виходу", default=2021)
    country = models.CharField("Країна", max_length=150)
    directors = models.ManyToManyField(Actor, verbose_name="Режисер", related_name="film_director")
    actors = models.ManyToManyField(Actor, verbose_name="Актор", related_name="film_actor")
    genres = models.ManyToManyField(Genre, verbose_name="Жанр")
    world_premiere = models.DateField("Прем'єра у світі", default=date.today)
    budget = models.PositiveIntegerField("Бюджет", default=0, help_text="Вказати суму у доларах")
    fees_in_usa = models.PositiveIntegerField("Збори в США", default=0, help_text="Вказати суму у доларах")
    fees_in_world = models.PositiveIntegerField("Збори в світі", default=0, help_text="Вказати суму у доларах")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(max_length=150, unique=True)
    draft = models.BooleanField("Чернетка", default=False)

    def __str__(self):
        return self.title

    def get_absolut_url(self):
        return reverse('movie_detail', kwargs={'slug': self.slug})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Фільм"
        verbose_name_plural = "Фільми"


class MovieShots(models.Model):
    """Кадри з фільму"""
    title = models.CharField("Назва", max_length=150)
    description = models.TextField("Опис")
    image = models.ImageField("Зображення", upload_to="movie_shots/")
    movie = models.ForeignKey(Movie, verbose_name="Фільм", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Кадр з фільму"
        verbose_name_plural = "Кадри з фільмів"


class RatingStar(models.Model):
    """Зірка рейтингу"""
    value = models.SmallIntegerField("Значення", default=0)

    def __str__(self):
        return f"{self.value}"

    class Meta:
        verbose_name = "Зірка рейтингу"
        verbose_name_plural = "Зірки рейтингу"
        ordering = ['-value']


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="Зірка")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Фільм")

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Review(models.Model):
    """Відгуки"""
    email = models.EmailField()
    name = models.CharField("Ім'я", max_length=100)
    text = models.TextField("Повідомлення", max_length=5000)
    parent = models.ForeignKey('self', verbose_name="Батько", on_delete=models.SET_NULL, blank=True, null=True)
    movie = models.ForeignKey(Movie, verbose_name="Фільм", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"
