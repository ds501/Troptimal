from django.contrib import admin
from troptimal_app.models import trop_request,attraction,attraction_pair,output

class TropReqAdmin(admin.ModelAdmin): #or StackedInline
    model = trop_request #The model connected
    extra = 3 #enough space for three extra Rates

class AttractionsAdmin(admin.ModelAdmin):
    model = attraction
    extra = 3

class Attractions_pairsAdmin(admin.ModelAdmin):
    model = attraction_pair
    extra = 3

class AdminOutput(admin.ModelAdmin):
    model = output
    extra = 3

admin.site.register(trop_request, TropReqAdmin)
admin.site.register(attraction, AttractionsAdmin)
admin.site.register(attraction_pair, Attractions_pairsAdmin)
admin.site.register(output, AdminOutput)