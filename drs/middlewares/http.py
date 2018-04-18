#-*- coding:-utf-8

__author__ = 'wx'

from drs.utils.logger import Logger
from django.http import HttpResponseForbidden
from django.http import HttpResponseNotAllowed
from django.template import loader
from django.template import RequestContext 

logger = Logger()

class Http403(Exception):
    pass

class Http404(Exception):
    pass

class Http500(Exception):
    pass

class Http405(Exception):
    pass

class Http403Middleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        
        """ 处理403异常
        """
        
        if isinstance(exception, Http403):
            t = loader.get_template('errorhandlers/403.htm')
            return HttpResponseForbidden(t.render({
                                                'message': 403,
                                                })) 
        return None

class Http405Middleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        
        """ 处理405异常
        """
        
        if isinstance(exception, Http405):
            t = loader.get_template('errorhandlers/405.htm')
            return HttpResponseNotAllowed(t.render({
                                                'message': 405,
                                                })) 
        return None
        


