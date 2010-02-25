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
        self.obj = obj
        self.to_var = to_variable
        
    def render(self, context):
        annotation_list = Annotation.objects.filter(content_type=ContentType.objects.get_for_object(self.obj),
                                                    object_id=self.obj.id)
        return annotation_list

@register.tag(name='get_annotations')    
def do_get_annotations(parser, token):
    try:
        tag_name, object, _, to_variable = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r requires a single argument" % token.contents.split()[0]
    return AnnotationParser(object, to_variable)



class AnnotationJSONParser(template.Node):
    def __init__(self, obj):
        self.obj = obj

    def render(self, context):
        annotation_list = Annotation.objects.filter(content_type=ContentType.objects.get_for_object(self.obj),
                                                    object_id=self.obj.id)
        annotation_list = annotation_list.values('id',
                                                 'date_added',
                                                 'commentor_id',
                                                 'comment',
                                                 'position')
        annotation_json = simplejson.dumps(list(annotation_list))
        return mark_safe(annotation_json)

@register.tag(name='get_annotations_json')
def do_get_annotations_json(parser, token):
    try:
        tag_name, obj  = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r requires a single argument" % token.contents.split()[0]
    return AnnotationJSONParser(obj)
