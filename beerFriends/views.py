import statistics

from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from beerFriends.forms.beerForm import BeerForm
from beerFriends.forms.reviewForm import ReviewCreateForm
from .models import Beer, Review


def filter_out_beers_with_less_ratings(beer_list):
    newly_rated = []
    for beer in beer_list:
        ratings = Review.objects.filter(beer=beer)
        if len(ratings) < 3:
            newly_rated.append(beer_list.pop(beer_list.index(beer)))
    return beer_list, newly_rated


def index(request):
    beer_list = Beer.objects.order_by('rating')[::-1]
    beer_ranking_list, newly_rated_beers = filter_out_beers_with_less_ratings(beer_list)
    context = {'beer_ranking_list': beer_ranking_list, 'newly_rated_beer': newly_rated_beers}
    return render(request, 'index.html', context)


def db(request):
    beers = Beer.objects.all()
    return render(request, "db.html", {"beers": beers})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })


def user_view(request, username):
    user = User.objects.filter(username=username).first()
    user_reviews = Review.objects.filter(creator=user.username).order_by('rating')[::-1]
    context = {'user_reviews': user_reviews, 'viewedUser': user}
    return render(request, 'beerFriends/user_detail.html', context)


class BeerCreate(LoginRequiredMixin, CreateView):
    form_class = BeerForm
    template_name = 'beerFriends/beer_form.html'

    def form_valid(self, form):
        beer = form.save(commit=False)
        beer.image = self.request.FILES['image']
        beer.save()
        return HttpResponseRedirect(reverse_lazy('index'))


def get_avg_rating(reviews):
    ratings = []
    for review in reviews:
        ratings.append(review.rating)

    if len(ratings) > 0:
        return statistics.mean(ratings)

    return "Not yet rated"


def beer_rating(beer):
    reviews = Review.objects.filter(beer__id=beer.id)
    return get_avg_rating(reviews)


class BeerDetailView(DetailView):
    model = Beer
    slug_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = Review.objects.filter(beer__id=self.kwargs['pk'])
        context['reviews'] = reviews
        context['now'] = timezone.now()
        rating = get_avg_rating(reviews)
        context['avgRating'] = rating
        context['avgRatingPercentage'] = rating * 10
        return context


class BeerUpdateView(LoginRequiredMixin, UpdateView):
    model = BeerForm
    fields = ['name', 'origin', 'alcoholContent', 'image']
    template_name = 'beerFriends/beer_form.html'

    def form_valid(self, form):
        beer = form.save(commit=False)
        beer.save()
        return HttpResponseRedirect(reverse_lazy('beer-detail', args=[self.kwargs['pk']]))


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    fields = ['rating', 'text']

    def form_valid(self, form):
        review = form.save(commit=False)
        review.save()
        beer = review.beer
        beer.rating = beer_rating(beer)
        beer.save()
        return HttpResponseRedirect(reverse_lazy('beer-detail', args=[beer.id]))


class ReviewCreate(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewCreateForm

    def form_valid(self, form):
        review = form.save(commit=False)
        beer = Beer.objects.filter(id=self.kwargs['pk']).first()
        review.beer = beer
        review.creator = self.request.user
        review.save()
        beer.rating = get_avg_rating(Review.objects.filter(beer__id=self.kwargs['pk']))
        beer.save()

        return HttpResponseRedirect(reverse_lazy('beer-detail', args=[self.kwargs['pk']]))

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ReviewCreate, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs


class UserDetailView(DetailView):
    model = User
    object = User.objects.filter(username="Tylor");
    context_object_name = "dude"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


