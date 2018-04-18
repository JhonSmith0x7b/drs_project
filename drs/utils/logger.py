#!/usr/bin/env python
# encoding: utf-8
# author: bchen
# license: (C) Copyright 2018-2019, Shanghai Stock Exchange.
# file: logger.py
# time: 2018/1/12 17:03
# desc: logging 配置
import logging
import os
import time

from drs.settings import log_path, mutex

class Logger:
    def __init__(self, name=None):
        self.log_file_path = log_path + time.strftime('%Y-%m-%d-%h', time.localtime(time.time())) + '.log'
        if not os.path.exists(self.log_file_path):
            if not os.path.exists(log_path):
                 os.system(r'mkdir %s' % log_path)
            os.system(r'touch %s' % self.log_file_path)
        self.file_handler = logging.FileHandler(self.log_file_path)
        self.stream_handler = logging.StreamHandler()
        self.formatter = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s:%(thread)s - %(message)s ')
        self.file_handler.setFormatter(self.formatter)
        self.stream_handler.setFormatter(self.formatter)
        self.logger = logging.getLogger(name)

    def release_handler(self):
        self.logger.removeHandler(self.file_handler)
        self.logger.removeHandler(self.stream_handler)

    def info(self, msg):
        mutex.acquire()
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.stream_handler)
        self.logger.info(msg)
        self.release_handler()
        mutex.release()

    def debug(self, msg):
        mutex.acquire()
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.stream_handler)
        self.logger.debug(msg)
        self.release_handler()
        mutex.release()

    def warning(self, msg):
        mutex.acquire()
        self.logger.setLevel(logging.WARNING)
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.stream_handler)
        self.logger.warning(msg)
        self.release_handler()
        mutex.release()

    def error(self, msg):
        mutex.acquire()
        self.logger.setLevel(logging.ERROR)
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.stream_handler)
        self.logger.error(msg)
        self.release_handler()
        mutex.release()
