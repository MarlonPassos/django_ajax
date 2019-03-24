from django.db import models

# Create your models here.

class Book(models.Model):
    BOOK_TYPES = (
        ('hardcover', 'Hardcover'),
        ('Paperback', 'Paperback'),
        ('ebook', 'E-book'),
    )

    title = models.CharField(max_length=50)
    publication_date = models.DateField(null=True)
    author = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    pages = models.IntegerField(blank=True, null=True)
    btype = models.CharField(max_length=15, choices=BOOK_TYPES)
    body = models.TextField()

    def __str__(self):
        return self.title