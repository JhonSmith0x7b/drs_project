#-*- coding:utf-8 -*-

__author__ = 'wx'

from .models import BackupCtrl
from drs.utils.logger import Logger
from datetime import timedelta, datetime, date
from django.utils import timezone
from drs.config import DevelopeConfig as config
from dateutil.relativedelta import relativedelta
import calendar

logger = Logger()

class BaseBackupType(object):
    
    today = timezone.now()   #今天的日期, datetime 类型
    yesterday = timezone.now() - timedelta(days=1)   #昨天的日期, datetime 类型
    convertdata = lambda *args: datetime.strftime(args[1], config.dateformat) #将时间转换成sql中的时间格式

    def __init__(self):
        pass

    def check(self, backupctrl):
        return False
    
    def gen(self, backupctrl):
        return None 
    

class AllBackup(BaseBackupType):
    
    """全量表

    check(backupctrl)
        主要验证备份间隔
    gen(backupctrl)
        全量表备份无where条件, 返回大于等于数据开始时间的数据
    """
    
    def check(self, backupctrl):
        last_date = backupctrl.Flast_date
        backup_interval = backupctrl.Fbackup_interval
        yesterday = self.yesterday.date()
        delta = timedelta(backup_interval)
        next_date = last_date + delta
        if yesterday < next_date:
            return False
        return True
    
    def gen(self, backupctrl):
        fdata_begin_date = backupctrl.Fdata_begin_date
        fsplit_field = backupctrl.Fsplit_field
        sql_date = self.convertdata(fdata_begin_date)
        return f' where  {fsplit_field} >= {sql_date} '

class DayBackup(BaseBackupType):
    
    """按日切片

    check(backupctrl)
        昨天大于最后备份时间
    gen(backupctrl)
        时间范围 数据开始时间与上一次备份时间中较大的时间到昨天为止, 每一天一句sql
    """

    def check(self, backupctrl):
        flast_date = backupctrl.Flast_date
        yesterday = self.yesterday.date()
        if yesterday <= flast_date:
            return False 
        return True
    
    def gen(self, backupctrl):
        flast_date = backupctrl.Flast_date
        fdata_begin_date = backupctrl.Fdata_begin_date.date()
        fsplit_field = backupctrl.Fsplit_field
        begin_date = None
        begin_date = flast_date if flast_date >= fdata_begin_date else fdata_begin_date
        yesterday = self.yesterday.date()
        results = []
        if yesterday < begin_date:
            return None
        else:
            next_date = begin_date
            while True:
                sql_date = self.convertdata(next_date)
                sql = f' where {fsplit_field} = {sql_date} '
                results.append(sql)
                if next_date == yesterday:
                    break
                else:
                    next_date += timedelta(days=1)
        return results

class MonthBackup(BaseBackupType):
    
    """按月切片
    
    check(backupctrl)
        判断flast_date时间小于上个月

    gen(backupctrl)
        时间范围 最后备份或数据开始时间, 到上个月为止, 每个月生成一条sql 大于等于月初, 小于等于月末
    """
    
    def check(self, backupctrl):
        flast_date = backupctrl.Flast_date
        flast_month = flast_date.replace(day=1)
        now_month = self.yesterday.date().replace(day=1)
        if now_month <= flast_month:
            return False
        return True

    def gen(self, backupctrl):
        fsplit_field = backupctrl.Fsplit_field
        flast_month = backupctrl.Flast_date.replace(day=1)
        fdata_begin_month = backupctrl.Fdata_begin_date.date().replace(day=1)
        yesterday_month = (self.yesterday.date() - relativedelta(months=1)).replace(day=1)
        results = []
        begin_month = flast_month if flast_month >= fdata_begin_month else fdata_begin_month
        if yesterday_month < begin_month:
            return None
        else:
            next_month = begin_month
            while True:
                month_range = calendar.monthrange(next_month.year, next_month.month)[1]
                sql_date_begin = self.convertdata(next_month.replace(day=1))
                sql_date_end = self.convertdata(next_month.replace(day=month_range))
                sql = f' where {fsplit_field} >= {sql_date_begin} and {fsplit_field} <= {sql_date_end} '
                results.append(sql)
                if next_month == yesterday_month:
                    break
                else:
                    next_month += relativedelta(months=1)
        return results

class YearBackup(BaseBackupType):
    
    """按年切片

    check(backupctrl)
        如果上次备份时间小于去年, 则通过检测
    
    gen(backupctrl)
        上次备份时间距去年, 每一年一条sql, 大于等于 1月1日 小于等于 12月31日
    """

    def check(self, backupctrl):
        flast_date = backupctrl.Flast_date
        flast_year = flast_date.year
        now_year = self.yesterday.date()
        last_year = (now_year - relativedelta(years=1)).year
        if last_year <= flast_year:
            return False
        return True
    
    def gen(self, backupctrl):
        fsplit_field = backupctrl.Fsplit_field
        fdata_begin_date = backupctrl.Fdata_begin_date.date().replace(day=1, month=1)
        flast_date = backupctrl.Flast_date.replace(day=1, month=1)
        last_year = (self.yesterday.date() - relativedelta(years=1)).replace(day=1, month=1)
        begin_year = flast_date if flast_date >= fdata_begin_date else fdata_begin_date
        results = []
        if begin_year >= last_year:
            return None
        else:
            next_year = begin_year
            while True:
                sql_date_begin = self.convertdata(next_year.replace(day=1, month=1))
                sql_date_end = self.convertdata(next_year.replace(day=31, month=12))
                sql = f' where {fsplit_field} >= {sql_date_begin} and {fsplit_field} <= {sql_date_end} '
                results.append(sql)
                if next_year == last_year:
                    break
                else:
                    next_year += relativedelta(years=1)
        return results
        

class RangeBackup(BaseBackupType):
    
    """指定区间
        指定区间类型特别约定
            Fsplit_field 格式 condition;20180410_20180420 
                                条件   ;开始日期_结束日期

        check(backupctrl)
            pass
        gen(backupctrl)
            根据特殊约定拆分字符串, 拼装出sql
    """

    def check(self, backupctrl):
        return True
    
    def gen(self, backupctrl):
        fsplit_field = backupctrl.Fsplit_field
        try:
            condition, dates = fsplit_field.split(';')
            begin_date, end_date = dates.split('_')
            sql = f' where  {condition} >= {begin_date} and {condition} <= {end_date} '
            return sql
        except:
            return False

class ZipperBackup(BaseBackupType):
    
    """拉链表

    check(backupctrl)
        pass
    
    gen(backupctrl)
        拆分条件在昨天之前的备份一份, 在昨天之后的, 备份一份文件
    """
    
    def check(self, backupctrl):
        return True
    
    def gen(self, backupctrl):
        fsplit_field = backupctrl.Fsplit_field
        fdata_begin_date = backupctrl.Fdata_begin_date.date()
        flast_date = backupctrl.Flast_date
        yesterday = self.yesterday.date()
        begin_date = flast_date if flast_date > fdata_begin_date else fdata_begin_date
        results = []
        if begin_date > yesterday:
            return None 
        else:
            sql = f' where {fsplit_field} >= {begin_date} and {fsplit_field} <= {yesterday} '
            results.append(sql)
            sql = f' where {fsplit_field} > {yesterday} '
            results.append(sql)
        return results

class ConditionBackup(BaseBackupType):
    
    """指定条件

    check(backupctrl)
        pass
    gen(backupctrl)
        直接返回条件
    """

    def check(self, backupctrl):
        return True
    
    def gen(self, backupctrl):
        fsplit_field = backupctrl.Fsplit_field
        return fsplit_field