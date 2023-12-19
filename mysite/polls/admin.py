from django.contrib import admin
from .models import Question, Choice, AdvUser


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInLine]


admin.site.register(Question, QuestionAdmin)


class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')

admin.site.register(AdvUser, AdvUserAdmin)