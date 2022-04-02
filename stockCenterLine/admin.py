from django.contrib import admin



# class UserAdmin(admin.ModelAdmin):
#     fields = ['user_id', 'name']
from stockCenterLine.models import Setting, Monitoring

admin.site.register(Setting)
admin.site.register(Monitoring)
