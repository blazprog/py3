from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
#from django.http import HttpResponse
from django.views.generic import View, ListView, DetailView, UpdateView, CreateView
from .models import  ExercisesModel, Subject, Language
import exercises.exercise_parser as my_parser


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
            lang="de" #This should newer happen
        language_obj = Language.objects.filter(language = lang)
        subject_id = self.kwargs.get("pk")
        if not subject_id:
            subject_id = 1
        subject_obj = get_object_or_404(Subject, id = subject_id)

        context = super().get_context_data(**kwargs)
        print(language_obj[0].language)
        context["language"] = language_obj[0]
        context["subject"] = subject_obj
        return context

class ExerciseDetailView(DetailView):
    model = ExercisesModel
    context_object_name = "ExerciseModel"
    template_name = "exercises/exercise_detail.html"

class ExerciseCreateView(CreateView):
    model = ExercisesModel
    fields = ["language", "subject", "name", "exercise"]
    template_name = "exercises/exercise_form.html"

    def get_success_url(self, **kwargs):
        print(self.kwargs)
        lang = self.kwargs.get("language")
        subject = self.kwargs.get("subject")
        return reverse("exercise_list",
                       kwargs={"language" : lang,
                               "pk":subject})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lang = self.kwargs.get("language")
        subject = self.kwargs.get("subject")
        context["language"] = Language.objects.filter(language=lang).first()
        context["action"] = reverse("exercise_create",
                                    kwargs = {"language": lang,
                                              "subject": subject})
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
        context["language"] = self.get_object().language
        context["action"] = reverse("exercise_update",
                kwargs = {'pk': self.get_object().id,
                          'language': lang})

        return context

