import datetime
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from annotation.models import Annotation
from annotation.forms import AnnotationModelForm
from django.utils import simplejson

def annotation_list(request, content_type_str, obj_id, position):
    ct = ContentType.objects.get(name=content_type_str)
    obj = ct.model_class().objects.get(id=obj_id)
    ann_list = Annotation.objects.filter(content_type=ct, object_id=obj.id)
    if request.is_ajax():
        return HttpResponse(simplejson.dumps(list(ann_list)))
    return render_to_response('annotations/list.html',
                              {'annotation_list': ann_list})

def annotate_form(request, content_type_str, obj_id, position=None):
    """
    Renders an AJAX-friendly html form for submitting snippets.
    """
    ct = ContentType.objects.get(name=content_type_str)
    obj = ct.model_class().objects.get(id=obj_id)
    ann_list = Annotation.objects.filter(content_type=ct, object_id=obj.id, position=position)
    preform_data = {'commentor':request.user.id,
                    'content_type':ct.id,
                    'object_id':obj_id,
                    'date_added':datetime.datetime.now(),
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
                                       'annotation_list': ann_list,
                                       'annotation_object': obj})
    else:
        # invalid / new
        return render_to_response('annotations/inline_form.html',
                                  {'form':f,
                                   'content_type': ct.name,
                                   'obj_id': obj.id,
                                   'position': position,
                                   'annotation_list': ann_list,
                                   'annotation_object': obj})
