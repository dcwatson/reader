from django import forms

from reader.models import Subscription


class SettingsForm (forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ('show_read',)
