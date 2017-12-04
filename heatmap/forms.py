from django import forms


class BikeShareHtmlInput(forms.Form):
    html_paste = forms.CharField(widget=forms.Textarea(attrs={'rows':'5'}))
