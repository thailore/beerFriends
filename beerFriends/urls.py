from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from beerFriends.views import *

app_name='beerFriends'
urlpatterns = [
    path("", index, name="index"),
    path("db/", db, name="db"),
    path("admin/", admin.site.urls),
    path("signup/", signup, name='signup'),
    path("change-password/", change_password, name='change_password'),
    path("add/", BeerCreate.as_view(success_url=reverse_lazy('index')), name="add"),
    path("<slug:pk>/edit/", BeerUpdateView.as_view(model=Beer, success_url=reverse_lazy('beer-detail')), name="edit"),
    path("rate/<slug:pk>/edit/", ReviewUpdateView.as_view(model=Review, success_url=reverse_lazy('beer-detail')), name="editReview"),
    path("rate/<slug:pk>/", ReviewCreate.as_view(success_url=reverse_lazy('beer-detail')), name="rate"),
    path('<slug:pk>/', BeerDetailView.as_view(), name='beer-detail'),
    path('user/<slug:username>', user_view, name='user'),
    path('accounts/', include('django.contrib.auth.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
