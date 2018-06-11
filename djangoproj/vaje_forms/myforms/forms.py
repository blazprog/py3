__author__ = 'blazko'
from django import forms
from .models import Subject, ExercisesModel, Language, UserProfile, User


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['language', 'subject',"group"]

class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['language', 'description']



class ChoiceFieldNoValidation(forms.ChoiceField):
    def validate(self, value):
        pass

class ExerciseForm(forms.ModelForm):
    subject_language = forms.ChoiceField()
    class Meta:
        model = ExercisesModel
        fields = ["language","subject_language","name","exercise"]


    def set_subjects(self, subjects):
        """
        Set onlj subjects for choosen language
        :param subjects:
        :return:None
        """
        self.fields["subject_language"].choices = subjects




class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "email", "password")

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ("tutor",)

class LoginForm(forms.Form):
    user = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



