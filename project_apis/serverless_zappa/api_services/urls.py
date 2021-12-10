from django.urls import path
from .views import TextBlobView, VaderView, ArticleData

urlpatterns = [
    path('textblob/', TextBlobView.as_view(), name="textblob"),
    path('vader/', VaderView.as_view(), name="vader"),
    path('article/', ArticleData.as_view(), name="article"),
]
