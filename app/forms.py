from django import forms


class ProfileEditForm(forms.Form):
    description = forms.CharField(required=False)
    new_image = forms.ImageField(required=False)
    card_template_id = forms.IntegerField(required=False, min_value=1, max_value=3)
