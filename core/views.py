from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.generic import DetailView, ListView, View, TemplateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy as _

from .forms import ProfileForm, LoginForm, RegisterForm
from .test_checking import TestChecking
from .models import *


class Main(LoginRequiredMixin, ListView):
    model = Test
    template_name = 'index.html'
    context_object_name = 'tests'
    paginate_by = 6
    login_url = '/login/'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.GET.get('search', None) is not None:
            queryset = queryset.filter(title__icontains=self.request.GET['search'])
        return queryset


class StartTest(LoginRequiredMixin, DetailView):
    model = Test
    template_name = 'test_detail.html'
    context_object_name = 'test'
    pk_url_kwarg = 'id'
    login_url = '/login/'

    def get_context_data(self, object, **kwargs):
        test_checking = TestChecking(
            user=self.request.user,
            request=self.request,
            test=object,
        )
        context = super().get_context_data(**kwargs)
        context['left_time'] = test_checking.left_time
        return context


class SetAnswer(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, id, *args, **kwargs):
        test_checking = TestChecking(
            user=request.user,
            request=request,
            test=get_object_or_404(Test, id=id),
        )
        question_id = request.GET.get('question_id', None)
        answer = request.GET.get('answer', None)
        if question_id is not None and answer is not None:
            is_set = test_checking.set_answer(question_id=question_id, answer=answer)
            return JsonResponse({'is_set': is_set}) \
                if is_set else HttpResponseNotFound({'is_set': is_set})
        return HttpResponseBadRequest({'is_set': False, \
                                       'message': _('Поля question и answer обязательны для заполнения')})


class CategoryFilter(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, id, *args, **kwargs):
        category = get_object_or_404(Category, id=id)
        if request.GET.get('search', None) is not None:
            tests = category.test_set.filter(title__icontains=request.GET['search'])
        else:
            tests = category.test_set.all()
        pagin = Paginator(tests, 6)
        tests = pagin.page(request.GET.get('page', 1))
        return render(request, 'category.html',
                      {'category': category, 'tests': tests})


class CompleteTest(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, id, *args, **kwargs):
        test = get_object_or_404(Test, id=id)
        test_checking = TestChecking(
            user=request.user,
            request=request,
            test=test,
        )
        user_test = test_checking.complete_test()
        if user_test is not None:
            return redirect(f'/profile/completed_tests/{user_test.id}/')
        return redirect(f'/test/{test.id}/')


class CompletedTest(LoginRequiredMixin, DetailView):
    model = UsersTest
    context_object_name = 'user_test'
    template_name = 'completed_test.html'
    pk_url_kwarg = 'id'
    login_url = '/login/'


class ListCompletedTest(LoginRequiredMixin, ListView):
    model = UsersTest
    context_object_name = 'user_tests'
    template_name = 'list_completed_test.html'
    paginate_by = 6
    login_url = '/login/'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class TestDetail(LoginRequiredMixin, DetailView):
    model = Test
    context_object_name = 'test'
    template_name = 'solution.html'
    pk_url_kwarg = 'id'
    login_url = '/login/'


class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'auth/profile.html'
    login_url = '/login/'


class ChangeProfile(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        form = ProfileForm(instance=request.user)
        return render(request, 'auth/change_profile.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _(f'Профиль успешно изменен!'))
            return redirect('/profile/')
        return render(request, 'auth/change_profile.html', {'form': form})


class UpdatePassword(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = '/profile/'
    template_name = 'auth/change_password.html'
    success_message = _('Пароль успешно изменен!')
    login_url = '/login/'


class Logout(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return redirect('/')

class Login(View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            request.session['next'] = request.GET.get('next', '/')
            form = LoginForm()
            return render(request, 'auth/login.html', {'form': form})
        return redirect('/')

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect(request.session.get('next', '/'))
        messages.error(request, _(f'Пользователь не существует или пароль неверный'))
        return render(request, 'auth/login.html', {'form': form})


class Register(View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = RegisterForm()
            return render(request, 'auth/register.html', {'form': form})
        return redirect('/')

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        return render(request, 'auth/register.html', {'form': form})

# Create your views here.