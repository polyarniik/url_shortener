from django import forms


class LinkForm(forms.Form):
    """
    Форма для создания ссылки
    """
    url = forms.URLField(label="Link")
