from django import forms
from annotation.models import Annotation

class AnnotationModelForm(forms.ModelForm):
    class Meta:
        model = Annotation
