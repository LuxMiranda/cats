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

#####################
# === Chapter 1 === #
#####################

# Identify function
def id(f):
    return f

# Function composition operator
def _after(girl,friend):
    return lambda *x : girl(friend(*x))

after = Infix(_after)

#####################
# === Chapter 2 === #
#####################

# Memoize any function f. 
# Requires that f's arguments can be cast into a string. 
def memoize(f):
    cache = {}
    def memoizedF(*x):
        argkey = str(*x)
        if argkey not in cache:
            cache[argkey] = f(*x)
        return cache[argkey]
    return memoizedF
