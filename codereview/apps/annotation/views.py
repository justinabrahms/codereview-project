from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from annotation.models import Annotation
from annotation.forms import AnnotationModelForm

def annotate_form(request, content_type_str, obj_id, position=None):
    """
    Renders an AJAX-friendly html form for submitting snippets.
    """
    ct = ContentType.objects.get(name=content_type_str)
    obj = ct.model_class().objects.get(id=obj_id)
    preform_data = {'commentor':request.user.id,
                    'content_type':ct.id,
                    'object_id':obj_id,
                    'position':position}
    f = AnnotationModelForm(request.POST or None, initial=preform_data)
    if f.is_valid():
        if f.save():
            # valid
            return HttpResponseRedirect(obj.get_absolute_url())
        else:
            return render_to_response('annotations/inline_form.html',
                                      {'form':f,
                                       'content_type': ct.name,
                                       'obj_id': obj.id,
                                       'position': position,
                                       'annotation_object': obj})
    else:
        # invalid / new
        return render_to_response('annotations/inline_form.html',
                                  {'form':f,
                                   'content_type': ct.name,
                                   'obj_id': obj.id,
                                   'position': position,
                                   'annotation_object': obj})
