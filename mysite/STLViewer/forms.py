from django import forms
from django_select2 import forms as s2forms

from . import models

class myMutipleChoiceField(forms.MultipleChoiceField):
#override the django MutipleChoiceField to allow new values...
     def validate(self,value):
          pass
     


class TagEditor(forms.Form):
    m_choices = []
    for value in models.Taggins.objects.values_list("tag",flat=True).distinct():
            m_choices.append((value,value))
    tagEditor = myMutipleChoiceField(
        choices = m_choices,
        #choices = models.Taggins.objects.values_list("tag",flat=True).distinct(),
        widget = s2forms.Select2TagWidget(attrs={'data-allow-clear':"true",'data-placeholder': "Select a value",'placeholder':" "}),   
        label="Tags:",
        required=False,
    )
     
    def clean(self):
        return self.cleaned_data


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

  



   