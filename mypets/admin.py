from django.contrib import admin

from .models import *

for model in [Author, Publisher, Genre, Book, Review, OrderHistory, Order, Cart, UserFavorite]:
    admin.site.register(model)
