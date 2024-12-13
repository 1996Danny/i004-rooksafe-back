from django.urls import path
from . import views

urlpatterns = [
    path('fetch-quotes', views.fetch_quotes, name='fetch_quotes'),
    path('fetch-historical-data', views.fetch_historical_data, name='fetch_historical_data'),
    path('get-symbols', views.get_symbols, name='get_symbols'),
]
