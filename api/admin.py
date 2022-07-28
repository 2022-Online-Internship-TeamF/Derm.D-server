from django.contrib import admin
from .models import *


class ConditionMediaInline(admin.TabularInline):
    model = ConditionMedia

class QuestionMediaInline(admin.TabularInline):
    model = QuestionMedia

class AnswerMediaInline(admin.TabularInline):
    model = AnswerMedia

class ConditionAdmin(admin.ModelAdmin):
    inlines = (ConditionMediaInline,)

class QuestionAdmin(admin.ModelAdmin):
    inlines = (QuestionMediaInline,)

class AnswerAdmin(admin.ModelAdmin):
    inlines = (AnswerMediaInline,)


admin.site.register(User)
admin.site.register(Archive)

admin.site.register(Condition, ConditionAdmin)

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)