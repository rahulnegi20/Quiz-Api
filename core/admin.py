from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None,{'fields':('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {'fields':('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Importat dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields' : ('email', 'name', 'password', 'password2')
        }),
    )

@admin.register(models.Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display=['id', 'title',]

class AnswerInlineModel(admin.TabularInline):
    model = models.Answer
    fields = ['answer', 'is_correct']

@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    fields = ['quiz', 'question', 'image']
    list_display = ['quiz','question',]

    inlines = [AnswerInlineModel,]

@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['answer', 'is_correct', 'question',]


class QuizTakerAdmin(admin.ModelAdmin):
    fields = ['user', 'quiz']
    list_display = ['user', 'quiz']


admin.site.register(models.User, UserAdmin)
admin.site.register(models.QuizTakers, QuizTakerAdmin)
# admin.site.register(models.Quiz, QuizAdmin)
# admin.site.register(models.Question, QuestionAdmin)
# #admin.site.register(models.Answer, AnswerInlineModel)
