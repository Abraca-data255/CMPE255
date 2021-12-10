from django.urls import path, include
from .views import index, search_results

urlpatterns = [
    path('', index, name="index"),
    path('results/', search_results, name="search"),
]
