from django.contrib import admin

# Register your models here.
from .models import Futasok

 
@admin.register(Futasok)
class RequestDemoAdmin(admin.ModelAdmin):
  list_display = [field.name for field in Futasok._meta.get_fields()]