from django import forms

from helpers import consts

_TYPE_OF_FIELDS = {
    'text': forms.CharField,
    'int': forms.IntegerField,
    'date': forms.DateField,
    'datetime': forms.DateTimeField
}
_TYPE_OF_WIDGETS = {
    'text': forms.TextInput(attrs={'class': 'form-control mx-2'}),
    'int': forms.NumberInput(attrs={'class': 'form-control mx-2'}),
    'date': forms.DateInput(attrs={'class': 'form-control mx-2', 'type': 'date'}),
    'datetime': forms.DateTimeInput(attrs={'class': 'form-control mx-2', 'type': 'datetime-local'})
}
_SHOW_CHOICES = (
    (consts.SCREEN, 'На экран'),
    (consts.CSV, 'CSV'),
    (consts.XLSX, 'XLSX')
)


class PromoForm(forms.Form):
    count = forms.IntegerField(initial=10, required=True, widget=_TYPE_OF_WIDGETS['int'])
    length = forms.IntegerField(initial=10, required=True, widget=_TYPE_OF_WIDGETS['int'])
    prefix = forms.CharField(required=False, widget=_TYPE_OF_WIDGETS['text'])
    postfix = forms.CharField(required=False, widget=_TYPE_OF_WIDGETS['text'])
    show = forms.ChoiceField(choices=_SHOW_CHOICES, required=True,
                             widget=forms.Select(attrs={'class': 'form-control ml-2'}))


class ReportForm(forms.Form):
    show = forms.ChoiceField(choices=_SHOW_CHOICES, required=True,
                             widget=forms.Select(attrs={'class': 'form-control ml-2'}))

    def __init__(self, *args, report_params=None, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        if report_params:
            for param in report_params:
                self.fields[param['slug']] = \
                    _TYPE_OF_FIELDS[param['input_type']](required=param['is_mandatory'],
                                                         label=param['title'],
                                                         widget=_TYPE_OF_WIDGETS[param['input_type']])
