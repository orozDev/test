from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class TimeAbstractModel(models.Model):
    
    class Meta:
        abstract = True
    
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='дата добавления')
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='дата изменения')
    
    
class Category(TimeAbstractModel):
    
    class Meta:
        verbose_name = _('категория')
        verbose_name_plural = _('категории')
        ordering = ('-created_at', '-updated_at')
    
    title = models.CharField(_('название'), max_length=50, unique=True)
    
    def __str__(self):
        return f'{self.title}'
    
    
class Test(TimeAbstractModel):
    
    class Meta:
        verbose_name = _('тест')
        verbose_name_plural = _('тесты')
        ordering = ('-created_at', '-updated_at')
        
    title = models.CharField(_('название'), max_length=60)
    image = models.ImageField(_('изображение'), 
        upload_to='tests_images', null=True, blank=True)
    description = models.TextField(_('описание'))
    time = models.PositiveIntegerField(_('время завершения'), 
                help_text=_('Указывается в секундах'))
    category = models.ForeignKey(Category, on_delete=models.PROTECT, 
                verbose_name=_('категория'))
    
    @property
    def amount_of_questions(self):
        return self.questions.all().count()
    amount_of_questions.fget.short_description = _('Количество вопросов')
    
    def __str__(self):
        return f'{self.title}'
    

class Question(TimeAbstractModel):
    
    class Meta:
        verbose_name = _('вопрос')
        verbose_name_plural = _('вопросы')
        ordering = ('-created_at', '-updated_at')
    
    title = models.CharField(_('вопрос'), max_length=250)
    test = models.ForeignKey(Test, 
        verbose_name=_('тест'), on_delete=models.CASCADE, related_name='questions')
    first_answer = models.CharField(_('превый вариант'), max_length=250)
    second_answer = models.CharField(_('второй вариант'), max_length=250)
    third_answer = models.CharField(_('третий вариант'), max_length=250)
    forth_answer = models.CharField(_('четвертый вариант'), max_length=250)
    true_answer = models.IntegerField(_('правильный вариант'), validators=[
        MinValueValidator(1), MaxValueValidator(4)])
    explaining = models.TextField(_('объяснение'))
    
    def __str__(self):
        return f'{self.title}'

    @property
    def letter_answer(self):
        if self.true_answer == 1:
            return 'а'
        elif self.true_answer == 2:
            return 'б'
        elif self.true_answer == 3:
            return 'в'
        else:
            return 'г'
    

class UsersTest(TimeAbstractModel):
    
    class Meta:
        verbose_name = _('тест пользователя')
        verbose_name_plural = _('тесты пользователя')
        ordering = ('-created_at', '-updated_at')
    
    COMPLETED =  'completed'
    IN_PROGRESS = 'in_progress' 
     
    STATUS = (
        (COMPLETED, _('Завершенный')),
        (IN_PROGRESS, _('В ходе выполнения')),
    )
    
    user = models.ForeignKey(User, related_name='tests', 
        verbose_name=_('пользователь'), on_delete=models.CASCADE)
    test = models.ForeignKey(Test, verbose_name=_('тест'), on_delete=models.PROTECT)
    status = models.CharField(_('Status'), max_length=20, default=IN_PROGRESS, choices=STATUS)
    
    @property
    def amount_of_correct_answers(self):
        return self.test.amount_of_questions - self.incorrect_answers.all().count()
    amount_of_correct_answers.fget.short_description = _('Количество верных вопросов')
    
    def __str__(self):
        return f'{self.user} - {self.test}'
    

class IncorrectAnswers(TimeAbstractModel):
    
    class Meta:
        verbose_name = _('неправильный ответ')
        verbose_name_plural = _('неправильные ответы')
        ordering = ('-created_at', '-updated_at')
        
    user_test = models.ForeignKey(UsersTest, on_delete=models.CASCADE,
        verbose_name=_('тест пользователь'), related_name='incorrect_answers')
    question = models.ForeignKey(Question, 
        verbose_name=_('вопрос'), on_delete=models.PROTECT)
    answer = models.IntegerField(_('выбранный вариант'), validators=[
        MinValueValidator(0), MaxValueValidator(4)], default=0)
    
    @property
    def correct_answer(self):
        return self.question.true_answer
    correct_answer.fget.short_description = _('правильный вариант')
    
    @property
    def letter_answer(self):
        if self.question.true_answer == 1:
            return 'а'
        elif self.question.true_answer == 2:
            return 'б'
        elif self.question.true_answer == 3:
            return 'в'
        else:
            return 'г'
    
    def __str__(self):
        return f'{self.user_test}'
                                 
# Create your models here.
