from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

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
        'num_books': num_books,
        'num_books_available': num_books_available,
        'num_authors': num_authors,
        'books': Book.objects.all(),
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def book_details(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        messages.success(request, f'{book.title} added to your cart.')
        return redirect('cart:add_to_cart', book_id=book.id)

    context = {
        'book': book,
    }

    return render(request, 'book_detail.html', context)


def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    cart_items_count = cart_items.count()
    total_price = sum(item.quantity * item.book.price for item in cart_items)

    context = {
        'cart_items': cart_items,
        'cart_items_count': cart_items_count,
        'total_price': total_price,
    }

    return render(request, 'cart.html', context)


def add_to_cart(request, book_id):
    book = Book.objects.get(pk=book_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, book=book)
    cart_item = CartItem.objects.filter(user=request.user, book=book_id).first()

    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('view_cart')


def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(pk=cart_item_id)
    cart_item.delete()
    return redirect('view_cart')


def checkout(request):
    return HttpResponseRedirect('/')
