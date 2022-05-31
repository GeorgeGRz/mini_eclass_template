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
    path('unregister/<int:course_id>',views.user_unregister,name="unregister"),
    path('<int:class_id>/users',views.showUsers,name='users'),
    path('<int:class_id>/files', views.files, name='files'),
    path('<int:class_id>/quizes', views.list_quizes, name='quizes'),
    path('<int:class_id>/upload_file',views.file_upload,name='file_upload'),
    path('<int:class_id>/livechat',views.chat,name='livechat'),
    path('<int:class_id>/new_announcement',views.addAnnouncement,name='newAnnouncement'),
    path('<int:class_id>/announcement/<int:announcement_id>',views.announcementDetail,name="announcement_Detail"),
    path('<int:class_id>/announcements',views.classAnnouncements,name="classAnnouncements"),
    #--------------------------------------------------------------------------#
    path("<int:class_id>/create_quiz",q_views.create_quiz,name="quiz_create"), #forward the creation of quiz to the questions
    path('<int:class_id>/quiz_create_submit/',q_views.submit_new_question,name='submit_new_question'),
    path('<int:class_id>/quiz_enable/<int:quiz_id>',q_views.quiz_enable,name='quiz_enable'),
    path('<int:class_id>/quiz_disable/<int:quiz_id>',q_views.quiz_disable,name='quiz_disable'),
    path('<int:quiz_id>/quiz_detail',q_views.detail,name='quiz_detail'),
    path('<int:question_id>/answer/', q_views.answer, name='answer'),
    path('<int:quiz_id>/show/', q_views.quiz_showAnswered, name='showQuiz'),
]
