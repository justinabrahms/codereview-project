import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey

class Annotation(models.Model):
    commentor = models.ForeignKey(User)
    comment = models.TextField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField()
    entity = GenericForeignKey()
    date_added = models.DateTimeField(default=datetime.datetime.now)
    position = models.CharField(max_length=10)
    
    def __unicode__(self):
        return "Comment for %s on %s" % (self.entity, self.position)
    
