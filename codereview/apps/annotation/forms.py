from django import forms
from django.forms import widgets
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from annotation.models import Annotation

class AnnotationModelForm(forms.ModelForm):
    commentor = forms.ModelChoiceField(widget=widgets.HiddenInput, queryset=User.objects.all())
    content_type = forms.ModelChoiceField(widget=widgets.HiddenInput, queryset=ContentType.objects.all())
    object_id = forms.IntegerField(widget=widgets.HiddenInput)
    date_added = forms.DateTimeField(widget=widgets.HiddenInput, required=False)
    position = forms.CharField(widget=widgets.HiddenInput)
    class Meta:
        model = Annotation
