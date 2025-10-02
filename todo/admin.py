from django.contrib import admin
from .models import ToDo

class ToDoAdmin(admin.ModelAdmin):
    readonly_fields = ('creation_date', )

admin.site.register(ToDo, ToDoAdmin)
