from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import LoginForm
from .views import profile, RegisterView, CustomLoginView

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='login.html',
                                           authentication_form=LoginForm), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', views.index, name='index'),
    path('book/<int:book_id>/', views.book_details, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout', views.checkout, name='checkout')
]
