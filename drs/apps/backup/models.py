from django.db import models

__author__ = 'bchen'

# Create your models here.
from django.utils import timezone


class BackupCtrl(models.Model):
    class Meta:
        db_table = u'backup_ctrl'
        verbose_name = u'备份控制'
        verbose_name_plural = u'备份控制'
        ordering = ['-Fmodify_time']

    BACKUP_TYPE = (
        ('0', u'全量'),
        ('1', u'按日切片'),
        ('2', u'按月切片'),
        ('3', u'按年切片'),
        ('4', u'指定区间'),
        ('5', u'拉链表'),
        ('6', u'指定条件'),
    )
    BACKUP_STATUS = (
        ('0', u'备份失败'),
        ('1', u'备份成功'),
        ('2', u'备份中'),
    )
    Fid = models.BigAutoField(primary_key=True, verbose_name='ID')
    Fschema = models.CharField(max_length=128, default='', verbose_name=u'库名')
    Ftable_name = models.CharField(max_length=128, default='', verbose_name=u'表名')
    Ftype = models.CharField(max_length=1, default='0', choices=BACKUP_TYPE, verbose_name=u'备份类型')
    Fsplit_field = models.CharField(max_length=1024, blank=True, default='', verbose_name=u'拆分条件')
    Fbackup_status = models.CharField(max_length=1, default='0', choices=BACKUP_STATUS, verbose_name=u'备份状态')
    Fdata_begin_date = models.DateTimeField(default=timezone.datetime(1990,11,26), verbose_name=u'数据开始日期')
    Fbackup_strategy = models.CharField(max_length=1, default='0', verbose_name=u'更新策略')
    Fbackup_interval = models.PositiveIntegerField(default=1, verbose_name=u'备份时间间隔（天）')
    Flast_date = models.DateField(default=timezone.datetime(1990,11,26), verbose_name=u'最后一次备份日期')
    Fpriority = models.CharField(max_length=1, default='0', verbose_name=u'优先级')
    Fserver_ip = models.GenericIPAddressField(null=True, verbose_name=u'备份服务器IP地址')
    Fserver_info = models.CharField(default='Backup001', max_length=32, verbose_name=u'服务器描述')
    Fmodify_time = models.DateTimeField(default=timezone.now, verbose_name=u'变更时间')


class FileInfo(models.Model):
    class Meta:
        db_table = u'file_info'
        verbose_name = u'文件信息'
        verbose_name_plural = u'文件信息'
        ordering = ['-Fdate']

    EXPORT_STATUS = (
        ('0', u'导出失败'),
        ('1', u'导出成功'),
        ('2', u'导出中'),
    )

    Fid = models.BigAutoField(primary_key=True, verbose_name='ID')
    Fschema = models.CharField(max_length=128, default='', verbose_name=u'库名')
    Ftable_name = models.CharField(max_length=128, default='', verbose_name=u'表名')
    Ffile_name = models.CharField(max_length=255, default='', verbose_name=u'文件名')
    Ffile_version = models.CharField(max_length=1, default='N', verbose_name=u'文件版本')
    Fcondition = models.CharField(max_length=1024, default='', verbose_name=u'导出条件')
    Frebackup = models.CharField(max_length=1, default='N', verbose_name=u'是否需要重新备份')
    Frecord_num = models.PositiveIntegerField(default=0, verbose_name=u'记录条数')
    Fbytes = models.PositiveIntegerField(default=0, verbose_name=u'文件大小')
    Fmd5 = models.CharField(max_length=32, default='', verbose_name=u'md5')
    Fserver_ip = models.GenericIPAddressField(null=True, verbose_name=u'备份服务器IP地址')
    Fserver_info = models.CharField(default='Backup001', max_length=32, verbose_name=u'服务器描述')
    Fstatus = models.CharField(max_length=1, default='0', choices=EXPORT_STATUS, verbose_name=u'导出状态')
    Fdate = models.DateField(auto_now=True, verbose_name=u'生成日期')
    Ftime = models.TimeField(auto_now=True, verbose_name=u'生成时间')
