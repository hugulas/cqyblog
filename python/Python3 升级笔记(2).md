# Python3 升级笔记(2)

## 写在开头的话

本人写的文章只是个人工作经验的免费分享，不代表本人供职公司的观点，不承担由此带来的任何责任。

参考文献：

[Python 3.0 有什么新变化](https://docs.python.org/zh-cn/3/whatsnew/3.0.html)

Python2走到了尽头，我后悔没有项目一开始就用 Python3， 偷懒了。

现在只能把代码按照 Python3重构。我把我做的改变分享下，供大家参考。

续上一篇 [Python3 升级笔记(1)](Python3升级笔记.md)

#### 改变10：dict.has_key方法没有了

词典没有了 has_key方法, 使用 key in dict 语句代替吧。

```python
错误: dict_example.has_key('type')
正确：'type' in dict_example
```

#### 改变11：一行捕获多个 exception

```python
错误： except (IDontLikeYouException, YouAreBeingMeanException), e:
    		pass
正确： except (IDontLikeYouException, YouAreBeingMeanException) as e:
        pass
```

### 改变12: xrange没有了

其实不是 xrange 没了，而是原来 range  方法（直接得到 list 方法）没了，python2的 xrange 变成了 python3 的range

参考：[Python 3's range is more powerful than Python 2's xrange](https://treyhunner.com/2018/02/python-3-s-range-better-than-python-2-s-xrange/)

```python
错误：for i in xrange(1,100000)
正确：for i in range(1,100000)
```

### 改变13：functools的一些函数没有必要了

我Python2的代码用了functools.reduce来实现和 python3一样的行为。现在升级到 python3，那么直接拿掉这句声明。

~~from functools import reduce~~

参考：https://docs.python.org/2/library/functools.html

#### 改变14：map()和 filter()返回值变成了 iterator 而不是 list

Python2中如果你把 map 和 filter 函数返回值当 list 用，随机访问它，那么你要考虑用 list(map())或者 list(filter())来把返回值变成 list



#### 改变15:获得脚本当前的路径

```python
python 2:os.path.dirname(pathlib.Path(__file__).parent.absolute())
python 3:pathlib.Path(__file__).parent.absolute()
```



