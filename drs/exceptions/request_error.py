#!/usr/bin/env python
# encoding: utf-8
# author: bchen
# license: (C) Copyright 2018-2019, Shanghai Stock Exchange.
# file: request_error.py
# time: 2018/1/12 17:17
# desc: 自定义request相关异常

__author__ = 'bchen'

class RequestError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)