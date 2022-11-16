from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice

# Create your views here.

# def index(request):
#     #Trae todas las preguntas de la base de datos
#     latest_question_list = Question.objects.all() 
    
#     return render(request, "polls/index.html", {
#         "latest_question_list": latest_question_list
#     })


# def detail(request, question_id):
#     #trae todas las opciones de respuesta de la pregunta seleccionada
#     question = get_object_or_404(Question, pk=question_id)
    
#     return render(request, "polls/detail.html", {
#         "question": question
#     })


# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {
#         "question": question
#     })


#Generic Views
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questioons"""
        return Question.objects.filter(pub_date__lte = timezone.now()).order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


#Function View
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try: 
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except(KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "No elegiste una respuesta",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))