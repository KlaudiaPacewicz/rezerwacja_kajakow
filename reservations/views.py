from typing import Any
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView

from reservations.forms import ConfirmReservationForm
from reservations.models import Kajak, Klient, Rezerwacja

# Create your views here.

# w class view request jest w  "self.request"
class KajakListView(ListView):
    model = Kajak
    template_name = "kajaki_list.html"

    def get_queryset(self):
        # w query set jesli chcemy isc "dalej" w relacjach to uzywamy __
        # a jak chcemy wziac wartosc obiektu to _
        # qs ktory wyswietli kajaki ktore zarezerwowal klient o id 1
        # qs = Kajak.objects.filter(reservations__klient_id=1)
        # wyswietl kajaki ktore nie maja rezerwacji
        qs = Kajak.objects.filter(reservations=None)

        # filter_form = ListViewFilterForm(self.request.POST)
        # if filter_form.is_valid():
        #     # filtering logic
        #     pass
        return qs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        return super().get_context_data(**kwargs)


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
    