#-*- coding:utf-8 -*-
__author__ = 'wx'

from .models import BackupCtrl
import xlrd
from django.utils import timezone
from datetime import datetime
from collections import OrderedDict
import ipaddress


class BaseMapperType(object):
    
    @staticmethod
    def convert(self, column):
        pass

class MapperStr(BaseMapperType):
    
    @staticmethod
    def convert(cell, column):
        max_length = False
        is_null = False
        if 'max_length' in column:
            max_length = column['max_length']
        if 'is_null' in column:
            is_null = column['is_null']
        cell_type = cell.ctype
        cell_value = cell.value
        #cell ctype 0 empty str 1 unicode str 2 number 3 date 4 boolean 5 error 6 blank
        if cell_type == 0:
            if not is_null:
                return False
            return None
        elif cell_type == 1:
            if max_length and max_length < len(cell_value):
                return False
            return cell_value
        elif cell_type == 2:
            if isinstance(cell_value, float):
                cell_value = int(cell_value)
            if max_length and max_length < len(str(cell_value)):
                return False
            return str(cell_value)
        else:
            return False

class MapperDateTime(BaseMapperType):
    
    @staticmethod
    def convert(cell, column):
        is_null = False
        if 'is_null' in column:
            is_null = column['is_null']
        cell_type = cell.ctype
        cell_value = cell.value
        if cell_type == 0:
            if is_null:
                return False
            return None
        elif cell_type == 1:
            try:
                return datetime.strptime(cell_value, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return False
        elif cell_type == 3:
            return  datetime(*xlrd.xldate_as_tuple(cell_value, 0)) # args 2 is datemode, use 0
        else:
            return False
        
class MapperDate(BaseMapperType):
    
    @staticmethod
    def convert(cell, column):
        is_null = False
        if 'is_null' in column:
            is_null = column['is_null']
        cell_type = cell.ctype
        cell_value = cell.value
        if cell_type == 0:
            if is_null:
                return False
            return None
        elif cell_type == 1:
            try:
                return datetime.strptime(cell_value, '%Y-%m-%d')
            except ValueError:
                return False
        elif cell_type == 3:
            return  datetime(*xlrd.xldate_as_tuple(cell_value, 0)) # args 2 is datemode, use 0
        else:
            return False

class MapperPosiveInt(BaseMapperType):
    
    @staticmethod
    def convert(cell, column):
        is_null = False
        if 'is_null' in column:
            is_null = column['is_null']
        cell_type = cell.ctype
        cell_value = cell.value
        if cell_type == 0:
            if not is_null:
                return False
            return None
        elif cell_type == 1:
            try:
                cell_value = int(cell_value)
                if cell_value < 0:
                    return False
                return cell_value
            except ValueError:
                return False
        elif cell_type == 2:
            if isinstance(cell_value, float):
                cell_type = int(cell_value)
            return cell_value
        pass

class MapperIp(BaseMapperType):
    
    @staticmethod
    def convert(cell, column):
        is_null = False
        if 'is_null' in column:
            is_null = column['is_null']
        cell_type = cell.ctype
        cell_value = cell.value
        if cell_type == 0:
            if not is_null:
                return False
            return None
        elif cell_type == 1:
            try:
                ipaddress.ip_address(cell_value)
                return cell_value
            except ValueError:
                return False
        pass

class BackupCtrlMapper(object):
    model = BackupCtrl
    columns = OrderedDict([
        ('Fschema',{
            'datatype': MapperStr,
            'max_length': 128,
        }),
        ('Ftable_name',{
            'datatype': MapperStr,
            'max_length': 128,
        }),
        ('Ftype',{
            'datatype': MapperStr,
            'max_length': 1,
        }),
        ('Fsplit_field',{
            'datatype': MapperStr,
            'max_length': 1024
        }),
        ('Fbackup_status',{
            'datatype': MapperStr,
            'max_length': 1
        }),
        ('Fdata_begin_date',{
            'datatype': MapperDateTime,
        }),
        ('Fbackup_strategy',{
            'datatype': MapperStr,
            'max_length': 1,
        }),
        ('Fbackup_interval',{
            'datatype': MapperPosiveInt,
        }),
        ('Flast_date',{
            'datatype': MapperDate,
        }),
        ('Fpriority',{
            'datatype': MapperStr,
        }),
        ('Fserver_ip',{
            'datatype': MapperIp,
        }),
        ('Fserver_info',{
            'datatype': MapperStr,
            'max_length': 32,
        }),
        ('Fmodify_time',{
            'datatype': MapperDateTime,
        }),
    ])
    success = True
    msg = 'Done.'
    def __init__(self, xlrow):
        self._Fschema = None
        self._Ftable_name = None
        self._Ftype = None
        self._Fsplit_field = None
        self._Fbackup_status = None
        self._Fdata_begin_date = None
        self._Fbackup_strategy = None
        self._Fbackup_interval = None
        self._Flast_date = None
        self._Fpriority = None
        self._Fserver_ip = None
        self._Fserver_info = None
        self._Fmodify_time = None
        self.__load_xls(xlrow)
    
    def convert2model(self):
        if not self.success:
            return False
        return self.model(
            **{column_key: getattr(self, column_key) for column_key in self.columns}
        )
    
    def __load_xls(self, xlrow):
        for column_key in self.columns:
            column = self.columns[column_key]
            top = xlrow[0]
            xlrow.remove(top)
            convert_data = column['datatype'].convert(top, column)
            if convert_data is False:
                self.success = False
                self.msg += '%s convert failed. \n' % column_key
            key = '_%s' % column_key    #mapper class attribute
            if hasattr(self, key):
                setattr(self, key, convert_data)

    def __repr__(self):
        re_msg = ''
        for column_key in self.columns:
            re_msg += '%s \n' % repr(getattr(self, column_key))
        return re_msg

    @property
    def Fschema(self):
        return self._Fschema
    
    @property
    def Ftable_name(self):
        return self._Ftable_name
    
    @property
    def Ftype(self):
        return self._Ftype
    
    @property
    def Fsplit_field(self):
        return self._Fsplit_field
    
    @property
    def Fbackup_status(self):
        return self._Fbackup_status
    
    @property
    def Fdata_begin_date(self):
        return self._Fdata_begin_date
    
    @property
    def Fbackup_strategy(self):
        return self._Fbackup_strategy
    
    @property
    def Fbackup_interval(self):
        return self._Fbackup_interval
    
    @property
    def Flast_date(self):
        return self._Flast_date
    
    @property
    def Fpriority(self):
        return self._Fpriority
    
    @property
    def Fserver_ip(self):
        return self._Fserver_ip

    @property
    def Fserver_info(self):
        return self._Fserver_info
    
    @property
    def Fmodify_time(self):
        return self._Fmodify_time
    
    pass

class PullBackupCtrlViaXls(object):

    """get backupctrl from xls file strategy class

    __init__(self, content)
        content is str, read from file or sth.
    """

    def __init__(self, content):
        xls = xlrd.open_workbook(file_contents=content)
        backup = xls.sheet_by_index(0)
        self._xls = backup
        pass
    def do(self):
        re_msg = ''
        for i in range(self._xls.nrows):
            bm = BackupCtrlMapper(self._xls.row(i))
            if bm.success:
                re_msg += repr(bm)
                bm.convert2model().save()
            else:
                print(bm) # not pass data from excel
        return re_msg





class Reader(object):

    """reader invoker
    
    usage:
    select strategy, and call execute()
    
    __init__(self, strategy)
        strategy include [PullBackupCtrlViaXls,]
    """

    def __init__(self, strategy):
        self._strategy = strategy
    def execute(self):
        return self._strategy.do()
        

# class ValidationBackupCtrl(object):
#     def __init__(self):
#         pass
#     def do(self):
#         return None

# def convert_model(model):
#         cols = []
#         for field in model._meta.fields:
#             cols.append({
#                 'name': field.name,
#                 'type': field.get_internal_type(),
#                 'isnull': field.null,
#                 'choices': field.choices,
#                 'isprimary': field.primary_key,
#                 'max_length': field.max_length,
#             })
#         return cols


# class PullBackupCtrlViaXls():

#     def __init__(self, content):
#         self.content = content
#         pass

#     def check_cell(self, cell, field, datemode=0):
#         cell_type = cell.ctype
#         cell_value = cell.value
#         field_type = field['type']
#         #cell ctype 0 empty str 1 unicode str 2 number 3 date 4 boolean 5 error 6 blank
#         if cell_type == 0 and not field['isnull']:
#             return 'ERROR'
#         elif field_type in ['DateTimeField', 'DateField']:
#             date = None
#             if cell_type != 3:
#                 try:
#                     date = datetime.strptime(cell_value, '%Y-%m-%d %H:%M:%S')
#                 except ValueError:
#                     return 'ERROR'
#             else:
#                 date = datetime(*xlrd.xldate_as_tuple(cell_value, datemode))
#             return date
#         elif field_type in ['PositiveIntegerField', 'IntegerField']:
#             try:
#                 cell_value = int(cell_value)
#             except:
#                 return 'ERROR'
#             return cell_value
#         elif field_type in ['CharField', 'GenericIPAddressField']:
#             if cell_type == 2:
#                 cell_value = str(int(cell_value))
#             return cell_value
#         return cell_value

#     def do(self):
#         content = self.content
#         msg, success, data = '', False, None
#         xls = xlrd.open_workbook(file_contents=content)
#         backup = xls.sheet_by_index(0)
#         fields = convert_model(BackupCtrl)
#         for field in fields: 
#             if field['type'] in ['BigAutoField'] and field['isprimary']:
#                 fields.remove(field)
#         if len(fields) != backup.ncols:
#             raise Exception('Cols count not equal, please check.')
#         pass_list = []
#         for i in range(backup.nrows):
#             row = backup.row(i)
#             checked_row = map(lambda args: self.check_cell(args[0], args[1], datemode=xls.datemode), 
#                             [(row[j], fields[j]) for j in range(len(row))])
#             if 'ERROR' in checked_row:
#                 continue
#             pass_list.append(checked_row)
#         for p in pass_list:
#             try: 
#                 bk = BackupCtrl(**dict(zip([f['name'] for f in fields], p)))
#                 bk.save()
#             except Exception as e:
#                 pass_list.remove(p)
#                 pass
#         msg, success, data = 'Done.', False, pass_list
#         return {
#             'msg': msg,
#             'success': success,
#             'data': data
#         }