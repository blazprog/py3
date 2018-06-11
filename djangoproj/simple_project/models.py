from django.db import models
from rest_framework import serializers

class Book(models.Model):
    author = models.CharField(max_length=120)
    title = models.CharField(max_length=120)
    year_published = models.IntegerField(default=2015)


class BookSerializer(serializer.ModelSerializer):
    class Meta:
        model = Book
        fields = (id, author, title, year_published)

        
def booksList():
    b1 = Book(id = 1, author = 'Franz Kafka',
              title = 'Proces',
              year_published = 1936)
    

    b2 = Book(id = 2, author = 'Josip Jurcic',
              title = 'Deseti brat',
              year_published = 1853)

    b3 = Book(id = 3, author = 'Lev Tolstoj',
              title = 'Vojna in mir',
              year_published = 1874)


    return [b1, b2, b3]
