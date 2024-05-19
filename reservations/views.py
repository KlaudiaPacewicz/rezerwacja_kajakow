from typing import Any
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView

from reservations.forms import ConfirmReservationForm, ListViewFilterForm
from reservations.models import Kajak, Klient, Rezerwacja

# Create your views here.

# w class view request jest w  "self.request"
class KajakListView(ListView):
    model = Kajak
    template_name = "kajaki_list.html"
    context_object_name = "object_list"

    def get_queryset(self):
        # w query set jesli chcemy isc "dalej" w relacjach to uzywamy __
        # a jak chcemy wziac wartosc obiektu to _
        # qs ktory wyswietli kajaki ktore zarezerwowal klient o id 1
        # qs = Kajak.objects.filter(reservations__klient_id=1)
        # wyswietl kajaki ktore nie maja rezerwacji
        qs = Kajak.objects.filter(reservations=None)
        return qs
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        data = super().get_context_data(**kwargs)
        data["form"] = ListViewFilterForm()
        return data
    
    def post(self, request, *args, **kwargs):
        qs = self.get_queryset() # wez szeroki widok kajakow
        filter_form = ListViewFilterForm(self.request.POST) # zaladuj dane do formularza
        if filter_form.is_valid(): # sprawdz czy formularz jest dobrze uzupelniony
            # filtering logic
            number_of_seats = filter_form.cleaned_data["seats"] # wybierz z formularza ilosc miejsc ktore ma miec kajak
            cargo = filter_form.cleaned_data["cargo"] # wybierz z formularza ilosc miejsc ktore ma miec kajak
            # filter main kajak queryset by number of seats
            if number_of_seats is not None: # jesli liczba miejsc zostala podana
                qs = qs.filter(seats=number_of_seats) # wez kajaki ktore pole seats jest rowne podanej liczbie miejsc
            if cargo != "None": # jesli opcja cargo zostala podana
                qs = qs.filter(cargo=cargo) # wybierz kajaki ktore sa cargo
        context = {self.context_object_name: qs, 'form': filter_form }
        return render(request, self.template_name, context)



class KajakDetailView(DetailView):
    model = Kajak
    template_name = "kajak_detail.html"

# w method view request jest przekazwywany jako argument
def confirm_reservation(request, kajak_id):
    # REQUEST METHODS
    # GET
    # POST
    # PUT
    # DELETE
    message = ""
    if request.method == "POST":
        form = ConfirmReservationForm(request.POST)
        if form.is_valid():
            klient, created = Klient.objects.get_or_create(mail=form.cleaned_data["mail"], defaults={"phone":form.cleaned_data["phone"], "birth_day": form.cleaned_data["birth_day"]})
            kajak = get_object_or_404(Kajak, id=kajak_id)
            if not kajak.reservations.exists():
                rezerwacja = Rezerwacja.objects.create(klient=klient, kajak=kajak)
                print(f"Stworzono rezerwacje {rezerwacja}")
                return redirect("kajaki-list")
            else:
                form = ConfirmReservationForm()
                message = "Ten kajak jest juz zarezerwowany"
                
    else:
        form = ConfirmReservationForm()

    return render(request, "confirm_reservation.html", {"form": form, "kajak_id": kajak_id, "message": message})
    