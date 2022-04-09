from django import template
from classes.models import *
register = template.Library()

@register.filter(name='enrolled')
def enrolled(user, course):
    return course.enrolledPeople.filter(pk=user.id).exists()