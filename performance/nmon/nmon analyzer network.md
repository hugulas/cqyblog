# 使用nmon analyzer 分析网络性能

本人写的文章只是个人工作经验的免费分享，不代表本人供职公司的观点，不承担由此带来的任何责任。

上一篇，我介绍了更好的性能监控工具nmon, 你有去试用吗？

如果是对某个workload采集性能数据，我们一般会把nmon的结果保存成文件。

例子命令：

```
nmon -f -s10 -360
```

+ -f: 使用工作表格式保存输出
+ -s: 采样间隔，-s10表示间隔10秒
+ -x：采样次数 -360表示采样360次，也就是采样一小时

在完成这样的采样后，我们有的时候就需要通过nmon的spreadsheet格式来找出当时workload的性能瓶颈。

然后，你下载nmon analyzer就可以在excel中打开nmon离线的看当时的性能监控数据了。

链接-> http://nmon.sourceforge.net/pmwiki.php?n=Site.Nmon-Analyser

注意：在这个包里还有他的英文使用文档，看了这个文档（NA_UserGuide v66.pdf），你就不用满世界去找每个tab数据的含义了。



## 实战分析网络性能

我这一篇会介绍怎么通过nmon analyzer分析网络的性能数据。

和网络有关工作表主要有如下几个：

- BBBN：网络的名字，速度和MTU大小
- BBBP：emstat和lsattr的结果，你可以看到netstat的信息
- NET：这一页显示了每张网卡的分时数据吞吐量，包括了读，写和总吞吐量（读+写）
- NETPACKET：这一页显示了每张网卡的分时传输的包数量，包括了读，写和总数
- NETSIZE：每张网卡上的包的大小

这里面MTU和网卡的速度我们首先要确定下。

如果你没有在Excel中找到网卡的类型和速度，可以通过以下命令查看。

首先，找到网络接口对应的网卡

```bash
hugulas@hugulas-PC:/sys/devices$ ls -la /sys/class/net
total 0
drwxr-xr-x  2 root root 0 May 15 10:11 .
drwxr-xr-x 53 root root 0 May 15 10:11 ..
lrwxrwxrwx  1 root root 0 May 15 10:11 docker0 -> ../../devices/virtual/net/docker0
lrwxrwxrwx  1 root root 0 May 24 16:02 enp1s0 -> ../../devices/pci0000:00/0000:00:03.1/0000:01:00.0/net/enp1s0
lrwxrwxrwx  1 root root 0 May 24 16:02 lo -> ../../devices/virtual/net/lo
```

然后，我们看看网卡设备的速度：

```bash
hugulas@hugulas-PC:/sys/devices$ cat /sys/class/net/enp1s0/speed
100	
```

我这张网卡是100Mb的

再次，还可以看看网卡的MTU：

```bash
hugulas@hugulas-PC:/sys/devices$ cat /sys/class/net/enp1s0/mtu
1500
```

如果我们想看看网卡是否瓶颈呢，我们可以来看看NET页面先。

从这个页面，我们从按照卡来划分的直方图中来看到流量集中在千兆卡上，读和写的峰值分别是90MB和110MB，这张网卡是张千兆网卡1000Gbps（125MB/s），已经接近它的极限了。

![image-20200524162433102](/Users/cqy/Library/Application Support/typora-user-images/image-20200524162433102.png)

从分时图也可以看到，瓶颈出现时，网络流量达到峰值。

![](/Users/cqy/Library/Application Support/typora-user-images/image-20200524161732846.png)

如果包的大小比较小，那么这张卡的最大吞吐量会更差。（你的包的大小受制于MTU大小，最大不能大于MTU。所以，一般认为MTU=9000的配置，对于高速网卡来说，性能更好）

我们可以看下它的包大小。我没有拿到NETSIZE工作表，但是可以根据NETPACKETS算出包大小，峰值时，读写在210K/s，那么包大小大约在428到523Byte之间。包还是比较小的。

![image-20200524162703826](/Users/cqy/Library/Application Support/typora-user-images/image-20200524162703826.png)





