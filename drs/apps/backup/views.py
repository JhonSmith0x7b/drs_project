from django.shortcuts import render
from drs.utils.logger import Logger
from drs.exceptions.request_error import RequestError
from drs.middlewares import http
from drs.apps.backup.backup_logic.xls_reader import Reader, PullBackupCtrlViaXls
from django.template import loader
from django.http import HttpResponse

logger = Logger()

def hello(request):
    logger.debug('123000')
    return render(request, 'index.html')

def importpage(request):
    return render(request, 'importpage.html')

def backupctrl_import(request):
    if request.method == 'POST':
        if 'myfile' in request.FILES:
            f = request.FILES['myfile']
            s = PullBackupCtrlViaXls(f.read())
            result = Reader(s).execute()
            return HttpResponse(repr(result))
        else:
            return HttpResponse('no file')
    else:
        raise http.Http405('405')
        pass
    pass