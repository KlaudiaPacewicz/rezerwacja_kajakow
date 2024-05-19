from django.contrib import admin

from reservations.models import Kajak, Klient, Rezerwacja

# Register your models here.

class KajakAdmin(admin.ModelAdmin):
    fields = ["id", "seats", "color", "cargo", "cup_holder", "kajak_type", "price_per_hour"]
    list_display = ["id", "seats", "color", "cargo", "cup_holder", "kajak_type", "price_per_hour"]
    readonly_fields = ["id",]

class KlientAdmin(admin.ModelAdmin):
    fields = ["mail", "phone", "birth_day"]
    list_display = ["mail", "phone", "birth_day"]

class RezerwacjaAdmin(admin.ModelAdmin):
    field = ["id", "date_created", "klient", "kajak", "price"]
    list_display = ["id", "date_created", "klient", "kajak", "price"]
    readonly_fields = ["id", "price", "date_created"]


admin.site.register(Kajak, KajakAdmin)
admin.site.register(Klient, KlientAdmin)
admin.site.register(Rezerwacja, RezerwacjaAdmin)

