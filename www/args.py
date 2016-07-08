'''
可变参数，给定一组数据a,b,c----a2+b2+c2+...
作用:允许你传入0个或多个参数,这些参数调用时自动组装为一个tuple。
'''
#第一种将a,b，c作为list或tuple传进来
def calc(numbers):
    sum = 0
    for n in numbers:
        sum = sum + n*n
    return sum

print(calc([1,2,3]))
#第二种是可变参数带有符号*
def calc(*numbers):
    sum = 0;
    for n in numbers:
        sum = sum + n*n
    return sum
print(calc(1,2,3))
'''
定义可变参数和定义一个list或tuple参数相比,仅仅在参数前加了一个*号,在函数numbers接收到的是一个tuple,
因此函数代码完全不变,调用可以传入任意个参数包括0个参数
如果已经有一个list,调用可变参数
'''
nums = [1,2,3]
print(calc(nums[0],nums[1],nums[2]))
#这样写法当然可行,问题是太繁琐,所以允许在list或tuple前加一个*号,把list的元素变成可变参数穿进去
print(calc(*nums))
'''
关键字参数
允许你传入0个多个含参数名的参数，这些关键字参数在函数内部组成一个dict
作用:扩展函数的功能
'''
def person(name,age,**kw):
    print('name:',name,'age:',age,'other:',kw)
#第一种
person('m',30,gender='md',job='engineer')
#第二种
extra={'city':'beijing','job':'E'}
#**标示将dict的所有key-value作为关键字参数传入到函数的**kw参数，kw将获得一个dict,注意：
#kw获得的dict是extra的一份拷贝
person('c',24,**extra)

'''
如果要限制关键字参数的名字,就可以用命名关键字参数,
和关键字参数**kw不同,命名关键字参数需要一个特殊分隔符*,
*后面的参数被视为命名关键字参数
'''
def person(name,age,*,city,job):
    print(name,age,city,job)
#调用方法
person('dd',24,city='bd',job='dc')

'''
小结

Python的函数具有非常灵活的参数形态，既可以实现简单的调用，又可以传入非常复杂的参数。

默认参数一定要用不可变对象，如果是可变对象，程序运行时会有逻辑错误！

要注意定义可变参数和关键字参数的语法：

*args是可变参数，args接收的是一个tuple；

**kw是关键字参数，kw接收的是一个dict。

以及调用函数时如何传入可变参数和关键字参数的语法：

可变参数既可以直接传入：func(1, 2, 3)，又可以先组装list或tuple，再通过*args传入：func(*(1, 2, 3))；

关键字参数既可以直接传入：func(a=1, b=2)，又可以先组装dict，再通过**kw传入：func(**{'a': 1, 'b': 2})。

使用*args和**kw是Python的习惯写法，当然也可以用其他参数名，但最好使用习惯用法。

命名的关键字参数是为了限制调用者可以传入的参数名，同时可以提供默认值。

定义命名的关键字参数在没有可变参数的情况下不要忘了写分隔符*，否则定义的将是位置参数。
'''