from django import forms
from pybo.models import Question

# form.is_valid(): request 객체로 들어온 입력값이 내가 원하는 모델에 맞는지 검사한다.
# form.save(commit=False): model 객체를 생성하고 임시저장. 추가적인 처리를 할 수 있다.
# form.save() or form.save(commit=True): model 객체를 생성하고 데이터베이스에 저장한다.
## 모델 객체의 모든 필드에 값이 할당되지 않았다면 오류가 발생한다.

# create_date는 사용자로부터 입력을 받지 않는다.
class   QuestionForm(forms.ModelForm):
    class   Meta:
        model = Question
        fields = ['subject', 'content']
