from django.conf.urls.static import static
from django.urls import path

from MyPetPetProject import settings
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book/<int:book_id>/', views.book_details, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout', views.checkout, name='checkout')
]
