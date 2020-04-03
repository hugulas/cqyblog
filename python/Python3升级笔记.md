# Python3 升级笔记(1)

## 写在开头的话

本人写的文章只是个人工作经验的免费分享，不代表本人供职公司的观点，不承担由此带来的任何责任。

参考文献：

[Python 3.0 有什么新变化](https://docs.python.org/zh-cn/3/whatsnew/3.0.html)

Python2走到了尽头，我后悔没有项目一开始就用 Python3， 偷懒了。

现在只能把代码按照 Python3重构。我把我做的改变分享下，供大家参考。

### 改变 1. print 语句

print语句没了，只有 print 函数了

打标准输出

```python
错误：print "The answer is", 2*2
正确：print("The answer is", 2*2)
```

打标准错误

```python
错误: print >>sys.stderr, "fatal error"
正确: print("fatal error", file=sys.stderr)
```

#### 改变 2. future的 import可以拿走了

我只在处理 unicode 和 print 的时候，Python2代码中用到了他们。

Python3不需要了。下面这句话可以拿走了。

~~from __future__ import print_function~~

#### 改变3. 拿到 encode("utf-8")

Python2为了和 node.js做交互，要把输出写成 utf-8, 所以大量使用了 str.encode("utf-8")，再见了。

#### 改变4：不再判断 StringType 还是 UnicodeType

Python3不再需要判断这个字符串是 String 还是 Unicode了。

~~if isinstance(attr_value, (StringType, UnicodeType)):~~

#### 改变5：Long没有了

Python3没有'**long integer**'了，所以也不在需要判断到底是 long 还是 int, 也不需要long 的类型转换了。

下面这样的语句可以去掉

~~isinstance(attr_value, LongType)~~

#### 改变6：不要再用相对路径引用了

例子参考自：https://stackoverflow.com/questions/16981921/relative-imports-in-python-3

下面是个Python 2能用和 Python 3有时能用的例子

##### 文件结构

```bash
main.py
mypackage/
    __init__.py
    mymodule.py
    myothermodule.py
```

##### mymodule.py

```python
#!/usr/bin/env python3

# Exported function
def as_int(a):
    return int(a)

# Test function for module  
def _test():
    assert as_int('1') == 1

if __name__ == '__main__':
    _test()
```

##### myothermodule.py

```python
#!/usr/bin/env python3

from .mymodule import as_int

# Exported function
def add(a, b):
    return as_int(a) + as_int(b)

# Test function for module  
def _test():
    assert add('1', '1') == 2

if __name__ == '__main__':
    _test()
```

main.py

```python
#!/usr/bin/env python3

from mypackage.myothermodule import add

def main():
    print(add('1', '1'))

if __name__ == '__main__':
    main()
```



如果你在 Python3中运行main.py或者mypackage/mymodule.py，可以通过，但是运行mypackage/myothermodule.py会因为相对引用失败。

最好的办法是使用完整的包名来引用

```python
from mypackage.mymodule import as_int
```

#### 改变7：重新抛出 exception 方式要改变

参考：

https://franklingu.github.io/programming/2016/06/30/properly-reraise-exception-in-python/

##### Python 2

```python
def bar():
    try:
        foo()
    except ZeroDivisionError as e:
        # we wrap it to our self-defined exception
        import sys
        raise MyCustomException, MyCustomException(e), sys.exc_info()[2]
```

##### Python 3

```python
def bar():
    try:
        foo()
    except ZeroDivisionError as e:
        # we wrap it to our self-defined exception
        raise MyCustomException from e
```

#### 改变8：遍历dict不再用 iteritems()而是 items()

```python
错误：for key,value in dict.iteritems()
正确：for key,value in dict.items()
```

