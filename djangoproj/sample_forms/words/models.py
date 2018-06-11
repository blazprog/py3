from django.db import models

class Word(models.Model):
    word = models.CharField(max_length=70)
    translation = models.CharField(max_length=70)
    description = models.TextField()
    sample_use = models.TextField()

    def __str__(self):
        return "{0} --> {1}".format(self.word, self.translation)

