from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView, UpdateView, CreateView
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SubjectForm,ExerciseForm, UserForm, UserProfileForm, LoginForm, LanguageForm
from .models import Subject, Language, ExercisesModel
import myforms.exercise_parser as my_parser
from django.forms.models import formset_factory

from crispy_forms.layout import Submit

# Create your views here.

#VIEWS FOR NAVIGATION
class GroupedSubjects(View):

    def get(self,request,*args,**kwargs):
        lang = self.kwargs.get("language","ru")
        context_dict = {}
        lang = self.kwargs.get("language","ru")
        language = Language.objects.filter(language=lang).first()
        context_dict["language"] = language
        context_dict["panels"] = GroupedSubjects.groupSubject(language)
        return render(request,"myforms/base.html", context_dict)

    @staticmethod
    def groupSubject(language, aktive_group=""):
        subject_list = Subject.objects.filter(language=language)
        panel_titles = list({s.group for s in subject_list})
        panels = {}
        for i,panel_title in enumerate(panel_titles):
            if panel_title != aktive_group:
                colapsed = "collapse"  #To se zapiše v class ot panela
            else:
                colapsed = ""

            panels[panel_title] = Panel(title = panel_title,
                                parent = "parent{0}".format(i),
                                href = "collapse{0}".format(i),
                                data_toggle = "collapse",
                                collapsed = colapsed)


        for subject in subject_list:
            try:
                panels[subject.group].add_subject(subject)
            except KeyError as e:
                #For testing puprposses
                pass
        return [panel for panel in panels.values()]




class Panel:
    """
    Helper class for grouping subjects in groups for
    displaying in sidebar accordian style menu
    """
    def __init__(self, title,parent, href, data_toggle, collapsed):
        self.title = title
        self.data_parent = parent
        self.href = href
        self.data_toggle = data_toggle
        self.subjects = []
        self.subjects_count = 0
        self.collapsed = collapsed  #S tem določam ali je menu odprt ali zaprt

    def add_subject(self, subject):
        self.subjects.append(subject)
        self.subjects_count += 1

#END OF VIEWS FOR NAVIGATION

class ExerciseView(View):

    def get(self,request,*args, **kwargs):
        lang = kwargs.get("language")
        form = ExerciseForm()
        form.set_subjects(get_subjects_list(lang))
        context = {}
        context["action"] = reverse("exercise_add2",
                                        kwargs = {"language": "ru"})
        context["form"] = form
        return render(request,"myforms/exercise_form2.html", context)

    def post(self, request,*args, **kwargs):
        form = ExerciseForm(request.POST)
        lang = kwargs.get("language")
        form.set_subjects(get_subjects_list(lang)) #Drugače mi javi error, da vrednost ne obstaja

        if form.is_valid():
            # <process form cleaned data>
            exercise = form.save(commit=False)
            subj_id = form.cleaned_data["subject_language"]
            exercise.subject = get_object_or_404(Subject,id=subj_id)
            exercise.save()
            return HttpResponseRedirect(reverse("subjects", kwargs={"language" : "ru"}))

        return render(request,"myforms/exercise_form2.html", {"form":form})

def get_subjects_list(language):
    """
    Return tuple of subject for given language suitable for
    displaying in forms.ChoiceField
    :param language:
    :return:tuple of tuples
    """
    language_obj = get_object_or_404(Language,language=language)
    subjects = Subject.objects.filter(language=language_obj)
    return tuple([(str(subject.id),subject.subject) for subject in subjects])


#SUBJECT EDIT VIEWS
class SubjectList(ListView):
    model = Subject
    context_object_name = "subject_list"
    template_name = "myforms/subjects.html"

    def get_context_data(self, **kwargs):
        """context moram razširiti s podatki, ki jih potrbuje base.html.
        To je s spiskom tem za posamezen jezi
        V nasprotnem primeru, v stranskem pladnju ni podatkov.
        """
        language = get_object_or_404(Language, language=self.kwargs["language"])
        context = super().get_context_data(**kwargs)
        context["language"] = language
        context["panels"] = GroupedSubjects.groupSubject(language)
        return context


