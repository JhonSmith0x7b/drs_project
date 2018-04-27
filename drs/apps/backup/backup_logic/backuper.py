#-*- coding:utf-8 -*-

__author__ = 'wx'

from drs.apps.backup.backup_logic.strategy_picker import Picker
from drs.apps.backup.backup_logic.where_gener import Gener
from drs.utils.logger import Logger
from drs.apps.backup.backup_logic import fileinfo_handler as fh
from drs.apps.backup.models import FileInfo

logger = Logger()

def de_responser(func):
    """handle装饰器, 自动调用下一级responser
    """
    def inner(self, *args, **kwargs):
        func(self, *args, **kwargs)
        if self.next is not None:
            self.next.handle()
    return inner

class BaseResponser(object):
    
    """基础责任者, 责任者内包含一个完整的区块功能, 可能存在下一个责任者的引用
    """

    def __init__(self):
        self.next = None
    
    @de_responser
    def handle(self):
        """完整区块功能, 不从外面接受参数, 在内部即可完成全部操作
        """
        logger.debug(f'I am {self.__class__}')
    
    def set_next(self, next):
        self.next = next

class FirstResponser(BaseResponser):

    """第一责任者, 包含功能: 获取备份策略, 筛选备份策略, 生成where语句, 将初始信息
    填入fileinfo表
    """

    def __init__(self):
        self.next = None
        
    @de_responser
    def handle(self):
        picker = Picker()
        data = picker.pick()
        gener = Gener()
        results = []
        for db_key in data:
            for backupctrl in data[db_key]:
                result = gener.gen(backupctrl)
                if result is None:
                    continue
                if isinstance(result, list):
                    for r in result:
                        fh.insert_via_info(db_key, backupctrl, r[0], r[-1])
                else:
                    fh.insert_via_info(db_key, backupctrl, result[0], result[-1])
        print([(f.Fcondition, f.Ffile_name) for f in FileInfo.objects.all()])
        print(len(FileInfo.objects.all()))
    
    def set_next(self, next):
        self.next = next

class SecondResponser(BaseResponser):

    """暂定
    """

    pass











