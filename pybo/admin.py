from django.contrib import admin

# Register your models here.
from .models import Question, Answer

class   QuestionAdmin(admin.ModelAdmin):
    ordering = ['create_date']
    search_fields = ['subject']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
