from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.urls import reverse


class Author(models.Model):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    father_name = models.CharField(max_length=50)
    biography = models.TextField()

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.father_name}'


class Publisher(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    address = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    genres = models.ManyToManyField(Genre, related_name='books')
    description = models.TextField()
    cover_image = models.ImageField()
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    stock_quantity = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=1)

    def average_rating(self) -> float:
        return Review.objects.filter(book=self).aggregate(Avg('rating'))['rating__avg'] or 0

    def __str__(self):
        return f'{self.title} от {self.author}'


class Review(models.Model):
    RATING_VERY_LOW = 1
    RATING_LOW = 2
    RATING_NORMAL = 3
    RATING_HIGH = 4
    RATING_VERY_HIGH = 4

    RATING_CHOICES = (
        (RATING_VERY_LOW, 'Ужасно'),
        (RATING_LOW, 'Плохо'),
        (RATING_NORMAL, 'Нормально'),
        (RATING_HIGH, 'Хорошо'),
        (RATING_VERY_HIGH, 'Отлично'),
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    header = models.CharField(max_length=30)
    text = models.CharField(max_length=200)
    rating = models.PositiveSmallIntegerField(default=RATING_NORMAL, choices=RATING_CHOICES)

    def __str__(self):
        return f'{self.book.title}: {self.rating}'


class OrderHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_history')

    def __str__(self):
        return f'История заказов {self.user}'


class Order(models.Model):
    ORDERED = 'ORDERED'
    COLLECTED = 'COLLECTED'
    SENT = 'SENT'
    SHIPPED = 'SHIPPED'
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'

    STATUS_CHOICES = (
        (ORDERED, 'Заказан'),
        (COLLECTED, 'Собран'),
        (SENT, 'Отправлен'),
        (SHIPPED, 'Доставлен'),
        (COMPLETED, 'Вручён'),
        (CANCELED, 'Отменён'),
    )

    history = models.ForeignKey(OrderHistory, on_delete=models.CASCADE, related_name='orders')
    address = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(default=ORDERED, choices=STATUS_CHOICES, max_length=15)

    def __str__(self):
        return f'Заказ {self.history.user} от {self.date}'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.quantity} x {self.book.title}'

    def get_absolute_url(self):
        return reverse('cart:cart_detail')


class UserFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_products')
    product = models.ManyToManyField(Book)
