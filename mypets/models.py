from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.urls import reverse


class Author(models.Model):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    father_name = models.CharField(max_length=50)
    biography = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.last_name} {self.first_name[0]}.{self.father_name[0]}.'


class Publisher(models.Model):
    name = models.CharField(max_length=150, unique=True)
    address = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    genres = models.ManyToManyField(Genre, related_name='books', blank=True)
    description = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to="uploads/", null=True, blank=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    sold_number = models.IntegerField(default=0)
    stock_quantity = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['-sold_number']

    def average_rating(self) -> float:
        return Review.objects.filter(book=self).aggregate(Avg('rating'))['rating__avg'] or 0

    def __str__(self):
        return f'"{self.title}" от {self.author}'


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
    ORD = 'ORDERED'
    COLL = 'COLLECTED'
    SENT = 'SENT'
    SHIP = 'SHIPPED'
    COMPL = 'COMPLETED'
    CANCL = 'CANCELED'

    STATUS_CHOICES = (
        (ORD, 'Заказан'),
        (COLL, 'Собран'),
        (SENT, 'Отправлен'),
        (SHIP, 'Доставлен'),
        (COMPL, 'Вручён'),
        (CANCL, 'Отменён'),
    )

    history = models.ForeignKey(OrderHistory, on_delete=models.CASCADE, related_name='orders')
    address = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(default=ORD, choices=STATUS_CHOICES, max_length=15)

    def __str__(self):
        return f'Заказ {self.history.user} от {self.date}'


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.book.title}'

    def get_absolute_url(self):
        return reverse('cart:cart_detail')


class UserFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_products')
    product = models.ManyToManyField(Book)
