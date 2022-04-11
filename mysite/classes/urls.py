from django.urls import path

from . import views

app_name = 'classes'

urlpatterns = [
    path('create', views.create_to_feed, name="create"),
    path('<int:class_id>/', views.detail, name='detail'),
    path('',views.list_classes,name="list"),
    path('enroll/<int:course_id>',views.user_enroll, name="enroll"),
    path('<int:class_id>/users',views.showUsers,name='users'),
    path('<int:class_id>/files', views.files, name='files'),
]
