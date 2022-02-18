from __future__ import annotations
from typing import Callable, Generic, TypeVar, Union
from functools import singledispatch

# Class to create infix operators
class Infix:
    def __init__(self, function):
        self.function = function
    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __or__(self, other):
        return self.function(other)
    def __rlshift__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __rshift__(self, other):
        return self.function(other)
    def __call__(self, value1, value2):
        return self.function(value1, value2)

ReturnType = TypeVar("ReturnType")
Function = Callable[..., ReturnType]

# Partial class for implementing partial function application
# From: https://github.com/sagnibak/func_py/blob/master/curry.py
class Partial(Generic[ReturnType]):
    def __init__(
            self, num_args: int, fn: Callable[..., ReturnType], *args, **kwargs
    ) -> None:

        self.num_args = num_args
        self.fn       = fn
        self.args     = args
        self.kwargs   = kwargs

    def __call__(self, *more_args, **more_kwargs) -> Union[Partial[ReturnType], ReturnType]:
        all_args = self.args + more_args 
        all_kwargs = dict(**self.kwargs, **more_kwargs)
        num_args = len(all_args) + len(all_kwargs)
        if num_args >= self.num_args:
            return self.fn(*all_args, **all_kwargs)
        else:
            return Partial(self.num_args, self.fn, *all_args, **all_kwargs)

    def __repr__(self):
        return f"Partial({self.fn}, args={self.args}, kwargs={self.kwargs})"

# Currying!
def curry(num_args: int) -> Callable[[Callable[..., ReturnType]], Partial[ReturnType]]:
    def decorator(fn: Callable[..., ReturnType]):
        return Partial(num_args, fn)
    return decorator

# Identify function
def id(f):
    return f

# Function composition operator
@Infix
def o(girl, friend):
    return lambda *x : girl(friend(*x)) 

# Memoization
# Equivalent to functool's @cache 
def memoize(f):
    cache = {}
    def memoizedF(*x):
        argkey = str(*x)
        if argkey not in cache:
            cache[argkey] = f(*x)
        return cache[argkey]
    return memoizedF


@singledispatch
def mempty(a):
    raise Exception('Not implemented for {}'.format(type(a)))

@singledispatch
def mappend(a, b):
    raise Exception('Not implemented for {}'.format(type(a)))

@mempty.register(str)
def _(a):
    return ''

@mappend.register(str)
def _(a,b):
    return a + b

class Writer:
    def __init__(self, first, second):
        self.first  = first
        self.second = second
    def __str__(self):
        return 'Writer({},{})'.format(self.first,self.second)

@Infix
def w(m1, m2):
    def inner(*x):
        p1 = m1(*x)
        p2 = m2(p1.first)
        return Writer(p2.first, mappend(p1.second,p2.second))
    return inner

def negate(b):
    return Writer(not b, 'Not so! ')

def isEven(n):
    return Writer(n % 2 == 0, 'isEven ')

isOdd = isEven |w| negate

print(isOdd(20))

