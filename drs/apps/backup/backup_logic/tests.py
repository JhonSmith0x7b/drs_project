#-*- coding:utf-8 -*-
__author__ = 'wx'

from django.test import TestCase
from drs.apps.backup.backup_logic import strategy_validator as sv
from drs.apps.backup.models import BackupCtrl
from django.conf import settings
import os
from drs.apps.backup.backup_logic.xls_reader import Reader
from drs.apps.backup.backup_logic.xls_reader import PullBackupCtrlViaXls
from drs.utils.logger import Logger
from drs.apps.backup.backup_logic.strategy_picker import Picker
from django.utils import timezone
from datetime import datetime
from drs.apps.backup.backup_logic.where_gener import Gener
from drs.apps.backup.backup_logic.backuper import FirstResponser, SecondResponser

logger = Logger()

class XlsImportTest(TestCase):
    
    """ run this test via 
        python manage.py test drs.apps.backup.tests.XlsImportTest
    """

    def setUp(self):
        f = open(os.path.join(settings.BASE_DIR, 'tests/init_data/BackupCtrl.xlsx'), 'rb')
        self._f = f

    def test_xls_import(self):
        p = PullBackupCtrlViaXls(self._f.read())
        result = Reader(p).execute()
        logger.debug(repr(result))
        logger.debug(repr(BackupCtrl.objects.all()))
        
        

class BackupCtrlTestCase(TestCase):

    """run this test via 
        python manage.py test drs.apps.backup.tests.BackupCtrlTestCase
    """
    
    def setUp(self):
        BackupCtrl.objects.create(Fschema='db', 
                                    Ftable_name='table',
                                    Ftype='6',
                                    Fsplit_field=' where eff_data > 2132131 and test = 1 ',
                                    Fbackup_status='2',
                                    Fdata_begin_date=timezone.make_aware(datetime(2018, 4, 15)),
                                    Fbackup_strategy='9',
                                    Fbackup_interval=99,
                                    Flast_date=timezone.now().date(),
                                    Fpriority='9',
                                    Fserver_ip='127.0.0.1',
                                    Fserver_info='Backup001',
                                    Fmodify_time=timezone.now())
        BackupCtrl.objects.create(Fschema='db', 
                                    Ftable_name='table',
                                    Ftype='5',
                                    Fsplit_field='eff_data',
                                    Fbackup_status='1',
                                    Fdata_begin_date=timezone.make_aware(datetime(2018, 4, 15)),
                                    Fbackup_strategy='8',
                                    Fbackup_interval=7,
                                    Flast_date=timezone.make_aware(datetime(2018, 4, 15)),
                                    Fpriority='3',
                                    Fserver_ip='127.0.0.2',
                                    Fserver_info='Backup002',
                                    Fmodify_time=timezone.now())
        BackupCtrl.objects.create(Fschema='db', 
                                    Ftable_name='table',
                                    Ftype='1',
                                    Fsplit_field='eff_data',
                                    Fbackup_status='0',
                                    Fdata_begin_date=timezone.make_aware(datetime(2018, 4, 15)),
                                    Fbackup_strategy='2',
                                    Fbackup_interval=7,
                                    Flast_date=timezone.make_aware(datetime(2018, 4, 15)),
                                    Fpriority='1',
                                    Fserver_ip='127.0.0.2',
                                    Fserver_info='Backup002',
                                    Fmodify_time=timezone.now())
        BackupCtrl.objects.create(Fschema='db', 
                                    Ftable_name='table1',
                                    Ftype='4',
                                    Fsplit_field='eff_data;20120606_20121212',
                                    Fbackup_status='2',
                                    Fdata_begin_date=timezone.make_aware(datetime(2018, 4, 15)),
                                    Fbackup_strategy='3',
                                    Fbackup_interval=7,
                                    Flast_date=timezone.now().date(),
                                    Fpriority='3',
                                    Fserver_ip='127.0.0.1',
                                    Fserver_info='Backup001',
                                    Fmodify_time=timezone.now())
        BackupCtrl.objects.create(Fschema='db', 
                                    Ftable_name='table1',
                                    Ftype='3',
                                    Fsplit_field='eff_data',
                                    Fbackup_status='1',
                                    Fdata_begin_date=timezone.make_aware(datetime(2010, 4, 15)),
                                    Fbackup_strategy='2',
                                    Fbackup_interval=7,
                                    Flast_date=timezone.make_aware(datetime(2013, 1, 1)),
                                    Fpriority='0',
                                    Fserver_ip='127.0.0.2',
                                    Fserver_info='Backup002',
                                    Fmodify_time=timezone.now())
        BackupCtrl.objects.create(Fschema='db', 
                                    Ftable_name='table1',
                                    Ftype='2',
                                    Fsplit_field='eff_data',
                                    Fbackup_status='0',
                                    Fdata_begin_date=timezone.make_aware(datetime(2017, 4, 15)),
                                    Fbackup_strategy='8',
                                    Fbackup_interval=7,
                                    Flast_date=timezone.make_aware(datetime(2018, 2, 1)),
                                    Fpriority='3',
                                    Fserver_ip='127.0.0.1',
                                    Fserver_info='Backup001',
                                    Fmodify_time=timezone.now())
        BackupCtrl.objects.create(Fschema='db1', 
                                    Ftable_name='table',
                                    Ftype='5',
                                    Fsplit_field='eff_data',
                                    Fbackup_status='2',
                                    Fdata_begin_date=timezone.make_aware(datetime(2018, 4, 15)),
                                    Fbackup_strategy='8',
                                    Fbackup_interval=7,
                                    Flast_date=timezone.make_aware(datetime(2018, 4, 15)),
                                    Fpriority='3',
                                    Fserver_ip='127.0.0.2',
                                    Fserver_info='Backup002',
                                    Fmodify_time=timezone.now())
        BackupCtrl.objects.create(Fschema='db', 
                                    Ftable_name='table',
                                    Ftype='0',
                                    Fsplit_field='eff_data',
                                    Fbackup_status='2',
                                    Fdata_begin_date=timezone.make_aware(datetime(2018, 4, 15)),
                                    Fbackup_strategy='8',
                                    Fbackup_interval=7,
                                    Flast_date=timezone.make_aware(datetime(2018, 4, 10)),
                                    Fpriority='3',
                                    Fserver_ip='127.0.0.2',
                                    Fserver_info='Backup002',
                                    Fmodify_time=timezone.now())
    
    def test_validator(self):
        test_data = BackupCtrl.objects.all()
        s = sv.CheckBackupCtrlViaModel(test_data)
        v = sv.Validator(s)
        v.execute()
    
    def test_picker(self):
        picker = Picker()
        result = picker.pick()
        print(result)
        return result
    
    def test_gener(self):
        data = self.test_picker()
        gener = Gener()
        results = []
        for key in data:
            for backupctrl in data[key]:
                result = gener.gen(backupctrl)
                results.append(result)
        print(results)
    
    def test_backuper(self):
        first = FirstResponser()
        first.set_next(SecondResponser())
        first.handle()
