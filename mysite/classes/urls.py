from django.urls import path

import questions

from . import views
from questions import views as q_views
app_name = 'classes'

urlpatterns = [
    path('create', views.create_to_feed, name="create"),
    path('<int:class_id>/', views.detail, name='detail'),
    path('',views.list_classes,name="list"),
    path('enroll/<int:course_id>',views.user_enroll, name="enroll"),
    path('<int:class_id>/users',views.showUsers,name='users'),
    path('<int:class_id>/files', views.files, name='files'),
    path('<int:class_id>/quizes', views.list_quizes, name='quizes'),
    #--------------------------------------------------------------------------#
    path("<int:class_id>/create_quiz",q_views.create_quiz,name="quiz_create"), #forward the creation of quiz to the questions
    path('<int:class_id>/quiz_create_submit/',q_views.submit_new_question,name='submit_new_question'),
]
