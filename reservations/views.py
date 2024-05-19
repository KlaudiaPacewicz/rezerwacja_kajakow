from typing import Any
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView

from reservations.forms import ConfirmReservationForm, ListViewFilterForm
from reservations.models import Kajak, Klient, Rezerwacja
from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Count, Q
from django.utils import timezone


from reservations.serializers import StatisticsSerializer

# Create your views here.

# w class view request jest w  "self.request"
def filter_choice_field(qs, field, field_value):
    # if cargo != "None": # jesli opcja cargo zostala podana
    #     qs = qs.filter(cargo=cargo) # wybierz kajaki ktore sa cargo
    # if cup_holder != "None": # jesli opcja cargo zostala podana
    #     qs = qs.filter(cup_holder=cup_holder) # wybierz kajaki ktore sa cargo
    # if color != "None": # jesli opcja cargo zostala podana
    #     qs = qs.filter(color=color) # wybierz kajaki ktore sa cargo
    if field_value != "None": # jesli opcja cargo zostala podana
        qs = qs.filter(**{field: field_value}) # stworzenie key value arguements from dict
    return qs

def filter_non_required_field(qs, field, field_value):
    # if number_of_seats is not None: # jesli liczba miejsc zostala podana
    #     qs = qs.filter(seats=number_of_seats) # wez kajaki ktore pole seats jest rowne podanej liczbie miejsc
    # if price_per_hour is not None: # jesli liczba miejsc zostala podana
    #     qs = qs.filter(price_per_hour=price_per_hour) # wez kajaki ktore pole seats jest rowne podanej liczbie miejsc
    if field_value is not None:
        qs = qs.filter(**{field: field_value})
    return qs

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
        qs = Kajak.objects.prefetch_related("reservations").all()
        return qs
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        data = super().get_context_data(**kwargs)
        data["form"] = ListViewFilterForm()
        data["start_date"] = "bla"
        data["end_date"] = "blabla"
        return data
    
    def post(self, request, *args, **kwargs):
        qs = self.get_queryset() # wez szeroki widok kajakow
        filter_form = ListViewFilterForm(self.request.POST) # zaladuj dane do formularza
        if filter_form.is_valid(): # sprawdz czy formularz jest dobrze uzupelniony
            # filtering logic
            number_of_seats = filter_form.cleaned_data["seats"] # wybierz z formularza ilosc miejsc ktore ma miec kajak
            cargo = filter_form.cleaned_data["cargo"] # wybierz z formularza ilosc miejsc ktore ma miec kajak
            cup_holder = filter_form.cleaned_data["cup_holder"]
            color = filter_form.cleaned_data["color"]
            kajak_type = filter_form.cleaned_data["kajak_type"]
            price_per_hour = filter_form.cleaned_data["price_per_hour"]

            start_date = filter_form.cleaned_data["start_date"]
            end_date = filter_form.cleaned_data["end_date"]
            if start_date > end_date:
                start_date, end_date = end_date, start_date
            print(start_date, end_date)

            # filter main kajak queryset by number of seats
            earlier_than = Q(reservations__start_date__gte=end_date) # gte -> greater than or equal
            later_than = Q(reservations__end_date__lte=start_date) # lte -> less than or equal
            reservation_dates = earlier_than | later_than | Q(reservations__isnull=True)


            qs = qs.filter(reservation_dates)

            qs = filter_non_required_field(qs, field="seats", field_value=number_of_seats)
            qs = filter_non_required_field(qs, field="price_per_hour", field_value=price_per_hour)
            
            qs = filter_choice_field(qs, field="cargo", field_value=cargo)
            qs = filter_choice_field(qs, field="cup_holder", field_value=cup_holder)
            qs = filter_choice_field(qs, field="color", field_value=color)
            qs = filter_choice_field(qs, field="kajak_type", field_value=kajak_type)

        context = {self.context_object_name: set(qs), 'form': filter_form, 'start_date': start_date, 'end_date': end_date}
        return render(request, self.template_name, context)


class KajakDetailView(DetailView):
    model = Kajak
    template_name = "kajak_detail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        print(self.kwargs)
        data = super().get_context_data(**kwargs)
        data.update(self.kwargs)

        # start_date_obj = timezone.datetime.strptime(data["start_date"], "YYYY-mm-dd HH:MM:SSz") #TODO find proper formatting of the date
        # end_date_obj = timezone.datetime.strptime(data["end_date"], "Y-m-d H:M:Sz") #TODO find proper formatting of the date

        # time_delta  = end_date_obj - start_date_obj
        # hours_to_pay = ceil(time_delta.seconds/3600.0) + time_delta.days*24
        # price_to_pay = hours_to_pay*data["objects"].price_per_hour
        # data["price_to_pay"] = price_to_pay
        return data

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


class StatisticsViewSet(viewsets.ViewSet):
    def get_queryset(self):
        return Kajak.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        queryset = queryset.prefetch_related("reservations").annotate(num_of_reservations=Count("reservations"))
        
        serializer = StatisticsSerializer(queryset, many=True)
        return Response(serializer.data)
