from django.contrib import admin
from .models import Entry
from .models import EntrySummarry
# Register your models here.

from django.db.models import Count, Sum, DateTimeField, Min, Max
from django.db.models.functions import Trunc

from import_export.admin import ImportExportModelAdmin
from django.urls import include,path
from django.http import HttpResponse, HttpResponseRedirect

#call import export
# # @admin.register(Entry)
# class EntryDATAAdmin(ImportExportModelAdmin):
#     pass

class EntryAdmin(ImportExportModelAdmin):
    fieldsets = [
        (None,  {'fields': ['text']}),
    ]
    list_display = ('text', 'pub_date','is_readed')
    list_filter = ['pub_date']
    search_fields = ['text']
    change_list_template = 'admin/entry_change_list_view.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('immortal/', self.set_immortal),
            path('mortal/', self.set_mortal),
        ]
        return my_urls + urls

    def set_immortal(self, request):
        Entry.objects.all().update(is_readed=True)
        self.message_user(request, "All heroes are now immortal")
        return HttpResponseRedirect("../")

    def set_mortal(self, request):
        Entry.objects.all().update(is_readed=False)
        self.message_user(request, "All heroes are now mortal")
        return HttpResponseRedirect("../")

@admin.register(EntrySummarry)
class EntrySummarryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/entry_summary_change_list.html'
    date_hierarchy = 'pub_date'

    # list_filter = (
    #     'pub_date',
    # )

    def get_next_in_date_hierarchy(self, request, date_hierarchy):
	    if date_hierarchy + '__day' in request.GET:
	        return 'hour'
	    if date_hierarchy + '__month' in request.GET:
	        return 'day'
	    if date_hierarchy + '__year' in request.GET:
	        return 'week'
	    return 'month'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        print("response====",response, response.context_data,request.GET)
        # try:
        #     qs = response.context_data['cl'].queryset
        # except (AttributeError, KeyError):
        #     return response
        qs = Entry.objects.all()
        metrics = {
            'total': Count('id'),
            'total_sales': Sum('id'),
        }
        response.context_data['summary'] = list(
            qs
            .values('text','id','pub_date')
            .annotate(**metrics)
            .order_by('-pub_date')
        )
        response.context_data['summary_total'] = dict(
            qs.aggregate(**metrics)
        )

        #for making graph view
        period = self.get_next_in_date_hierarchy(
            request,
            self.date_hierarchy
        )
        print("period=======",period)
        response.context_data['period'] = period

        summary_over_time = qs.annotate(
            period=Trunc(
                'pub_date',
                'day',
                output_field=DateTimeField(),
            ),).values('period').annotate(total=Sum('id')).order_by('-pub_date')
        summary_range = summary_over_time.aggregate(
            low=Min('id'),
            high=Max('id'),
        )
        high = summary_range.get('high', 0)
        low = summary_range.get('low', 0)
        response.context_data['summary_over_time'] = [{
            'period': x['period'],
            'total': x['total'] or 0,
            'pct': \
               ((x['total'] or 0) - low) / (high - low) * 100 
               if high > low else 0,
        } for x in summary_over_time]
        print("response======",response)
        return response


    


admin.site.register(Entry,EntryAdmin)
admin.site.site_header = "Diary Adminstration"
admin.site.index_title = "Diary Adminstration"