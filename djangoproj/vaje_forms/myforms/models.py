from django.db import models
from django.contrib.auth.models import User
from .form_translator import trans_dict



class Language(models.Model):
    language = models.CharField(max_length=3)
    description = models.CharField(max_length=50)

    def __str__(self):
        return self.description

    def __init__(self, *args, **kwargs):
        """
        Object language je v contextu vseh templateov, zato mu dodam property-e
        s prevedenimi stringi
        """
        super().__init__(*args, **kwargs)
        fields = [field for field in trans_dict.keys() if field[1]==self.language]
        for f in fields:
            setattr(self,f[0],trans_dict[f])



class Subject(models.Model):
    language = models.ForeignKey(Language)
    subject = models.CharField(max_length=60)
    group = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.subject


class ExercisesModel(models.Model):
    language = models.ForeignKey(Language)
    subject = models.ForeignKey(Subject)
    name = models.CharField(max_length=60)
    exercise = models.TextField()

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    tutor = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

