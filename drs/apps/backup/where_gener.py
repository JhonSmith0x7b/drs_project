#-*- coding:utf-8 -*-

from .backup_type import AllBackup, DayBackup, MonthBackup, YearBackup, RangeBackup, ZipperBackup, ConditionBackup

__author__ = 'wx'

class Gener(object):
    
    """where条件生成类, 根据backupType进行不同的组装与生成
    """

    def __init__(self, groups):
        self._groups = groups
    
    def gen(self):
        for key in self._groups:
            results = []
            for backupctrl in self._groups[key]:
                result = self.__gen(backupctrl)
                if isinstance(result, list):    #返回复数sql为数组, 单独sql为对象
                    results += result
                else:
                    results.append(result)
            self._groups[key] = results
        print(self._groups)

    def __gen(self, backupctrl):
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
