# Python RQ初学者指南

## 让 Python 任务排队执行

### 引言

已经有一些关于 Python RQ 的教程了，比如[简易教程-RQ](https://www.twle.cn/go/rq)，

我写这篇 Python RQ 指南的目的是为了让你通过故事的方式可以一步步走下来基本能用，看完这一篇文章基本搞懂 RQ 的。



我在这篇文章中也会带入我用 Python 处理数据时的一些思考。

### 为什么我的 Python程序需要队列？

我学习使用 Python 已经有一段时间了，主要是用做数据处理，需要把数据从机器上下载下来，经过处理后放到结构化的数据库中。我自己设计的爬虫需要用到这个 Python 程序，它每天定时执行，把需要处理的数据下载产生报表。爬虫要按照顺序执行好几个步骤，比如下载数据，解析数据，存储到数据库，然后产生摘要。我的同事还设计了 web 应用，允许用户手动调用这些步骤。

但是，让人困扰的是如果我们仅仅使用



#### 第一步，你需要有个 redis。

如果你是在Linux 或者 mac 上，这条 docker命令能让你一步拥有redis 环境。

```bash
docker run --name my-redis-container -p 6379:6379 -d redis
```

如果你的环境是LinuxOne/s390x

```bash
docker run --name my-redis-container -p 6379:6379 -d s390x/redis
```



####  第二步 安装 RQ

```bash
pip install rq
```



#### 第三步 建立Redis Queue

默认的 RQ 是连接到 redis://@localhost:6379/0。如果你的配置不是这样，自己去查参数吧。

```python
from redis import Redis
from rq import Queue

q = Queue(connection=Redis())
```



#### 第四步 准备好你的任务

你需要随便写个函数，并把他放在某个独立的 python 文件中。注：RQ不允许使用当前“\_\_main\_\_”所在的文件中的函数。所以，不要偷懒，单独准备个文件吧。'

下面这个例子时官方文档提供的，会点网页的词数。

```python
import requests

def count_words_at_url(url):
    resp = requests.get(url)
    return len(resp.text.split())
```



#### 第五步 把任务加入RQ队列

```python
from my_module import count_words_at_url
result = q.enqueue(
             count_words_at_url, 'http://nvie.com')
```

