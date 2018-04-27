#-*- coding:utf-8 -*-

from drs.apps.backup.backup_logic.backup_type import AllBackup, DayBackup, MonthBackup, YearBackup, RangeBackup, ZipperBackup, ConditionBackup

__author__ = 'wx'

class Gener(object):
    
    """where条件生成类, 根据backupType进行不同的组装与生成
    """

    def __init__(self):
        pass
        
    def gen(self, backupctrl):
        ftype = backupctrl.Ftype
        backuptype = None
        if ftype == '0':
            backuptype = AllBackup()
        elif ftype == '1':
            backuptype = DayBackup()
        elif ftype == '2':
            backuptype = MonthBackup()
        elif ftype == '3':
            backuptype = YearBackup()
        elif ftype == '4':
            backuptype = RangeBackup()
        elif ftype == '5':
            backuptype = ZipperBackup()
        elif ftype == '6':
            backuptype = ConditionBackup()
        else:
            pass
        if backuptype:
            result = backuptype.gen(backupctrl)
            return result
        else:
            return False
