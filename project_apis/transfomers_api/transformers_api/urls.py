from django.urls import path
from .views import AnalysisAPI

urlpatterns = [
   path('', AnalysisAPI.as_view(), name="api_views"),
]
