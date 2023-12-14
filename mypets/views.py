from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .forms import RegisterForm, LoginForm
from .models import Book, Author, CartItem


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()

    # Books in stock (status = 'a')
    num_books_available = Book.objects.filter(stock_quantity__gt=0).count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'title': 'Книжное Королевство | Книжный интернет-магазин',
        'num_books': num_books,
        'num_books_available': num_books_available,
        'num_authors': num_authors,
        'books': Book.objects.all(),
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)
            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True
        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт создан для {username}')

            return redirect(to='/profile')

        return render(request, self.template_name, {'form': form})


def dispatch(self, request, *args, **kwargs):
    # will redirect to the home page if a user tries to access the register page while logged in
    if request.user.is_authenticated:
        return redirect(to='/profile')

    # else process dispatch as it otherwise normally would
    return super(RegisterView, self).dispatch(request, *args, **kwargs)


@login_required
def profile(request):
    return render(request, 'profile.html')


def book_details(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        messages.success(request, f'{book.title} added to your cart.')
        return redirect('cart:add_to_cart', book_id=book.id)

    context = {
        'title': 'Корзина | Книжный интернет-магазин',
        'book': book,
    }

    return render(request, 'book_detail.html', context)


def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    cart_items_count = cart_items.count()
    total_price = sum(item.quantity * item.book.price for item in cart_items)

    context = {
        'title': 'Корзина | Книжный интернет-магазин',
        'cart_items': cart_items,
        'cart_items_count': cart_items_count,
        'total_price': total_price,
        'delivery_cost': 100,
    }

    return render(request, 'cart.html', context)


def add_to_cart(request, book_id):
    book = Book.objects.get(pk=book_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, book=book)

    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('view_cart')


def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(pk=cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('view_cart')


def checkout(request):
    return HttpResponseRedirect('/')
