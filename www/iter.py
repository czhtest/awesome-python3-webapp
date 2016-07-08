d = {'a':1,'b':2,'c':3}
#迭代出key
for key in d:
    print(key)

#迭代出value
for value in d.values():
    print(value)

#同时迭代
for key,value in d.items():
    print('%s:%s' % (key,value))

#判断一个对象是否可迭代对象通过collections 的iterable类型
from collections import Iterable
print(isinstance('abc',Iterable))
#for循环同时引用了两个变量,很常用
for x,y in [(1,1),(2,4),(3,9)]:
    print(x,y)

#任何可迭代对象都可以作用于for循环，包括我们自定义的数据类型，只要符合迭代条件，就可以使用for循环。

L = list(range(1,11))
print(L)
#（）代表将生成一个generator:
#一边循环一边计算叫生成器
M = (x*x for x in L)

print(isinstance(M,Iterable))
for x in M:
    print(x)

#加判断
N = (x*x for x in L if x%2==0)
for x in N:
    print(x)

#定义generator的另一种方法就是函数定义保含yield关键字,
def fib(max):
    n,a,b = 0,0,1
    while n < max:
        yield b
        a,b = b,a+b
        n = n + 1

    return 'done'
'''
这里，最难理解的就是generator和函数的执行流程不一样。函数是顺序执行，遇到return语句或最后一行一行函数就返回。而变成
generator函数，在每次调用next的时候执行，遇到yield语句就返回。再次执行从上次返回的yield语句出继续执行
'''
def odd():
    print('step 1')
    yield 1
    print('step 2')
    yield 3
    print('step 3')
    yield 5

for x in odd():
    print(x)
#把list、dict、str等Iterable变成Iterator可以使用iter()函数：








