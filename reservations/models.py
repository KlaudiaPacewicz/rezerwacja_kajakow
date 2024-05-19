from datetime import timedelta
from enum import Enum
from math import ceil
from django.db import models
from django.forms import ValidationError
from django.utils import timezone

# Create your models here.

class KajakType(Enum):
    SPORT = "sport"
    RECREATIONAL = "recreational"
    KIDS = "kids"

    @classmethod
    def choices(cls):
        return [(i.name, i.value) for i in cls]
    


class Kajak(models.Model):

    KAJAK_COLORS_CHOICES = [("RED", "red"), ("GREEN", "green")]

    seats = models.PositiveSmallIntegerField()
    color = models.CharField(choices=KAJAK_COLORS_CHOICES, max_length=16)
    cargo = models.BooleanField(default=False)
    cup_holder = models.BooleanField(default=False)
    kajak_type = models.CharField(choices=KajakType.choices(), max_length=16)
    price_per_hour = models.DecimalField(decimal_places=2, max_digits=5) #od 000.00 do 999.99

    def __str__(self):
        return f"{self.id}/{self.seats}/{self.kajak_type}/{self.price_per_hour}"



class Klient(models.Model):
    mail = models.EmailField(unique=True)
    phone = models.CharField(max_length=16)
    birth_day = models.DateField()

    def __str__(self):
        return f"{self.id}/{self.mail}"
    

class Rezerwacja(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE)
    kajak = models.ForeignKey(Kajak, on_delete=models.PROTECT, related_name="reservations")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return f"{self.klient.mail}/{self.kajak}"

    def save(self, *args, **kwargs):
        hours_to_pay = 100
        if self.end_date is not None:
            time_delta: timedelta = self.end_date - self.start_date
            hours_to_pay = ceil(time_delta.seconds/3600.0) + time_delta.days*24
        #TODO calculate hours from start to end
        self.price = self.kajak.price_per_hour*hours_to_pay
        super(Rezerwacja, self).save(*args, **kwargs)


# #select_related
# {"date_created": jakas data, "klient": {"id": 1, "mail": jakis mail...}, "kajak": 1, "price":12.42}


# #prefetch_related

# n+1 problem


# uczniowie = Uczen.objects.all() # +1 zapytan

# for uczen in uczniowie: # n zapytan
#     print(uczen)
#     print(uczen.szkola.name) # <- zapytanie do bazy danych

# uczniowie = Uczen.objects.all().select_related("szkola") # 1 zapytanie

# for uczen in uczniowie: 
#     print(uczen)
#     print(uczen.szkola.name) # <- juz zostaloa zrobione w select_related