#-*- coding:utf-8 -*-

"""提供一些业务上操作fileinfo的特殊方法
"""

__author__ = 'wx'

from drs.apps.backup.models import FileInfo
from django.utils import timezone

def insert_via_info(db_table, backupctrl, filename, where_sen, *args):
    db, table = db_table.split(';')
    where_sen = '' if where_sen == None else where_sen
    fileinfo = FileInfo(Fschema=db,
                        Ftable_name=table,
                        Ffile_name=filename,
                        Fcondition=where_sen,
                        Fserver_ip='123.45.67.89',
                        Fserver_info='temp',
                        Fstatus='0')
    fileinfo.save()
