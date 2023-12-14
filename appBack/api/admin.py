from django.contrib import admin
from . import models
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['ticket_number', 'name', 'phone_number']

class ToolAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

admin.site.register(models.Customer, CustomerAdmin)
