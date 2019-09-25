# Python如何远程调试

我是陈沁悦。我最近用Python写数据处理程序，有的时候程序卡死在某个地方，光看log也猜不出来到底卡在哪个函数，怎么办？

我以前一直用Java， Ctrl-Break就能打出stack trace。Java的远程调试也非常好用，和Eclipse之类的IDE稍微配置下，就能用。可是python怎么办？

Google了下这个问题？如果不用Pycharm远程调试的话，有几个办法。

Stack Overflow建议使用发信号的办法，操作有些繁琐，自己照着写了debug.py，不是所有的时候都好用，有的时候会遇到python output显示User Defined Signal，然后直接退出。

{% embed url="https://stackoverflow.com/questions/132058/showing-the-stack-trace-from-a-running-python-application" caption="Stack Overflow send user signal" %}

我也试过其他的方案。[https://gist.github.com/reywood/e221c4061bbf2eccea885c9b2e4ef496\#file-how-to-md](https://gist.github.com/reywood/e221c4061bbf2eccea885c9b2e4ef496#file-how-to-md)

{% embed url="https://gist.github.com/reywood/e221c4061bbf2eccea885c9b2e4ef496" caption="来自gist的方法：https://gist.github.com/reywood/e221c4061bbf2eccea885c9b2e4ef496\#file-how-to-md" %}

和下面代码段描述的那样，我首先pip安装了pyrasite, 然后调用pyrasite-shell来调试相应的进程。我把gist中的代码复制黏贴到了python交互窗口中，就打出了每个线程的调用栈。

我感觉还是很费劲啊！

```text
# 找到python进程，如果想用具体参数来过滤，建议用ps -ef
[tester@zThAnalys PerfDataAnalytics]$ ps -e|grep python
 29949 pts/1    00:16:27 python2

# 调试python进程pid 29949
[tester@zThAnalys PerfDataAnalytics]$ pyrasite-shell 29949
Pyrasite Shell 2.0
Connected to 'python2 fix_broken_result.py xxxx'
Python 2.7.5 (default, Feb 20 2018, 09:19:39)
[GCC 4.8.5 20150623 (Red Hat 4.8.5-28)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
(DistantInteractiveConsole)

# 打印每个线程的调用栈
>>> for thread_id, frame in sys._current_frames().items():
...    print 'Stack for thread {}'.format(thread_id)
...    traceback.print_stack(frame)
...    print ''
...
Stack for thread 4396227720960
  File "fix_broken_result.py", line 72, in <module>
    main()
# 调用栈是机密信息，就不打出来了
```



