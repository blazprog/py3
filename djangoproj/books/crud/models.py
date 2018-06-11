from django.db import models

class Book(models.Model):
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=120)
    releaseDate = models.DateField()
    keywords = models.CharField(max_length=120)

    def __str__(self):
        return '{} : {}'.format(self.author, self.title)
