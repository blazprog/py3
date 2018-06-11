from django.db import models

class Language(models.Model):
    language = models.CharField(max_length=3)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description

class Subject(models.Model):
    language = models.ForeignKey(Language)
    subject = models.CharField(max_length=60)

    def __str__(self):
        return self.subject



class ExercisesModel(models.Model):
    language = models.ForeignKey(Language)
    subject = models.ForeignKey(Subject)
    name = models.CharField(max_length=60)
    exercise = models.TextField()

    def __str__(self):
        return self.name

