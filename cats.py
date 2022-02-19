from __future__ import annotations
from typing import Generic, TypeVar, Union, Type, Callable
from functools import singledispatch

#def memoize(f):
#    cache = {}
#    def memoizedF(*x):
#        argkey = str(*x)
#        if argkey not in cache:
#            cache[argkey] = f(*x)
#        return cache[argkey]    
#    return memoizedF
#
# Memoize a function that returns a Writer monad
#def memoizeWriter(f):
#    firstCache  = {}
#    second = None
#    def memoizedF(*x):
#        argkey = str(*x)
#        if argkey not in firstCache:
#            writer = f(*x)
#            firstCache[argkey] = writer.first
#            second = writer.second
#        return Writer(firstCache[argkey], second)
#    return memoizedF


ReturnType = TypeVar("ReturnType")
Function = Callable[..., ReturnType]

class WriterMonad:
    def __init__(self, first, second):
        self.first  = first
        self.second = second
    def __str__(self):
        return 'Writer({}, {})'.format(self.first,self.second)

class WriterFunction:
    def __init__(self, function, second):
        self.function = function
        self.second   = second
    def __call__(self, *args):
        result = self.function(*args)
        return WriterMonad(result,self.second)

def Writer(second):
    def decorator(fn: Function):
        return WriterFunction(fn, second)
    return decorator

# Class to create infix operators
class infix:
    def __init__(self, function):
        self.function = function
    def __ror__(self, other):
        return infix(lambda x, self=self, other=other: self.function(other, x))
    def __or__(self, other):
        return self.function(other)
    def __rlshift__(self, other):
        return infix(lambda x, self=self, other=other: self.function(other, x))
    def __rshift__(self, other):
        return self.function(other)
    def __call__(self, value1, value2):
        return self.function(value1, value2)

# Partial class for implementing partial function application
# From: https://github.com/sagnibak/func_py/blob/master/curry.py
class partial(Generic[ReturnType]):
    def __init__(
            self, num_args: int, fn: Callable[..., ReturnType], *args, **kwargs
    ) -> None:

        self.num_args = num_args
        self.fn       = fn
        self.args     = args
        self.kwargs   = kwargs

    def __call__(self, *more_args, **more_kwargs) -> Union[partial[ReturnType], ReturnType]:
        all_args = self.args + more_args 
        all_kwargs = dict(**self.kwargs, **more_kwargs)
        num_args = len(all_args) + len(all_kwargs)
        if num_args >= self.num_args:
            return self.fn(*all_args, **all_kwargs)
        else:
            return partial(self.num_args, self.fn, *all_args, **all_kwargs)

    def __repr__(self):
        return f"partial({self.fn}, args={self.args}, kwargs={self.kwargs})"
  
# Currying!
def curry(num_args: int) -> Callable[[Callable[..., ReturnType]], partial[ReturnType]]:
    def decorator(fn: Callable[..., ReturnType]):
        return partial(num_args, fn)
    return decorator

# Identify function
def id(f):
    return f

# Function composition operator
@infix
def o(girl, friend):
    return lambda *x : girl(friend(*x)) 

@singledispatch
def mempty(a):
    raise Exception('mempty not implemented for {}'.format(type(a)))

@singledispatch
def mappend(a, b):
    raise Exception('mappend not implemented for {}'.format(type(a)))

@mempty.register(str)
def _(a):
    return ''

@mappend.register(str)
def _(a,b):
    return a + b

@infix
def lk(m1, m2):
    def inner(*x):
        p1 = m1(*x)
        p2 = m2(p1.first)
        return WriterMonad(p2.first, mappend(p1.second,p2.second))
    return inner

@infix
def rk(m1, m2):
    return lk(m2,m1)

