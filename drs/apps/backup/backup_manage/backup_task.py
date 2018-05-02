#!/usr/bin/env python
# encoding: utf-8
# author: bchen
# license: (C) Copyright 2018-2019, Shanghai Stock Exchange.
# file: backup_task.py
# time:
# desc: 任务， 一个task对应一个文件
import time
import os
#from drs.utils.logger import Logger
from drs.settings import export_conf, back_server_conf
import random
from datetime import datetime
from datetime import date
from drs.apps.backup.models import DataDict,FileInfo
#from drs_app.tools.logger_color import set_color

class TestCase1():
    def FileInfo1(self):
        FileInfo.objects.create(Fschema='PD_DATA',
                                Ftable_name='SEC_OPT_VOLATILITY',
                                Ffile_name='PD_DATA.SEC_OPT_VOLATILITY.20161230.txt',
                                Ffile_version='N',
                                Fcondition="WHERE TRADE_DATE='20161230'",
                                Frebackup='N',
                                Frecord_num='9',
                                Fbytes=99,
                                Fmd5='',
                                Fserver_ip='9',
                                Fserver_info='127.0.0.1',
                                Fstatus='1',
                                Fdate=date.today(),
                                Ftime=datetime.now())
        FileInfo.objects.create(Fschema='PD_DATA',
                                Ftable_name='SEC_OPT_QUOT',
                                Ffile_name='PD_DATA.SEC_OPT_QUOT.20161230.txt',
                                Ffile_version='N',
                                Fcondition="WHERE TRADE_DATE='20161230'",
                                Frebackup='N',
                                Frecord_num='9',
                                Fbytes=99,
                                Fmd5='',
                                Fserver_ip='9',
                                Fserver_info='127.0.0.1',
                                Fstatus='1',
                                Fdate=date.today(),
                                Ftime=datetime.now())
        DataDict.objects.create(Schemaname='PD_DATA',
                                Tablename='SEC_OPT_VOLATILITY',
                                Columnid='1',
                                Columnname='TRADE_DATE',
                                Commentstring='',
                                Columntype='DATE',
                                Charlength='8',
                                Elktype='TIMESTAMP',
                                Elkpartition='1',
                                Fstatus='0')
        DataDict.objects.create(Schemaname='PD_DATA',
                                Tablename='SEC_OPT_VOLATILITY',
                                Columnid='2',
                                Columnname='OPT_CODE',
                                Commentstring='',
                                Columntype='CHAR(8)',
                                Charlength='8',
                                Elktype='CHAR(8)',
                                Elkpartition='1',
                                Fstatus='0')
        DataDict.objects.create(Schemaname='PD_DATA',
                                Tablename='SEC_OPT_QUOT',
                                Columnid='1',
                                Columnname='TRADE_DATE',
                                Commentstring='',
                                Columntype='DATE',
                                Charlength='8',
                                Elktype='TIMESTAMP',
                                Elkpartition='1',
                                Fstatus='0')
        DataDict.objects.create(Schemaname='PD_DATA',
                                Tablename='SEC_OPT_QUOT',
                                Columnid='2',
                                Columnname='OPT_CODE',
                                Commentstring='',
                                Columntype='CHAR(8)',
                                Charlength='8',
                                Elktype='CHAR(8)',
                                Elkpartition='1',
                                Fstatus='0')
class ExportJob:
    def __init__(self, file_info=None):
        self.file_info = file_info
        # while count:
        self.alls=FileInfo.objects.filter(Fstatus='1').values_list('Fschema','Ftable_name','Ffile_name','Fcondition','Fserver_info')[0]
        self.Fschema=self.alls[0]
        self.Ftable_name = self.alls[1]
        self.Ffile_name = self.alls[2]
        self.Fcondition=self.alls[3]
        self.Fserver_info = self.alls[4]
        self.column_names=''
        self.column_name_type=''
        self.concat_drop()
        num=0
        Columnnames=DataDict.objects.filter(Tablename=self.Ftable_name).filter(Schemaname=self.Fschema).order_by('Columnid').values_list('Columnname',flat=True)
        Elktypes = DataDict.objects.filter(Tablename=self.Ftable_name).filter(Schemaname=self.Fschema).order_by('Columnid').values_list('Elktype', flat=True)
        while num < DataDict.objects.filter(Tablename=self.Ftable_name ).filter(Schemaname=self.Fschema).count():
            if num==0:
                comm=''
            else:
                comm=','
            self.column_name_type= self.column_name_type +'\n'+comm+ Columnnames[num]+' '*5+Elktypes[num]
            self.column_names = self.column_names + '\n' + comm + Columnnames[num]
            num = num+1
        self.concat_create()
        self.concat_insert()
        BASE_DIR = os.path.dirname(__file__)
        TEXT_DIR = os.path.join(BASE_DIR, 'create_insert/')
        NAME_TEXT_DIR=TEXT_DIR+self.Fschema+'_'+self.Ftable_name+'.sql'
        concat_text=self.drop + '\n' + self.create + '\n'*3 +self.insert
        with open(NAME_TEXT_DIR,'w',encoding='GBK') as create_text:
            create_text.write(concat_text)

    def concat_drop(self):
        self.table = 'PD_GDSFILE.'+ self.Fschema+'_'+self.Ftable_name
        self.drop = 'DROP FOREIGN TABLE IF EXISTS '
        self.drop += self.table + ';'
    def concat_create(self):
        self.create = 'CREATE FOREIGN TABLE ' + self.table + '('+self.column_name_type+'\n'
        self.create += ')server gsmpp_server options(location \'gsfs://' + \
                       self.Fserver_info+ ':' + str(export_conf['gds']['port'])+\
                       '\',\n' + 'format \'TEXT\',encoding \'GBK\',delimiter \'|\',null \'\',NOESCAPING \'ON\')write only;'

    def concat_insert(self):
        self.insert = 'START TRANSACTION;\n'+'INSERT INTO ' + self.table + '\nSELECT '+self.column_names+'\n'
        self.insert += 'FROM ' + self.Fschema + '.' + self.Ftable_name + ' \n'
        self.insert += self.Fcondition + ';\nEND;'

    def do_export(self):
            cmd_ssh = 'ssh ' + back_server_conf[self.file_info.Fserver_info]['user'] + '@' + \
                  self.file_info.Fserver_ip + ' '
            cmd += 'gsql -h ' + export_conf['elk_cn_host'][int(random.random() * len(export_conf['elk_cn_host']))]
            cmd += ' -p ' + export_conf['gsql']['port'] + ' -d ' + export_conf['gsql']['database']
            cmd += ' -U ' + export_conf['gsql']['user'] + ' -W ' + export_conf['gsql']['password'] + ' -c \"'
            self.logger.info(set_color('[' + self.file_info.Fserver_info + ']') +
                             set_color(self.create, 'yellow'))
            self.logger.info(set_color('[' + self.file_info.Fserver_info + ']') +
                             set_color(self.insert, 'yellow'))
            self.logger.info(set_color('[' + self.file_info.Fserver_info + ']') +
                             set_color(self.drop, 'yellow'))
            self.logger.info(set_color('[' + self.file_info.Fserver_info + ']') + cmd)
            self.update_fileinfo(update_status=1)
            return True

