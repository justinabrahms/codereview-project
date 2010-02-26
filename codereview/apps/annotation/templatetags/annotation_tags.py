try:
    import simplejson
except ImportError:
    try:
        import json
    except ImportError:
        from django.utils import simplejson
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import mark_safe
from django import template
from annotation.models import Annotation

register = template.Library()

class AnnotationParser(template.Node):
    def __init__(self, obj, to_variable):
        self.obj = template.Variable(obj)
        self.to_var = to_variable
        
    def render(self, context):
        obj = self.obj.resolve(context)
        annotation_list = Annotation.objects.filter(content_type=ContentType.objects.get_for_model(obj),
                                                    object_id=obj.id)
        context[self.to_var] = annotation_list
        return ''

@register.tag(name='get_annotations')    
def do_get_annotations(parser, token):
    """
    Given an object which has annotations and a variable, this tag
    will add create the variable in the template's context with a list
    of annotations.

    Syntax
    
    ::
    
      {% load annotation_tags %}
      {% get_annotations <object> as <variable %}
      
    """
    try:
        tag_name, object, _, to_variable = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r requires a single argument" % token.contents.split()[0]
    return AnnotationParser(object, to_variable)


class AnnotationJSONParser(template.Node):
    def __init__(self, obj):
        self.obj = template.Variable(obj)

    def render(self, context):
        obj = self.obj.resolve(context)
        annotation_list = Annotation.objects.filter(content_type=ContentType.objects.get_for_model(obj.entity),
                                                    object_id=obj.entity.id)
        annotation_list = annotation_list.values('id',
                                                 'commentor_id',
                                                 'comment',
                                                 'position')
        annotation_json = simplejson.dumps(list(annotation_list))
        return mark_safe(annotation_json)

@register.tag(name='get_annotations_json')
def do_get_annotations_json(parser, token):
    """
    Given an object which has annotations, this tag will add return a
    json representation of the annotations.

    Syntax
    
    ::
    
      {% load annotation_tags %}
      {% get_annotations_json <object> %}

    """
    try:
        tag_name, obj  = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r requires a single argument" % token.contents.split()[0]
    return AnnotationJSONParser(obj)
