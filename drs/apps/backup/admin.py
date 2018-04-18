from django.contrib import admin

from .models import BackupCtrl
from .models import FileInfo

__author__ = 'bchen'

class DRSAdmin(admin.AdminSite):
    admin.AdminSite.site_title = u'Disaster Recovery System'
    admin.AdminSite.site_header = u'drs 管理系统'


@admin.register(BackupCtrl)
class BackupCtrlAdmin(admin.ModelAdmin):
    # def script_create(self, obj):
    #     return "%s" % obj.Fscript_create[0:100]
    # script_create.short_description = u'创建外表脚本'
    #
    # def script_insert(self, obj):
    #     return "%s" % obj.Fscript_insert[0:100]
    # script_insert.short_description = u'加载数据脚本'

    list_display = ('Fschema', 'Ftable_name', 'Ftype', 'Fsplit_field', 'Fbackup_status',
                    'Fdata_begin_date', 'Fbackup_strategy', 'Fserver_ip', 'Fserver_info',
                    'Fbackup_interval', 'Flast_date', 'Fpriority', 'Fmodify_time')
    list_per_page = 20
    search_fields = ('Fschema', 'Ftable_name',  'Flast_date')
    list_filter = ('Fschema', 'Ftable_name', 'Ftype', 'Fbackup_status', 'Flast_date', 'Fmodify_time')
    date_hierarchy = 'Fmodify_time'


@admin.register(FileInfo)
class FileInfoAdmin(admin.ModelAdmin):
    list_display = ('Fschema', 'Ftable_name', 'Ffile_name', 'Fcondition',
                    'Ffile_version', 'Frecord_num', 'Fbytes', 'Fmd5',
                    'Fstatus', 'Fserver_ip','Fserver_info', 'Frebackup',
                    'Fdate', 'Ftime')
    list_per_page = 20
    search_fields = ('Fschema', 'Ftable_name', 'Fdate')
    list_filter = ('Fschema', 'Ftable_name', 'Fstatus', 'Fdate', 'Frebackup')




admin_site = DRSAdmin(name='management')
