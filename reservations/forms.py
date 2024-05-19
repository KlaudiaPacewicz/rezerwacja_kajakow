from django import forms


class ConfirmReservationForm(forms.Form):
    mail = forms.EmailField()
    phone = forms.CharField(max_length=16)
    birth_day = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    

class ListViewFilterForm(forms.Form):
    seats = forms.IntegerField(min_value=1)
