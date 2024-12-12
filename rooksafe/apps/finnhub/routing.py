# routing.py
from django.urls import re_path
from .consumers import StockPriceConsumer
from django.urls import path

# websocket_urlpatterns = [
#     re_path(r'ws/trades/(?P<stock_symbol>\w+)/$', StockPriceConsumer.as_asgi()),
# ]
websocket_urlpatterns = [
    path('ws/trades/<str:stock_symbol>/', StockPriceConsumer.as_asgi()),
]