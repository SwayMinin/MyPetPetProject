from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, Book, Author


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()

    # Available books (status = 'a')
    num_books_available = Book.objects.filter(stock_quantity__gt=0).count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_books_available': num_books_available,
        'num_authors': num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


@login_required(login_url='/login/')
def add_to_cart(request, book_id):
    cart_item = Cart.objects.filter(user=request.user, book=book_id).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        Cart.objects.create(user=request.user, book=book_id)
    messages.success(request, 'Товар добавлен в Вашу корзину.')

    return redirect('cart:cart_detail')


@login_required(login_url='/login/')
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id)

    if cart_item.user == request.user:
        cart_item.delete()
        messages.success(request, 'Предмет удалён из корзины.')

    return redirect('cart:cart_detail')


@login_required(login_url='/login/')
def cart_detail(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.quantity * item.product.price for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'cart/cart_detail.html', context)
