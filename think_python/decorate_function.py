#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 将装饰器定义成类
Desc : 
"""

import types
from functools import wraps

class Profiled:
    def __init__(self, func):
        print("__init__")
        wraps(func)(self)
        self.ncalls = 0

    def __call__(self, *args, **kwargs):
        print("__call__")
        self.ncalls += 1
        return self.__wrapped__(*args, **kwargs)

    def __get__(self, instance, cls):
        print("__get__")
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)


#情况一
@Profiled
def add(x, y):
    print("add")
    return x + y

result = add(2,3)


class Spam:
    @Profiled
    def bar(self, x):
        print("bar")
        print(self, x)

#情况二
spam = Spam()
spam.bar(3)

#情况三
Spam.bar(3)