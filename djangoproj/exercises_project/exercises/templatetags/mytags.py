from django import template
from exercises.models import Subject

register = template.Library()

@register.inclusion_tag('exercises/subjects_list.html')
def get_subject_list(language = None):
    if language:
        return {"subjects" : Subject.objects.filter(language=language)}
    else:
        return {'subjects': Subject.objects.all()}