class SubjectViewMixin:
    model = Subject
    form_class = SubjectForm
    template_name = "myforms/subject_form.html"

    def get_success_url(self, **kwargs):
        lang= self.kwargs.get("language")
        return reverse("subjects_list", kwargs={"language": lang})

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        lang = self.kwargs.get("language")
        language = get_object_or_404(Language,language=lang)
        if type(self) is SubjectUpdateView:
            context["action"] = reverse("subject_edit",
                                kwargs = {"pk":self.object.id, "language" : lang})
        else:
            context["action"] = reverse("subject_add",
                                        kwargs = {"language": lang})
        context["language"] = language
        context["panels"] = GroupedSubjects.groupSubject(language)
        return context


class SubjectUpdateView(SubjectViewMixin, UpdateView):
    pass


class SubjectCreateView(SubjectViewMixin, CreateView):

    def get_initial(self,**kwargs):
        lang=self.kwargs.get("language")
        language = Language.objects.filter(language=lang).first()
        return {
            "language": language,
        }
#END OF SUBJECT EDIT VIEWS


#LANGUAGE EDIT VIEWS
class LanguageList(ListView):
    model = Language
    context_object_name = "language_list"
    template_name = "myforms/languages.html"

    def get_context_data(self, **kwargs):
        language = get_object_or_404(Language, language=self.kwargs.get("language"))
        context = super().get_context_data(**kwargs)
        context["language"] = language
        context["panels"] = GroupedSubjects.groupSubject(language)
        return context


class LanguageViewMixin:
    model = Language
    form_class = LanguageForm
    template_name = "myforms/language_form.html"

    def get_success_url(self, **kwargs):
         return reverse("language_list", kwargs={"language": self.kwargs.get("language")})

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        lang = self.kwargs.get("language")

        language = get_object_or_404(Language,language=lang)
        if type(self) is LanguageUpdateView:
            context["action"] = reverse("language_edit",
                                kwargs = {"pk":self.object.id, "language" : lang})
        else:
            context["action"] = reverse("language_add",
                                        kwargs = {"language": lang})
        context["language"] = language
        context["panels"] = GroupedSubjects.groupSubject(language)
        return context



class LanguageUpdateView(LanguageViewMixin, UpdateView):
    pass


class LanguageCreateView(LanguageViewMixin, CreateView):
    pass

#END OF LANGUAGE EDIT VIEWS




#EXERCISE MODEL VIEWS

class ExerciseList(ListView):
    context_object_name = "exercise_list"
    template_name = "myforms/exercises.html"

    def get_queryset(self):
        subject_id = self.kwargs.get("subject")
        subject_obj = get_object_or_404(Subject, id = subject_id)
        return ExercisesModel.objects.filter(subject = subject_obj)

    def get_context_data(self, **kwargs):
        """context moram razširiti s podatki, ki jih potrbuje base.html.
        To je s spiskom tem za posamezen jezi
        V nasprotnem primeru, v stranskem pladnju ni podatkov.
        """
        subject_id = self.kwargs.get("subject")
        subject_obj = get_object_or_404(Subject, id = subject_id)
        context = super().get_context_data(**kwargs)
        context["language"] = subject_obj.language
        context["panels"] = GroupedSubjects.groupSubject(subject_obj.language, subject_obj.group)
        return context


class ExerciseMixin:

    def get_success_url(self):

        return reverse("exercises",
                       kwargs = {"subject": self.object.subject.id,
                            "language" : self.object.subject.language.language })

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        lang = self.kwargs.get("language")
        language = Language.objects.filter(language=lang).first()
        context["language"] = language
        if self.object:
            context["panels"] = GroupedSubjects.groupSubject(language,self.object.subject.group)
        else:
            context["panels"] = GroupedSubjects.groupSubject(language)

        if type(self) is ExerciseUpdateView:
            context["action"] = reverse("exercise_edit",
                                kwargs = {"pk":self.get_object().id, "language" : lang})
        else:
            context["action"] = reverse("exercise_add",
                                        kwargs = {"language": lang})
        return context

    def get_form(self, form_class):
        form = form_class(**self.get_form_kwargs())
        form.set_subjects(get_subjects_list(self.kwargs.get("language")))
        return form

    def form_valid(self, form):
        self.object = form.save(commit=False)
        subj_id = form.cleaned_data["subject_language"]
        self.object.subject = get_object_or_404(Subject,id=subj_id)
        self.object.save()
        return super().form_valid(form)



