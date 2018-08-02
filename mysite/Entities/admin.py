from django.contrib import admin

from django.contrib.admin import AdminSite

from .models import Category, Origin, Hero, Villain
from django.db.models import Count, Sum, DateTimeField, Min, Max
from django.http import HttpResponse, HttpResponseRedirect
import csv

from django import forms
from django.contrib.auth.models import User, Group
from django.urls import include,path, reverse

from django.shortcuts import render, redirect
from django.utils.html import format_html

from .forms import PromiseForm
# Register your models here.

class CsvImportForm(forms.Form):
    csv_file = forms.FileField()

class EntityAdminSite(AdminSite):
    site_header = "CookBook Entity Admin"
    site_title = "CookBook Entity Portal"
    index_title = "Welcome to CookBook Entity Portal"

entity_admin_site = EntityAdminSite(name='entity_admin')

entity_admin_site.register(Category)
entity_admin_site.register(Origin)
entity_admin_site.register(Hero)
entity_admin_site.register(Villain)

@admin.register(Origin)
class OriginAdmin(admin.ModelAdmin):
    change_list_template = "Entities/import_origin_data.html"
    list_display = ("name", "hero_count", "villain_count")

    
    # #calc field way first
    # def hero_count(self, obj):
    #   return obj.hero_set.count()

    # def villain_count(self, obj):
    #   return obj.villain_set.count()

    #other method
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
        _hero_count=Count("hero", distinct=True),
        _villain_count=Count("villain", distinct=True),
        )
        return queryset

    def hero_count(self, obj):
        return obj._hero_count
    def villain_count(self, obj):
        return obj._villain_count

    hero_count.admin_order_field = '_hero_count'
    villain_count.admin_order_field = '_villain_count'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
                path('import-csv/', self.import_csv),
        ]
        return my_urls + urls
    
    def import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            reader = csv.reader(csv_file)
            # Create Hero objects from passed in data
            # ...
            self.message_user(request, "Your csv file has been imported")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "admin/csv_form.html", payload
            )

@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    change_list_template = "Entities/heroes_changelist.html"

    actions = ["mark_immortal", "export_as_csv"]
    class IsVeryBenevolentFilter(admin.SimpleListFilter):
        title = 'is_very_benevolent'
        parameter_name = 'is_very_benevolent'
        
        def lookups(self, request, model_admin):
            return (
            ('Yes', 'Yes'),
            ('No', 'No'),
            )
        def queryset(self, request, queryset):
            value = self.value()
            if value == 'Yes':
                return queryset.filter(benevolence_factor__gt=75)
            elif value == 'No':
                return queryset.exclude(benevolence_factor__gt=75)
            return queryset

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.xls'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
        return response

    def mark_immortal(self, request, queryset):
        queryset.update(is_immortal=True)

    list_display = ("name", "is_immortal", "category", "origin", "is_very_benevolent","account_actions")
    list_filter = ("is_immortal", "category", "origin",IsVeryBenevolentFilter)
    readonly_fields = ('account_actions',)

    def is_very_benevolent(self, obj):
        return obj.benevolence_factor > 75
    is_very_benevolent.boolean = True # to show icons
    export_as_csv.short_description = "Export Rows"

    def get_actions(self, request):
        """Delete the actions"""
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def process_mortal(self, request, hero_id, *args, **kwargs):
        print("request==========,hero_id==",request,self.model, hero_id)
        self.model.objects.all().filter(id=hero_id).update(is_immortal=True)
        self.message_user(request, "Hero {} are now mortal".format(hero_id))
        return HttpResponseRedirect("../")

    def process_imortal(self , request, hero_id, *args, **kwargs):
        self.model.objects.all().filter(id=hero_id).update(is_immortal=False)
        self.message_user(request, "Hero {} are now immortal".format(hero_id))
        return HttpResponseRedirect("../")
        # form = PromiseForm()
        # payload = {"form": form}
        # return render(request, 'Entities/a_test.html',payload)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('immortal/', self.set_immortal),
            path('mortal/', self.set_mortal),
            ]
        custom_urls = [
            path(
                '<int:hero_id>/mortal',
                self.admin_site.admin_view(self.process_mortal),
                name='hero-mortal',
            ),
           path(
                '<int:hero_id>/imortal',
                self.admin_site.admin_view(self.process_imortal),
                name='hero-imortal',
            ),
        ]
        return custom_urls + my_urls + urls

    def set_immortal(self, request):
        self.model.objects.all().update(is_immortal=True)
        self.message_user(request, "All heroes are now immortal")
        return HttpResponseRedirect("../")

    def set_mortal(self, request):
        self.model.objects.all().update(is_immortal=False)
        self.message_user(request, "All heroes are now mortal")
        return HttpResponseRedirect("../")

    def account_actions(self, obj):
        print("calling account_actions")
        return format_html(
            '<a class="button call_popup" href="{}">Make Mortal</a>&nbsp;'
            '<a class="button" href="{}">Make Imortal</a>',
            reverse('admin:hero-mortal', args=[obj.pk]),
            reverse('admin:hero-imortal', args=[obj.pk]),)
            # reverse('', args=[obj.pk]),
            # reverse('', args=[obj.pk]))
    account_actions.short_description = "Account Actions"
    account_actions.allow_tags = True


#change header and base views
admin.site.site_header = "CookBook Admin"
admin.site.site_title = "CookBook Admin Portal"
admin.site.index_title = "Welccome to CookBook Admin"
admin.site.register(Category)
# admin.site.register(Origin)
# admin.site.register(Hero)
admin.site.register(Villain)



#to remove default models
# admin.site.unregister(User)
# admin.site.unregister(Group)


