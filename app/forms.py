from django import forms


class ProfileEditForm(forms.Form):
    description = forms.CharField(required=False)
    new_image = forms.ImageField(required=False)
