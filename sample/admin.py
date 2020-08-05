from django.contrib import admin
from .models import Springports,Mysqlports
# Register your models here.

class sport(admin.ModelAdmin):
    list_display = ('port','user','port','time','state')

admin.site.register(Springports,sport)
admin.site.register(Mysqlports,sport)