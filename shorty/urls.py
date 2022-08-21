from django.contrib import admin
from django.urls import path

from shortener.views import root, UrlView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', UrlView.as_view(), name='index'),
    path('index/', UrlView.as_view(), name='index'),
    path('<str:url_hash>/', root, name='root'),
]
