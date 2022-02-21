from django.db import models
from django.urls import reverse
from datetime import date


class Category(models.Model):
    name = models.CharField('Категория', max_length=100)
    description = models.TextField('Описание', blank=True, null=True)
    url = models.SlugField(max_length=160, unique=True)


    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Категория'  
        verbose_name_plural = 'Категории' 


class Actor(models.Model):
    full_name = models.CharField('Полное имя', max_length=100)
    #last_name = models.CharField('фамилия', max_length=100)
    birth_date = models.DateField('Дата рождения', blank=True, null=True)
    description = models.TextField('Описание', blank=True, null=True)
    image = models.ImageField('Фото', upload_to='actors/', blank=True, null=True)


    def __str__(self):
        return f'{self.full_name}'

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={'slug': f'{self.full_name}'})


    def calculate_age(self):
        today = date.today()

        try: 
            birthday = self.birth_date.replace(year=today.year)
        # raised when birth date is February 29 and the current year is not a leap year
        except ValueError:
            birthday = self.birth_date.replace(year=today.year, day=today.day-1)

        if birthday > today:
            return today.year - self.birth_date.year - 1
        else:
            return today.year - self.birth_date.year


    class Meta:
        verbose_name = 'Актеры и режисеры'
        verbose_name_plural = 'Актеры и режисеры'


class Genre(models.Model):
    name = models.CharField('Название', max_length=100)
    description = models.TextField('Описание', blank=True, null=True)
    url = models.SlugField(max_length=160, unique=True)


    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Movie(models.Model):
    title = models.CharField('Название', max_length=150)
    tagline = models.CharField('Слоган', max_length=150, default='')
    description = models.TextField('Описание', blank=True, null=True)
    poster = models.ImageField('Афиша', upload_to='movies/')
    year = models.PositiveSmallIntegerField('Дата выхода', default='2022')
    country = models.CharField(max_length=150)
    directors = models.ManyToManyField(Actor, related_name='film_director')
    actors = models.ManyToManyField(Actor, related_name='film_actor')
    
    genres = models.ManyToManyField(Genre)
    world_premiere = models.DateField('Мировая премьера', blank=True, null=True )     #default=date.today
    budget = models.PositiveIntegerField('Бюджет', default=0, help_text='Укажите сумму в долларах')
    fees_in_usa = models.PositiveIntegerField('Сборы_в_США', default=0, help_text='Укажите сумму в долларах')
    fees_in_world = models.PositiveIntegerField('Сборы_в_США', default=0, help_text='Укажите сумму в долларах')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField(default=False)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'slug': self.url})


    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class MovieShots(models.Model):
    """ Кадры из фильма """ 

    title = models.CharField('Название', max_length=150)
    description = models.TextField('Описание', blank=True, null=True)
    image = models.ImageField(upload_to = 'movie_shots/')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)  #при удалении фильма все кадры удалятся


    def __str__(self):
        return self.title


    verbose_name = 'Кадры из фильма'
    verbose_name_plural = 'Кадры из фильма'     


class RatingStar(models.Model):
    value = models.PositiveSmallIntegerField('Рейтинг', default=0)


    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = 'Звезда рейтинга'                 
        verbose_name_plural = 'Звезды рейтинга'  
        ordering = ['-value']     # сортировка          


class Rating(models.Model):
    ip = models.CharField('IP адрес', max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.star} - {self.movie}'


    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
            

class Reviews(models.Model):
    """ Отзывы """
    email = models.EmailField()
    name = models.CharField('логин', max_length=100)
    text = models.TextField('Отзыв ', max_length=5000)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.name} - {self.movie}'


    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'