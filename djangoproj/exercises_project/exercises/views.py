from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
#from django.http import HttpResponse
from django.views.generic import View, ListView, DetailView, UpdateView, CreateView
from .models import  ExercisesModel, Subject, Language
import exercises.exercise_parser as my_parser
from .form_translator import add_translated_strings
from .forms import UserForm, SubjectForm

class SelectLanguageView(ListView):
    model = Language
    context_object_name = "languages"
    template_name = "exercises/select_language.html"

class SampleFormView(View):
    def get(selfself, request):
        return render(request,"exercises/form.html")

class ExerciseSolveView(View):
    def get(self, request, pk, language): #pk parameter defined in url
        exercise = get_object_or_404(ExercisesModel,pk=pk)
        context_dict = {}
        context_dict["exercise_name"] = exercise.name
        context_dict["exercise_id"] = exercise.id
        context_dict["language"] = exercise.language
        listDisplay, listCheck = my_parser.parse(exercise.exercise.strip())
        context_dict["exercise_parts"] = listDisplay
        context_dict["action"] = reverse("exercise_solve",
                kwargs = {'pk': exercise.id, 'language': language})

        add_translated_strings(context_dict,
                               "exercise_solve.html",
                               exercise.language.language,
                               "Check")
        return render(request,"exercises/exercise_solve.html", context_dict)

    def post(self, request, pk,  *args, **kwargs):
        exercise = get_object_or_404(ExercisesModel,pk=pk)
        listDisplay, listCheck = my_parser.parse(exercise.exercise.strip())
        i=0
        context_dict = {}
        for key in listCheck.keys():
            my_parser.markUserAnswer(key,request.POST[key],listDisplay)
        #Tu bi bilo bolj enostavno v context_dict postaviti exercise object
        context_dict["exercise_id"] = exercise.id
        context_dict["exercise_parts"] = listDisplay
        context_dict["exercise_name"] = exercise.name
        context_dict["language"] = exercise.language
        add_translated_strings(context_dict,
                               "exercise_check.html",
                               exercise.language.language,
                               "Here_are_the_results_of", "Nazaj_na_vajo")
        return render(request,"exercises/exercise_check.html",context_dict)


class ExercisesListView(ListView):
    #model = ExercisesModel
    context_object_name = "exercises"
    template_name = "exercises/exercises_list.html"

    def get_queryset(self):
        subject_id = self.kwargs.get("pk")
        lang = self.kwargs.get("language")
        language_obj = Language.objects.filter(language = lang).first()
        if not subject_id:
            subject_obj = Subject.objects.filter(language=language_obj).first()
        else:
            subject_obj = get_object_or_404(Subject, id = subject_id)

        return ExercisesModel.objects.filter(subject = subject_obj, language = language_obj)

    def get_context_data(self, **kwargs):
        lang = self.kwargs.get("language")
        if not lang:
            lang="ru" #This should newer happen

        language_obj = Language.objects.filter(language = lang)
        subject_id = self.kwargs.get("pk")
        if not subject_id:
            subject_obj = Subject.objects.filter(language=language_obj).first()
        else:
            subject_obj = get_object_or_404(Subject, id = subject_id)

        context = super().get_context_data(**kwargs)
        context["language"] = language_obj[0]
        context["subject"] = subject_obj
        add_translated_strings(context,
                               "exercise_list.html",
                               lang,
                               "Seznam_vaj","Nova_vaja","Nova_tema", "Edit", "Solve")
        return context


class ExerciseDetailView(DetailView):
    model = ExercisesModel
    context_object_name = "ExerciseModel"
    template_name = "exercises/exercise_detail.html"


class ExerciseCreateView(CreateView):
    model = ExercisesModel
    fields = ["language", "subject", "name", "exercise"]
    template_name = "exercises/exercise_form.html"


    def get_initial(self):
        lang = self.kwargs.get("language")
        language = Language.objects.filter(language=lang).first()
        return {
            "language" : language
        }

    def get_success_url(self, **kwargs):
        lang = self.kwargs.get("language")

        subject = self.kwargs.get("subject")
        return reverse("exercise_list",
                       kwargs={"language" : lang,
                               "pk":subject})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lang = self.kwargs.get("language")
        subject = self.kwargs.get("subject")
        context["language"] = Language.objects.filter(language=lang).first() #rabim za base.html
        context["action"] = reverse("exercise_create",
                                    kwargs = {"language": lang,
                                              "subject": subject})
        add_translated_strings(context,
                       "exercise_form.html",
                       lang,
                       "nova_vaja","save")
        return context


class ExerciseUpdateView(UpdateView):
    model = ExercisesModel
    fields = ["language", "subject", "name", "exercise"]
    template_name = "exercises/exercise_form.html"

    def get_success_url(self):
        lang = self.kwargs.get("language")
        subject_id = self.get_object().subject.id
        return reverse("exercise_list",
                       kwargs = {"language" : lang,
                                 "pk": subject_id})  #Po pomoti je subject_id poimenovan pk

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        lang = self.kwargs.get("language")
        subject = self.object.subject.id
        context["language"] = Language.objects.filter(language=lang).first() #rabim za base.html
        context["action"] = reverse("exercise_update",
                                    kwargs = {"language": lang,
                                              "pk": self.object.id})
        add_translated_strings(context,
                       "exercise_form.html",
                       lang,
                       "Create")
        return context

class SubjectCreateView(CreateView):
    model = Subject
    fields = ["language", "subject"]

    template_name = "exercises/subject_form.html"

    def get_initial(self):
        lang = self.kwargs.get("language")
        language = Language.objects.filter(language=lang).first()
        return {
            "language" : language
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lang = self.kwargs.get("language")
        context["language"] = Language.objects.filter(language=lang).first() #rabim za base.html
        context["action"] = reverse("subject_create",
                                    kwargs = {"language": lang})
        add_translated_strings(context,
                       "subject_form.html",
                       lang,
                       "Create","nova_tema")
        return context

    def get_success_url(self):
        lang = self.kwargs.get("language")
        subject = self.object.id
        return reverse("exercise_list",
                       kwargs={"language" : lang,
                               "pk":subject})


#Registration & authentication views
class CreateUser(CreateView):
    form_class = UserForm
    template_name = "exercises/user_form.html"
    fields = ["user", "password", "email"]

    def get_success_url(self):
        return reverse("select_language")

