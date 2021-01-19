from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Actor, Category, Genre, Movie, MovieShots, RatingStar, Rating, Review
from ckeditor_uploader.widgets import CKEditorUploadingWidget


# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категорії"""
    list_display = ('id', 'name', 'slug')
    list_display_links = ('name',)


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label="Опис", widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


class ReviewInline(admin.StackedInline):
    """Відгуки на сторінці фільму"""
    model = Review
    extra = 1
    readonly_fields = ('name', 'email')


class MovieShotsInline(admin.TabularInline):
    """Кадри на сторінці фільму"""
    model = MovieShots
    extra = 1
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f"<img src={obj.image.url} width=100 height=110/>")

    get_image.short_description = "Кадр"


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Фільми"""
    list_display = ('id', 'title', 'category', 'slug', 'draft', 'get_poster')
    readonly_fields = ('get_poster',)
    list_display_links = ('title',)
    list_filter = ('year', 'draft',)
    search_fields = ('title', 'category__name')
    actions = ["publish", "un_publish"]
    inlines = [MovieShotsInline, ReviewInline, ]
    save_on_top = True
    save_as = True
    list_editable = ('draft',)
    form = MovieAdminForm
    # fields = (('actors', 'directors', 'genres'), )
    fieldsets = (
        (None, {
            "fields": (('title', 'tagline'),)
        }),
        (None, {
            "fields": (('description', 'poster', 'get_poster'),)
        }),
        (None, {
            "fields": (('year', 'world_premiere', 'country'),)
        }),
        ('Actor', {
            "classes": ('collapse',),
            "fields": (('actors', 'directors', 'genres', 'category'),)
        }),
        (None, {
            "fields": (('budget', 'fees_in_usa', 'fees_in_world'),)
        }),
        ("Options", {
            "fields": (('slug', 'draft'),)
        }),
    )

    def publish(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 фільм було опубліковано"
        else:
            message_bit = f"{row_update} фільмів було опубліковано"
        self.message_user(request, message_bit)

    def un_publish(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 фільм було знято з публікації"
        else:
            message_bit = f"{row_update} фільмів було знято з публікації"
        self.message_user(request, message_bit)

    publish.short_description = "Опублікувати"
    publish.allowed_permission = ('change',)

    un_publish.short_description = "Зняти з публікації"
    un_publish.allowed_permission = ('change',)

    def get_poster(self, obj):
        return mark_safe(f"<img src={obj.poster.url} width=50 height=60/>")

    get_poster.short_description = "Постер"


@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    """Відгуки"""
    list_display = ('id', 'name', 'text', 'movie', 'parent')
    readonly_fields = ('name', 'email')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанри"""
    list_display = ('id', 'slug', 'name')
    ordering = ('id',)


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Актори"""
    list_display = ('id', 'name', 'birth_date', 'get_image')
    list_display_links = ('name',)
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f"<img src={obj.image.url} width=50 height=60/>")

    get_image.short_description = "Зображення"


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """Кадри з фільму"""
    list_display = ('id', 'title', 'movie', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f"<img src={obj.image.url} width=50 height=60/>")

    get_image.short_description = "Кадр"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ('id', 'ip', 'star', 'movie')


admin.site.register(RatingStar)

admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movies | Oleh"
