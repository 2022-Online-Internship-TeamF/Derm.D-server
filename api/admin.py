from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Archive)

admin.site.register(Condition)
admin.site.register(ConditionMedia)

admin.site.register(Question)
admin.site.register(QuestionMedia)

admin.site.register(Answer)
admin.site.register(AnswerMedia)
