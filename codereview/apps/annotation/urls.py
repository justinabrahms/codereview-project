from django.conf.urls.defaults import *

urlpatterns = patterns("",
  url('(?P<content_type_str>[-\w]+)/(?P<obj_id>\d+)/annotate_form/(?P<position>\d+)/',
      'annotation.views.annotate_form',
      name='annotate-form'),
)
