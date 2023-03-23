from django.urls import path
from .views import *

urlpatterns = [
    path('', Main.as_view(), name='main'),
    path('test/<int:id>/', StartTest.as_view(), name='start_test'),
    path('category/<int:id>/', CategoryFilter.as_view(), name='category_filter'),
    path('ajax/set_answer/<int:id>/', SetAnswer.as_view(), name='set_answer'),
    path('complete_test/<int:id>/', CompleteTest.as_view(), name='complete_test'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('profile/', Profile.as_view(), name='profile'),
    path('profile/logout/', Logout.as_view(), name='logout'),
    path('profile/change/', ChangeProfile.as_view(), name='change_profile'),
    path('profile/change/password/', UpdatePassword.as_view(), name='change_password'),
    path('profile/completed_tests/', ListCompletedTest.as_view(), name='completed_tests'),
    path('profile/completed_tests/<int:id>/', CompletedTest.as_view(), name='completed_test'),
    path('solution/<int:id>/', TestDetail.as_view(), name='solution'),
]
