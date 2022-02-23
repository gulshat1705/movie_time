from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.generic import View, ListView, DetailView
from django.db.models import Q

from movies.models import Actor, Movie, Genre, Rating
from .forms import ReviewFrom, RatingForm


class GenreYearView:
    """ жанры и года выхода фильма """ 
    def get_genres(self):
        return Genre.objects.all()


    def get_years(self):
        return Movie.objects.filter(draft=False).values('year')  # вывод только года


class MoviesView(GenreYearView, ListView):        # ListView
    """ Вывод списка фильмов """
    model = Movie
    queryset = Movie.objects.filter(draft=False)        # не черновик
    paginate_by = 2 # !!!!!! пока по одному

class MovieDetailView(GenreYearView, DetailView):      #DetailView
    """ Детальное описание фильма """
    model = Movie
    slug_field = "url"          # по какому полю надо будет искать.сравнивает с url


    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()
        return context


class AddReview(View):
    """ оставить отзывы """
    def post(self, request, pk):
        form = ReviewFrom(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid:
            form = form.save(commit=False)
            # ответить отзыву
            if request.POST.get("parent", None):   # будем искать ключ parent это имя нашего поля , если оно, будет выполнится код
                form.parent_id = int(request.POST.get("parent")) 
            form.movie = movie            
            form.save()
        return redirect(movie.get_absolute_url())  # останемня на той же странице


class ActorView(GenreYearView, DetailView):
    """ вывод информации о актере"""  
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = 'first_name'


class FilterMoviesView(GenreYearView, ListView):
    """ фильтр фильмов """
    paginate_by = 1

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) |   #вывод или жанра или года, ','= и
            Q(genres__in=self.request.GET.getlist('year'))
            ).distinct()    #.distinct() убирать повторяющийся элементов
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year"] = ''.join([f"year={x}&" for x in self.request.GET.getlist("year")])
        context["genre"] = ''.join([f"genre={x}&" for x in self.request.GET.getlist("genre")])
        return context


class AddStarRating(View):
    """Добавление рейтинга фильму"""
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class Search(ListView):
    """ SEARCH """
    paginate_by = 3

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get('q')) 

    def get_context_data(self, *args, **kwargs):
        context =  super().get_context_data(*args, **kwargs)  
        context['q'] = f'q={self.request.GET.get("q")}&'
        return context       