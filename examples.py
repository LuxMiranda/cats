from cats import Writer, rk, curry, o

# Writer monads and Kleisli composition

@Writer('Not so! ')
def negate(b):
    return not b

@Writer('isEven ')
def isEven(n):
    return n % 2 == 0

isOdd = negate |rk| isEven

print(isOdd(4))
# Output: Writer(False, isEven Not so! )

# Currying

@curry(num_args=3)
def addEm(a,b,c):
    return a + b + c

@curry(num_args=3)
def multEm(a,b,c):
    return a*b*c

mult10add9 = addEm(4,5) |o| multEm(1,10)

print(mult10add9(6))
# Output: 69
