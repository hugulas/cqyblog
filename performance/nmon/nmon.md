# 更好用的nmon

本人写的文章只是个人工作经验的免费分享，不代表本人供职公司的观点，不承担由此带来的任何责任。

上一篇，我通过两篇实例介绍了怎么使用top去给性能问题定性。你有没有在听完课程后尝试玩一下这个工具呢？

我们的这门课程是一门实战课程，练习很重要。如果你还没有练习过，我建议你一定要动手做一做。分析性能和写程序一样，动手了才能真的学会。

如果你已经动手练习过，你也许会发现top与Windows任务管理器、Mac活动监视器相比，好像少了点什么？

嗯，是的，top没有IO的性能数据，也没有网络的性能数据。

todo加一个小标题

那么在Linux 上有没有命令行版本的任务管理器呢？有， 我推荐你使用nmon。nmon的作者是IBM的Nigel。到2019年5月，已经有768000个下载了。（要注意的是，nmon是个人作品，和IBM无关，不代表IBM和IBM管理层的观点、立场和战略，也没有提供或隐含任何保证，无法从 IBM 获取相关的帮助。）

对比nmon和Linux上其他主流性能监控工具的界面（比如top和sar），nmon颜值上完胜对手。作为一个工程师、一个码农，你去调性能时，当着测试的面打开nmon，是不是妥妥的黑客范。废话不多说，我们拿nmon来分析一下性能问题，通过实战看看它比top好在哪里？

**nmon的界面：**

![&#x56FE;&#x7247;](/Users/cqy/Box Sync/cqyblog/performance/nmon/mb8SXuKS7Aw2Nn4r.png!thumbnail.png)

从启动界面就可以看到，nmon提供了大量的快捷键。 我们先按下c键，就可以看到**处理器的使用情况了。**

![&#x56FE;&#x7247;](/Users/cqy/Box Sync/cqyblog/performance/nmon/lJ41JGTErO4efrmt.png!thumbnail.png)

我这次实验用的是一台安装了CentOS的物理机器，4核的AMD处理器。在nmon的处理器视图中， 竖线"\|" 把视图分成了两半。左边有5列，分别是CPU，User%，Sys%，Wait%，和Idle。

* CPU列是处理核的序号；
* User%列表示了用户进程消耗的处理器时间比例；
* Sys%表示了系统空间消耗的处理器时间比例；
* Wait%列表示了处理器处于等待状态的处理器时间比例，比如等待磁盘IO；
* Idle列表示了处理器空闲的时间比例。

而右边的界面更有意思，nmon通过颜色和字符组成的柱状图，让我们形象化地了解CPU的使用情况。

![&#x56FE;&#x7247;](/Users/cqy/Box Sync/cqyblog/performance/nmon/gxl5TwzkcEw1JEcs.png!thumbnail.png)

从我贴的图上，你可以看到，每个处理器是一行，绿色底色的字母U表示用户进程消耗的处理器时间，红色底色的字母S表示系统空间消耗的处理器时间。如果绿色字母U越多，说明用户进程消耗的处理器时间越多。

我们从贴图中可以看到在表头下依次有四行，分别显示了四个核的利用率，每行的右侧只有一两个U或者S，可见CPU利用率不高。在四个核的利用率下隔了一行是处理器利用率的平均值。

如果我还想同时看**内存，网络和磁盘的性能信息怎么办**？我也记不住那么多快捷键啊，那就按下h键吧。

nmon相比其他命令行的最大的好处是帮助做得非常友好，所见即所得，你可以一边看帮助，一边尝试不同的选项，立刻看到效果。

比如，我在按下m键（memory），在界面的底部就冒出了一块新的信息“Memory and Swap”。这新冒出来的一块内容就是内存和交换区信息。我们来读一下。

表格第一行开头显示：Page Size:4KB 表示内存是以4KB为单位分块的， 然后有两列：RAM-Memory和SWAP-Space，分别显示了内存和SWAP分区的使用情况。

我的这台Linux有6374.3M内存，还有5531.9M空闲，空闲率是82.1%。SWAP分区是6912M，还有5187M空闲，空闲率75%。

![&#x56FE;&#x7247;](/Users/cqy/Box Sync/cqyblog/performance/nmon/y5UlpPWZ8KYvhSOq.png!thumbnail.png)

我除了想看内存和处理器的性能，还想看**磁盘和网络的\*\***性能**\*\*。**

我按照帮助的提示按下了n和d，打开了网络（network）和磁盘（disk）的信息。然后，我再次按下了h，把帮助（help）给关闭了。

nmon的快捷键几乎都是按照英文单词首字母来的，非常容易记住。按一下首字母快捷键打开响应的窗口，再按一下就关了这个窗口。看下面这张贴图，nmon界面中有处理器信息，有内存信息，有网络性能数据，还有磁盘IO的性能数据。我们已经准备好了，让我们来跑个程序练练手吧。 ![&#x56FE;&#x7247;](/Users/cqy/Box Sync/cqyblog/performance/nmon/1eqbN2jYLMsr4Vc5.png!thumbnail.png)

我们运行例子程序2（[https://github.com/hugulas/perftools-intro/blob/master/linux-perf/sample2/mem.c](https://github.com/hugulas/perftools-intro/blob/master/linux-perf/sample2/mem.c)）， 通过nmon来看看这个程序慢在哪里。

```text
# 编译
gcc mem.c -o mem
# 执行，每次调用间隔100微秒
./mem 100
```

程序运行一小会儿，我们就会发现nmon输出界面中有三处异常。

1. 在处理器区域，处理器Wait%占比特别高，屏幕右侧满满的都是蓝色的W字符。怎么回事？
2. 在磁盘区域，sdc设备Busy 100%，这块磁盘满负载了，屏幕右侧是满满的黄色W字符，有大量的写操作和小部分读操作。
3. 在内存区域，内存还剩1.4%，几乎用完了。交换（Swap）分区空闲空间不断在减少， 从刚开始的75%下降到66.7%，并且每秒都在不断减少。

内存耗尽，是这三个现象的根本原因。内存耗尽，系统不断地使用交换分区，交换分区所在的硬盘sdc3出现了大量的写操作。因为内存用尽，大量的内存操作不得不在磁盘上进行，处理器不得不等待IO结束，所以处理器都处于等待状态。那我们再来继续追踪是哪个程序有问题吧。 ![&#x56FE;&#x7247;](/Users/cqy/Box Sync/cqyblog/performance/nmon/KO4uXg5bHYsQxdQX.png!thumbnail.png)

我通过按下“n”和“d"关掉了磁盘和网络视图，然后按下“t"打开了“Top Processes”进程列表视图，在进程列表中，我们可以看到mem程序，Size KB那一列是7400668，它使用了超过740万KB内存，也就是7.4GB内存，而且从Res Data那一列可以看到，绝大部分内存花在了数据部分。mem程序吃光了，我机器上所有的内存。 ![&#x56FE;&#x7247;](/Users/cqy/Box Sync/cqyblog/performance/nmon/evdpRb0AkxQnZTM8.png!thumbnail.png)

## 总结

通过今天的学习，我们可以发现nmon相比top更容易上手，也更方便定制自己的性能监控界面。更重要的是， nmon不仅可以用于定位处理器和内存的问题，还可以用于定位网络，磁盘等更多方面的性能问题。

这里我也给你提一个问题：“top，nmon用于监控性能时，都会对系统性能有一定的影响，怎么控制它带来的影响呢？