class ExerciseUpdateView(ExerciseMixin, UpdateView):
    model = ExercisesModel
    fields = ["language", "subject_language", "name", "exercise"]
    form_class = ExerciseForm
    template_name = "myforms/exercise_form.html"

    def get_initial(self,*args, **kwargs):
        return {
            "subject_language" : self.object.subject.id
        }


class ExerciseCreateView(ExerciseMixin, CreateView):
    model = ExercisesModel
    form_class = ExerciseForm
    fields = ["language", "subject_language", "name", "exercise"]
    template_name = "myforms/exercise_form.html"

    def get_initial(self,**kwargs):
        lang=self.kwargs.get("language")
        language = Language.objects.filter(language=lang).first()

        return {
            "language": language,
        }


class ExerciseSolveView(View):
    def get(self, request, pk, language): #pk parameter defined in url
        exercise = get_object_or_404(ExercisesModel,pk=pk)
        context_dict = {}
        context_dict["exercise_name"] = exercise.name
        context_dict["exercise_id"] = exercise.id
        context_dict["language"] = exercise.language
        context_dict["subject"] = exercise.subject.id
        listDisplay, listCheck = my_parser.parse(exercise.exercise.strip())
        context_dict["exercise_parts"] = listDisplay
        context_dict["action"] = reverse("exercise_solve",
                kwargs = {'pk': exercise.id, 'language': exercise.language.language})

        context_dict["panels"] = GroupedSubjects.groupSubject(exercise.language,exercise.subject.group)
        return render(request,"myforms/exercise_solve.html", context_dict)

    def post(self, request, pk,  *args, **kwargs):
        exercise = get_object_or_404(ExercisesModel,pk=pk)
        listDisplay, listCheck = my_parser.parse(exercise.exercise.strip())
        i=0
        context_dict = {}
        correct_answers = 0
        incorrect_answers = 0
        for key in listCheck.keys():
            answer_is_correct = my_parser.markUserAnswer(key,request.POST[key],listDisplay)
            if answer_is_correct:
                correct_answers += 1
            else:
                incorrect_answers += 1
        #Tu bi bilo bolj enostavno v context_dict postaviti exercise object
        context_dict["exercise_id"] = exercise.id
        context_dict["exercise_parts"] = listDisplay
        context_dict["exercise_name"] = exercise.name
        context_dict["language"] = exercise.language
        context_dict["panels"] = GroupedSubjects.groupSubject(exercise.language, exercise.subject.group)
        context_dict["correct_answers"] = correct_answers
        context_dict["incorrect_answers"] = incorrect_answers
        #add_translated_strings(context_dict,
        #                       "exercise_check.html",
        #                       exercise.language.language,
        #                       "Here_are_the_results_of", "Nazaj_na_vajo")
        return render(request,"myforms/exercise_check.html",context_dict)

#END OF EXERCISE MODEL VIEWS



#USER AUTHENTICATION AND REGISTRATION VIEWS
def register(request, language):
    """Ta view realiziram kot funkcijo, ker uporablja dve formi,
    za enkrat še ne vem, kako to narediti z
    """
    registred = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            #set password hashira password
            user.set_password(user.password)
            user.save()
            profile_form = profile_form.save(commit=False)
            profile_form.user = user
            profile_form.save()
            registred = True
            return HttpResponseRedirect(reverse("subjects", kwargs={"language" : language}))
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    language_obj = Language.objects.filter(language=language).first()
    return render(request,"myforms/register.html",
                  {"user_form" : user_form,
                   "profile_form":profile_form,
                   "registred":registred,
                   "language" : language_obj})

class LoginView(View):
    def post(self, request, language):
        form = LoginForm(data=request.POST)
        username =  form.data["user"]
        password =  form.data["password"]
        user = authenticate(username=username, password=password)
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("subjects", kwargs={"language" : language}))
            else:
               return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            return HttpResponse("Invalid login details supplied.")
            return render(request,"myforms/login.html",
                    {"form" : LoginForm(),"error_message": "Invalid login details"})

    def get(self, request, language):
        language_obj = Language.objects.filter(language=language).first()
        return render(request,"myforms/login.html", {"form" : LoginForm(),
                                                     "language": language_obj})



@login_required
def user_logout(request, language):
    logout(request)
    return HttpResponseRedirect(reverse("subjects", kwargs={"language" : language}))


#END OF USER AUTHENTICATION AND REGISTRATION VIEWS








