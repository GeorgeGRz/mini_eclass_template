from django import template
from classes.models import *
register = template.Library()

@register.filter(name='enrolled')
def enrolled(user, course):
    return course.enrolledPeople.filter(pk=user.id).exists()

@register.filter(name='getUserById')
def getUserByID(user,userid):
    print(userid)
    return User.objects.get(pk=userid)