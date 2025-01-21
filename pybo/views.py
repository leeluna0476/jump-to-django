from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.utils import timezone
from django.http import HttpResponseNotAllowed, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm

def index(request):
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)

def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.create_date = timezone.now()
            if request.user.is_authenticated:
                answer.author = request.user
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        return HttpResponseNotAllowed('Only POST is available')
    #너 왜
    context = {'question': question, 'form': form }
    return render(request, 'pybo/question_detail.html', context)

@login_required
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.author = request.user
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

@login_required
def question_delete(request, question_id):
    if request.method == 'POST':
        question = get_object_or_404(Question, pk=question_id)
        if request.user == question.author:
            question.delete()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def answer_delete(request, answer_id):
    if request.method == 'POST':
        answer = get_object_or_404(Answer, pk=answer_id)
        if request.user == answer.author:
            answer.delete()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})
