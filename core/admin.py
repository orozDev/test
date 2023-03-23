from django.contrib import admin
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.sessions.models import Session
from .models import *

admin.site.register(Session)

class TestAdminForm(forms.ModelForm):
    
    description = forms.CharField(label=_('Описание'), 
        widget=CKEditorUploadingWidget())
    
    class Meta:
        model = Test
        fields = '__all__'
        

class QuestionAdminForm(forms.ModelForm):
    
    title = forms.CharField(label=_('Вопрос'), widget=forms.Textarea)
    first_answer = forms.CharField(label=_('Превый вариант'), 
        widget=CKEditorUploadingWidget())
    second_answer = forms.CharField(label=_('Второй вариант'), 
        widget=CKEditorUploadingWidget())
    third_answer = forms.CharField(label=_('Третий вариант'), 
        widget=CKEditorUploadingWidget())
    forth_answer = forms.CharField(label=_('Четвертый вариант'), 
        widget=CKEditorUploadingWidget())
    explaining = forms.CharField(label=_('объяснение'), 
        widget=CKEditorUploadingWidget())
    
    class Meta:
        model = Test
        fields = '__all__'


class QuestionInline(admin.StackedInline):
    model = Question
    form = QuestionAdminForm
    extra = 0


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'time', 'get_image',)
    search_fields = ('title', 'description', 'time',)
    readonly_fields = ('created_at', 'updated_at', 'get_image', 
                       'amount_of_questions')
    inlines = [QuestionInline,]
    form = TestAdminForm
    
    fieldsets = (
        (_('Оснавная информация'), {'fields': (
            'title',
            'image',
            'category',
            'description',
            'time',
        )}),
        (_('Дополнительная информация'), {'fields': (          
            'created_at',
            'updated_at',
            'get_image',
            'amount_of_questions',
        )}),
    )
    
    @admin.display(description=_('изображение'),)
    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" alt="{obj.title}" width="200px" />')
        return '-'
    
    
class IncorrectAnswersInline(admin.StackedInline):
    model = IncorrectAnswers
    fields = (
        'question',
        'answer',
        'correct_answer',
    )
    readonly_fields = ('correct_answer',)
    extra = 0 
    

@admin.register(UsersTest)
class UsersTestAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'amount_of_correct_answers', 'status',)
    list_filter = ('user', 'test',)
    readonly_fields = ('created_at', 'updated_at', 'amount_of_correct_answers')
    inlines = [IncorrectAnswersInline,]
    
    fieldsets = (
        (_('Оснавная информация'), {'fields': (
            'user',
            'test',
            'status',
        )}),
        (_('Дополнительная информация'), {'fields': (          
            'created_at',
            'updated_at',
            'amount_of_correct_answers',
        )}),
    )
    

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    

# Register your models here.
