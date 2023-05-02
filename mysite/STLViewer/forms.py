from django import forms
from django_select2 import forms as s2forms

from . import models
import os
import magic


class myMutipleChoiceField(forms.MultipleChoiceField):
#override the django MutipleChoiceField to allow new values...
     def validate(self,value):
          pass
     
class TagEditor(forms.Form):

    tagEditor = myMutipleChoiceField(
        widget = s2forms.Select2TagWidget(attrs={'data-allow-clear':"true",'data-placeholder': "Select a value",'placeholder':" "}),   
        label="Tags:",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(TagEditor, self).__init__(*args, **kwargs)
        choices = []
        for value in models.Taggins.objects.values_list("tag", flat=True).distinct():
            choices.append((value, value))
        self.fields['tagEditor'].choices = choices
     
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

    def __init__(self, *args, **kwargs):
        super(TagFilter, self).__init__(*args, **kwargs)
        self.fields['tagFilter'].queryset = models.Taggins.objects.values_list("tag", flat=True).distinct()
 
class ItemSearchForm(forms.Form):
    search = forms.CharField(label='Search', max_length=100, required=False)

class AddItemsForm(forms.Form):
    file = forms.FileField()

    class Meta:
        model = models.Items

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')

        if uploaded_file:
            # Check the file extension
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            if file_extension != '.stl':
                raise forms.ValidationError('Only .stl files are allowed.')
            # Check the file's magic bytes
            #file_path = uploaded_file.temporary_file_path()
            #file_mime = magic.from_file(file_path, mime=True)
            #allowed_mimes = ['model/stl', 'application/octet-stream']
            #if file_mime not in allowed_mimes:
                #raise forms.ValidationError(f'Invalid file format. Only .stl and application/octet-stream files are allowed. (MIME type: {file_mime})')

        return uploaded_file
  



   