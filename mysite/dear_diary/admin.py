from django.contrib import admin
from .models import Entry
# Register your models here.

class EntryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    list_display = ('text', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['text']

admin.site.register(Entry,EntryAdmin)