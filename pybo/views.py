from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.utils import timezone
from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from .decorators import require_http_methods
from common.models import GithubUser
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
import json

@require_http_methods(['GET'])
def index(request):
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}
    return render(request, 'pybo/question_list.html', context)

@require_http_methods(['GET'])
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)

@require_http_methods(['POST'])
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = request.POST
    form = AnswerForm(data)
    if form.is_valid():
        answer = form.save(commit=False)
        answer.question = question
        answer.create_date = timezone.now()
        if request.user.is_authenticated:
            answer.author = request.user
        answer.save()
        return redirect('pybo:detail', question_id=question.id)
    context = {'question': question, 'form': form }
    return render(request, 'pybo/question_detail.html', context)

#API test
#@login_required
@require_http_methods(['POST', 'GET'])
def question_create(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = request.POST
        form = QuestionForm(data)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            #API test
            if request.user.is_authenticated:
                question.author = request.user
            else:
                question.author = GithubUser.objects.get(username='test');
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

#API test
#@login_required
@require_http_methods(['DELETE'])
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        question.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

#API test
#@login_required
@require_http_methods(['PUT'])
def question_modify(request, question_id):
## handle 404 manually by JsonResponse
    try:
        question = get_object_or_404(Question, pk=question_id)
    except Http404:
        return JsonResponse({'error': 'Not Found', 'message': f'Question with ID { question_id } not found'}, status=404)

    if request.user != question.author:
        return JsonResponse({'error': 'Forbidden', 'message': 'Cannot modify question'}, status=403)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = request.body
    form = QuestionForm(data, instance=question)
    if form.is_valid():
        question = form.save(commit=True)
        context = {'question': question, 'form': form }
        return render(request, 'pybo/question_detail.html', context)
    response = JsonResponse({'error': 'Bad Request', 'message': 'Missing required fields or invalid data', 'details': form.errors}, status=400)
    response['Content-Type'] = 'application/json; charset=utf-8';
    return response

#API test
#@login_required
@require_http_methods(['DELETE'])
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        answer.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
