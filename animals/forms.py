from django import forms
from .models import ShelterSettings

class ShelterSettingsForm(forms.ModelForm):
    class Meta:
        model = ShelterSettings
        fields = '__all__'
