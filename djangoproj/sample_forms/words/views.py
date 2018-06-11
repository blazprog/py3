from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse


from .forms import WordForm
from .models import Word


def index(request):
    return render(request,"words/index.html")

def add_word(request):
    if request.method == "POST":
        form = WordForm(request.POST)
        if form.is_valid():
            word = form.save(commit=True)
            print(word.id)
            return HttpResponseRedirect(reverse("words:home"))
        else:
            print(form.errors)
    else: # GET
        form = WordForm()

    context = {"form" : form}
    return render(request,"words/add_word.html", context)


def list_all_words(request):
    words = Word.objects.order_by("translation")
    context_dict = {"words_list" : words}
    return render(request,"words/words_list.html", context_dict)



def practice_words(request):
    words = Word.objects.order_by("translation")
    context_dict = {"words_list" : words}
    return render (request, "words/practice.html", context_dict)

def check_answer(request):
    answer=""
    word_id = None
    is_correct = False
    if request.method == "GET":
        answer = request.GET["answer"]
        word_id = request.GET["word_id"]
        word = Word.objects.get(id = int(word_id))
        if word.word.strip() == answer.strip():
            is_correct = True

    data = {"is_answer_correct" : is_correct,
            "correct_answer" : word.word.strip()}

    return JsonResponse(data)



def get_singer_details(request):
    singers =  {"Blondie": "American singer with hits Blondie, One Way or Another",
             "Samantha":"She use to sing the best is yet to come!",
              "Kim":"She was a pilots wife, tailand based"}
    singer_name = ""
    if request.method == "GET":
        singer_name = request.GET["singer"]
        data = {"singer": singer_name,
                "description": singers[singer_name]}

        return JsonResponse(data)





def check_json(request):
    print("Returning Json from function")
    data = {'name': 'bard', 'surname': 'simpson'}
    print(data)
    return JsonResponse(data)





