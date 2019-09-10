from django import forms
from .models import Listings, File

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('file',)

class Upload(forms.Form):
    #class Meta:
        #model = Listings
        #fields = ('textracted', 'photo_main', 'photo_1',) #'photo_main',
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

class newReading(forms.ModelForm):
    class Meta:
        model = Listings
        fields = ('title',)