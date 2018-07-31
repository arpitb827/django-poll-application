from django.contrib import admin

from django.contrib.admin import AdminSite

from .models import Epic, Event, EventHero, EventVillain
# Register your models here.

class EventAdminSite(AdminSite):
	site_header = "CookBook Event Admin"
	site_title = "CookBook Event Portal"
	index_title = "Welcome to CookBook Event Portal"

event_admin_site = EventAdminSite(name='event_admin')

event_admin_site.register(Epic)
event_admin_site.register(Event)
event_admin_site.register(EventHero)
event_admin_site.register(EventVillain)

#change header and base views
admin.site.site_header = "CookBook Admin"
admin.site.site_title = "CookBook Admin Portal"
admin.site.index_title = "Welccome to CookBook Admin"
admin.site.register(Epic)
admin.site.register(Event)
admin.site.register(EventHero)
admin.site.register(EventVillain)

