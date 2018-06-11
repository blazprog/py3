__author__ = 'blazko'

from django import forms
from django.forms.formsets import  formset_factory
from django.forms.models import modelformset_factory,inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field,Div,Fieldset,HTML, Button
from crispy_forms.bootstrap import FormActions
from .models import Nakup, NakupIzdelki

class NameForm(forms.Form):
    your_ugly_name = forms.CharField(label="Tvoje ime", max_length=100)

    helper = FormHelper()
    helper.label_class = "col-lg-2"
    helper.field_class = "col-lg-4"
    helper.layout = Layout (
        Fieldset("Zaupaj nam svoje ime","your_name"),
        FormActions(Submit("save", "Save changes")                                       )
        )
    helper.form_tag = False


class ContactMeForm(forms.Form):
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField()

    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
           Fieldset("Pošlji sporočilo","subject",
                    "message",
                    "sender",
                    "cc_myself"),
                   FormActions(Submit("save", "Send"),
                   HTML("""<a role="button" class="btn btn-default"
                        href="{% url "index" %}">Cancel</a>""")
        )
    )


class ArticleForm(forms.Form):
    title = forms.CharField()
    author = forms.CharField()

    #helper = FormHelper()
    #helper.form_tag = False
    #helper.layout = Layout (
    #    Fieldset("",pub_date, title)
    #)


ArticleFormSet = formset_factory(ArticleForm, extra=3)

class ArticleFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = "post"
        self.layout = Layout(Field("pub_date", css_class="table_pub_date"),
                             Field("title", css_class="table_title"))



class NakupForm(forms.ModelForm):
    class Meta:
        model = Nakup
        fields = ["datum_nakupa", "trgovina"]

    helper = FormHelper()
    helper.layout = Layout (
        Fieldset("Podatki o nakupu","trgovina","datum_nakupa")
        )
    helper.form_tag = False



class NakupIzdelkiFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = "post"
        self.form_tag = False
        self.layout = Layout(Field("izdelek", css_class="input-sm izdelek_te", wrapper_class='izdelek_te'),
                             Field("kolicina", css_class="input-sm kolicina_te"),
                             Field("cena", css_class="input-sm cena_te"))


class NakupIzdelkiForm(forms.ModelForm):
    class Meta:
        model = NakupIzdelki
        fields = ["izdelek","kolicina","cena"]

NakupIzdelkiFormset = inlineformset_factory(Nakup,NakupIzdelki, 
        form=NakupIzdelkiForm, extra=4)
