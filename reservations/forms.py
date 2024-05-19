from django import forms

from reservations.models import Kajak, KajakType

def create_choices(choice_list):
    li = [("None", "------"),]
    li2 = [choice for choice in choice_list]
    li.extend(li2)
    return li

class ConfirmReservationForm(forms.Form):
    mail = forms.EmailField()
    phone = forms.CharField(max_length=16)
    birth_day = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    

class ListViewFilterForm(forms.Form):
    start_date = forms.DateTimeField(required=True, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    end_date = forms.DateTimeField(required=True, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    seats = forms.IntegerField(min_value=1, required=False)
    cargo = forms.ChoiceField(choices=[("None", "------"),(True, "TRUE"), (False, "FALSE"),], required=False)
    cup_holder = forms.ChoiceField(choices=[("None", "------"),(True, "TRUE"), (False, "FALSE"),], required=False)
    color = forms.ChoiceField(choices=create_choices(Kajak.KAJAK_COLORS_CHOICES), required=False)
    kajak_type = forms.ChoiceField(choices=create_choices(KajakType.choices()), required=False)
    price_per_hour = forms.DecimalField(decimal_places=2, max_digits=5, required=False)
