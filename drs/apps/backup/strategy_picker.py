#-*- coding:utf-8 -*-

__author__ = 'wx'

from .models import BackupCtrl
from drs.utils.logger import Logger
from django.utils import timezone
from .backup_type import AllBackup, DayBackup, MonthBackup, YearBackup, RangeBackup, ZipperBackup, ConditionBackup

logger = Logger()

class Picker(object):

    def __init__(self):
        self._data = self.__get_data()
    
    def __get_data(self):
        # Fbackup_status=0 备份状态筛选
        return BackupCtrl.objects.filter()
    
    def pick(self):
        picks = []
        for row in self._data:
            result = self.__pick(row)
            picks.append(row) if result else None
        dealed_picks = self.__deal_picks(picks)
        return dealed_picks

    def __deal_picks(self, picks):
        
        """按照数据库_表名分组, 按照优先级排序
        """

        groups = {}
        for pick in picks:
            group_name = f'{pick.Fschema};{pick.Ftable_name}'
            if group_name not in groups:
                groups[group_name] = [pick]
            else:
                # 在这里将优先级高的策略放在数组头部
                group = groups[group_name]
                priority = int(pick.Fpriority)
                cursor = len(group)
                while True:
                    if cursor is 0:
                        group = [pick] + group
                        groups[group_name] = group
                        break
                    cursor -= 1 
                    current = group[cursor]
                    current_priority = int(current.Fpriority)
                    if priority < current_priority:
                        group = group[:cursor + 1] + [pick] + group[cursor + 1:]
                        groups[group_name] = group
                        break
        return groups
                


    def __pick(self, backupctrl):
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
            result = backuptype.check(backupctrl)
            return result
        else:
            return False
