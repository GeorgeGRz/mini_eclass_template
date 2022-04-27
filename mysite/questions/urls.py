from django.urls import path

from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.index, name='index'),
    
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/answer/', views.answer, name='answer'),

    #path('quiz_create/', views.create_quiz, name='quiz_create'),
    #path('quiz_create_submit/',views.submit_new_question,name='submit_new_question'),
    
]
