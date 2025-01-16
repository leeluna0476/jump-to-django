from django import forms
from pybo.models import Question

# form.is_valid(): request 객체로 들어온 입력값이 내가 원하는 모델에 맞는지 검사한다.
# form.save(commit=False): model 객체를 생성하고 임시저장. 추가적인 처리를 할 수 있다.
# form.save() or form.save(commit=True): model 객체를 생성하고 데이터베이스에 저장한다.
## 모델 객체의 모든 필드에 값이 할당되지 않았다면 오류가 발생한다.

# create_date는 사용자로부터 입력을 받지 않는다.
# widgets에 bootstrap class를 attr로 추가하여 django가 html을 생성할 때 스타일이 적용되도록 한다.
class   QuestionForm(forms.ModelForm):
    class   Meta:
        model = Question
        fields = ['subject', 'content']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }
        labels = {
            'subject': '제목',
            'content': '내용',
        }
