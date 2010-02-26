import unittest
import datetime
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django import template
from django.utils import simplejson
from annotation.models import Annotation
from annotation.templatetags.annotation_tags import AnnotationJSONParser, AnnotationParser

class AnnotationTests(unittest.TestCase):
    def setUp(self):
        self.annotation = annotation_gen()
    
    def test_json_parsing(self):
        obj = self.annotation.entity
        parse_cls = AnnotationJSONParser('obj')
        out_txt = parse_cls.render(template.Context({'obj':self.annotation}))
        obj_json = simplejson.loads(out_txt)

        self.assertEquals(obj_json[0]['id'], self.annotation.id)
        self.assertEquals(obj_json[0]['commentor_id'], self.annotation.commentor.id)
        self.assertEquals(obj_json[0]['comment'], self.annotation.comment)
        self.assertEquals(obj_json[0]['position'], self.annotation.position)

    def test_list_view(self):
        parse_cls = AnnotationParser('obj', 'zot')
        ctx = template.Context({'obj':self.annotation.entity})
        parse_cls.render(ctx)
        self.assertEquals(ctx['zot'][0], self.annotation)

    def tearDown(self):
        User.objects.all().delete()
        Annotation.objects.all().delete()

def user_gen(**kwargs):
    kwargs.setdefault('username', 'dvader')
    usr = User.objects.create(**kwargs)
    usr.set_password('the-force')
    return usr

def annotation_gen(**kwargs):
    if not User.objects.count():
        user_gen()
    kwargs.setdefault('commentor', User.objects.order_by('?')[0])
    kwargs.setdefault('comment', 'test comment')
    kwargs.setdefault('content_type', ContentType.objects.get(name__icontains='content type'))
    kwargs.setdefault('object_id', kwargs['content_type'].id)
    kwargs.setdefault('date_added', datetime.datetime.now())
    kwargs.setdefault('position', '2')
    return Annotation.objects.create(**kwargs)
    
