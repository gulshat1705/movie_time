
from django.urls import path

from . import viewset


urlpatterns = [
    path('', viewset.MoviesView.as_view()),
    path('filter/', viewset.FilterMoviesView.as_view(), name='filter'),
    path('search/', viewset.Search.as_view(), name='search'),
    path("add-rating/", viewset.AddStarRating.as_view(), name='add_rating'),
    path('<slug:slug>/', viewset.MovieDetailView.as_view(), name="movie_detail"),
    path('review/<int:pk>/', viewset.AddReview.as_view(), name="add_review"),
    path('actor/<slug:slug>/', viewset.ActorView.as_view(), name="actor_detail"),

]
