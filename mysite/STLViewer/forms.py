from django import forms
from django_select2 import forms as s2forms

from . import models

class TagEditor(forms.ModelForm):
    tagEditor = forms.ModelMultipleChoiceField(
        queryset= models.Taggins.objects.values_list("tag",flat=True).distinct(),
        widget = s2forms.Select2TagWidget(attrs={'data-allow-clear':"true",'data-placeholder': "Select a value",'placeholder':" "}),   
        label="Tags:",
        required=False,
    )

    class Meta:
        model = models.Taggins
        fields = ["tagEditor",]


class TagFilter(forms.ModelForm):
    tagFilter = forms.ModelMultipleChoiceField(
        queryset = models.Taggins.objects.values_list("tag",flat=True).distinct(),
        widget = s2forms.Select2MultipleWidget(attrs={'data-allow-clear':"true",'data-placeholder': "Select a value",'placeholder':" "}),   
        label="Suche: Tags:",
        required=False,
    )

    class Meta:
        model = models.Taggins
        fields = [ "tagFilter",]
 
class ItemSearchForm(forms.Form):
    search = forms.CharField(label='Search', max_length=100, required=False)

  



   