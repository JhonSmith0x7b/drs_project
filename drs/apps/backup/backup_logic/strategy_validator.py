#-*- coding:utf-8 -*-

__author__ = 'wx'

from drs.apps.backup.models import BackupCtrl
from collections import OrderedDict
from datetime import datetime
from datetime import date
from django.core.validators import validate_ipv46_address
from drs.utils.logger import Logger
from collections import Iterable

logger = Logger()


class BaseIntrospection(object):

    """基本类型验证类
    """
    
    @staticmethod
    def introspection(column_name, column, value):
        typical = column['datatype'] if 'datatype' in column else None
        max_length = column['max_length'] if 'max_length' in column else None
        is_null = column['is_null'] if 'is_null' in column else None
        if is_null and value is None:
            return True, f'{column_name} is None, but PASS!'
        if typical == 'BigAutoField':
            if not isinstance(value, int):
                return False, f'{column_name} not pass! BigAutoField type must be int, now is {type(value)}'
        elif typical == 'CharField':
            if not isinstance(value, str):
                return False, f'{column_name} not pass! CharField type must be str'
            if max_length:
                if len(value) > max_length:
                    return False, f'{column_name} not pass! CharField length {len(value)}>{max_length}'
        elif typical == 'DateTimeField':
            if not isinstance(value, datetime):
                return False, f'{column_name} not pass! DataTimeField type must be datetime.datetime, now is {type(value)}'
        elif typical == 'PositiveIntegerField':
            if not isinstance(value, int):
                return False, f'{column_name} not pass! PositiveIntegerField type must be int, now is {type(value)}'
            if value < 0:
                return False, f'{column_name} not pass! PositieIntegerField must > 0, now is {value}'
        elif typical == 'DateField':
            if not isinstance(value, date):
                return False, f'{column_name} not pass! DateField type must be datetime.date, now is {type(date)}'
        elif typical == 'GenericIPAddressField':
            if not isinstance(value, str):
                return False, f'{column_name} not pass! GenericIPAddressField type must be str, now is {type(value)}'
            try:
                validate_ipv46_address(value)
            except:
                return False, f'{column_name} not pass! GenericIPAddressField not Ipv4 or Ipv6 format.'
        else:
            return False, f'{column_name} not pass! Unknown Error.'
        return True, f'{column_name} pass!'

class FidIntrospection(BaseIntrospection):
    pass

class FschemaIntrospection(BaseIntrospection):
    pass

class Ftable_nameIntrospection(BaseIntrospection):
    pass

class FtypeIntrospection(BaseIntrospection):
    pass

class Fsplit_fieldIntrospection(BaseIntrospection):
    pass

class Fbackup_statusIntrospection(BaseIntrospection):
    pass

class Fdata_begin_dateIntrospection(BaseIntrospection):
    pass

class Fbackup_strategyIntrospection(BaseIntrospection):
    pass

class Fbackup_intervalIntrospection(BaseIntrospection):
    pass

class Flast_dateIntrospection(BaseIntrospection):
    pass

class FpriorityIntrospection(BaseIntrospection):
    pass

class Fserver_ipIntrospection(BaseIntrospection):
    pass

class Fserver_infoIntrospection(BaseIntrospection):
    pass

class Fmodify_timeIntrospection(BaseIntrospection):
    pass

class BackupCtrlMapper(object):
    
    """将model类进行映射, 以应对不同列的验证方式
    """
    
    check_report = None
    fields = BackupCtrl._meta.fields
    columns = OrderedDict([
        ('Fid', {
            'datatype': 'BigAutoField',
            'i': FidIntrospection,
        }),
        ('Fschema',{
            'datatype': 'CharField',
            'max_length': 128,
            'i': FschemaIntrospection,
        }),
        ('Ftable_name',{
            'datatype': 'CharField',
            'max_length': 128,
            'i': Ftable_nameIntrospection,
        }),
        ('Ftype',{
            'datatype': 'CharField',
            'max_length': 1,
            'i': FtypeIntrospection,
        }),
        ('Fsplit_field',{
            'datatype': 'CharField',
            'max_length': 1024,
            'i': Fsplit_fieldIntrospection,
        }),
        ('Fbackup_status',{
            'datatype': 'CharField',
            'max_length': 1,
            'i': Fbackup_statusIntrospection,
        }),
        ('Fdata_begin_date',{
            'datatype': 'DateTimeField',
            'i': Fdata_begin_dateIntrospection,
        }),
        ('Fbackup_strategy',{
            'datatype': 'CharField',
            'max_length': 1,
            'i': Fbackup_strategyIntrospection,
        }),
        ('Fbackup_interval',{
            'datatype': 'PositiveIntegerField',
            'i': Fbackup_intervalIntrospection,
        }),
        ('Flast_date',{
            'datatype': 'DateField',
            'i': Flast_dateIntrospection,
        }),
        ('Fpriority',{
            'datatype': 'CharField',
            'i': FpriorityIntrospection,
        }),
        ('Fserver_ip',{
            'datatype': 'GenericIPAddressField',
            'i': Fserver_ipIntrospection,
            'is_null': True
        }),
        ('Fserver_info',{
            'datatype': 'CharField',
            'max_length': 32,
            'i': Fserver_infoIntrospection,
        }),
        ('Fmodify_time',{
            'datatype': 'DateTimeField',
            'i': Fmodify_timeIntrospection,
        }),
    ])

    def __init__(self, model):
        
        """model的映射类, 用来进行验证
        args:
            model model实现对象
        """

        self.model = model
    
    def check(self):
        values = [getattr(self.model, field.name) for field in self.fields]
        self.check_report = self.__convert(values)
        is_s = True
        for row in self.check_report:
            if row[0] is False:
                is_s = False
                break
        return is_s
    def get_report(self):
        return self.check_report
    
    def __convert(self, values):
        if len(values) != len(self.columns):
            return False
        check_row = list(map(lambda column_key, column, value: column['i'].introspection(column_key, column, value),
                        list(self.columns.keys()),
                        list(self.columns.values()),
                        values))
        return check_row
       
class CheckBackupCtrlViaModel(object):

    """用来验证backupctrl的类, 支持传入单个与数组
    """

    def __init__(self, models):
        
        """
        args:
            models 可以传入 Iterable object(QuerySet) 或者单个 model
        """
        if not isinstance(models, Iterable):
            models = [models]
        self._models = models
    
    def do(self):
        for model in self._models:
            bcm = BackupCtrlMapper(model)
            result = bcm.check()
            logger.debug(repr(bcm.get_report()) + str(result))
            

class Validator(object):
    
    """ 策略验证的调用者
    """
    
    def __init__(self, strategy):
        self._strategy = strategy
    
    def execute(self):
        self._strategy.do()
