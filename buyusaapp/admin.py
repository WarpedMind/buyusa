from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse,Http404,JsonResponse
from django.conf import settings
from .models import Profile, Gig, Purchase, Review, Donate, ImportData
from .views import sendmailbythread

# Register your models here.
#admin.site.register(Profile,ProfileAdmin)
admin.site.register(Gig)
admin.site.register(Purchase)
admin.site.register(Review)
admin.site.register(Donate)
#admin.site.register(ImportData,ImportDataAdmin)
#admin.site.register(ImportData,readonly_fields=('companyid','company','employees','phone','url','email','psic',
            #'brandnames','salutation','firstname','middlename','lastname',
            #'suffix','gender','titleext','ImportSource','ImportTimestamp','ImportID'))

@admin.register(ImportData)
class ImportDataAdmin(admin.ModelAdmin):
    #save_as = False
    #save_as_continue = False
    readonly_fields=('companyid','company','employees','phone','url','email','psic',
                     'brandnames','salutation','firstname','middlename','lastname',
                     'suffix','gender','titleext','ImportSource','ImportTimestamp','ImportID')
    
    change_form_template = 'importdata_admin_change.html'
    
    #def has_add_permission(self, request):
        #return False
    #def has_change_permission(self, request, obj=None):
        #return False
    def has_delete_permission(self, request, obj=None):
        return False    
        
    def add_view(request, form_url='', extra_context=None):
        return HttpResponse('<a href="/importdata/" target="_blank">Import Data!</a>')
    
    
    def get_actions(self, request):
        #actions = super().get_actions(request)
        #if 'delete_selected' in actions:
            #del actions['delete_selected']
        return []



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    actions = ['make_sendmail']
    
    def make_sendmail(self, request, queryset):
        for obj in queryset:
            email = obj.CompanyContactEmail
            sendmailbythread([email,], u'[buyusa] Please do your first login and change password',
                                 u'Please do your first login and change password：%s/firstlogin/%s' % (settings.SITE_URL,obj.LoginLink,))
        self.message_user(request, "Email sent.")
    make_sendmail.short_description = "Send mail to the user again"
    
    #def get_urls(self):
        #urls = super().get_urls()
        #my_urls = [
            #path('sendmail/', self.admin_site.admin_view(self.sendmail)),
        #]
        #return my_urls + urls

    #def sendmail(self, request):
        ##context = dict(
           ##self.admin_site.each_context(request),
           ##key=value,
        ##)
        ##return TemplateResponse(request, "admin/sendmail.html", context)
        #info = self.model._meta.app_label, self.model._meta.model_name
        #return redirect('%s_%s_changelist' % info)
    
    
