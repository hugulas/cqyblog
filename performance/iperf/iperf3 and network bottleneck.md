

# 怎么判断网络到底是不是瓶颈？如何寻找参照物？



本人写的文章只是个人工作经验的免费分享，不代表本人供职公司的观点，不承担由此带来的任何责任。



上一篇文章中，我提到了可以用nmon看网络是不是瓶颈。[使用nmon analyzer 分析网络性能](../nmon/nmon analyzer network.md)



我们是根据进出网卡的流量和网卡带宽的比较判断出来的。 进出网卡的流量分别是90MB/s和115MB/s，和千兆网卡的最大吞吐量非常接近了。在这里，我使用的参照物是网卡的标称带宽。

但是，不同的使用场景下，带宽的上限是不一样的。比如，很多万兆卡使用MTU 9000比使用MTU 1500，在传输流数据的时候有明显的优势。再比如，同一张网卡流数据传输和小块数据传输的吞吐量上限很大概率是不同的。有些厂商会提供性能白皮书来给客户做参考，比如

[IBM z14 OSA-Express7S 25 GbE Performance Report version 2019-04-19](https://www.ibm.com/support/pages/ibm-z14-osa-express7s-25-gbe-performance-report-version-2019-04-19)

我们可以依赖厂商提供的数据来判断当前网络是否达到了峰值。

但是，真实的环境永远是残酷的。两台机器可能来自不同的厂商，不同的体系架构，使用不同的操作系统；网卡也是不同的厂商，不同的型号，中间还隔着路由器，交换机，防火墙和万水千山。这个时候，就很难依靠静态的参照物了，吞吐量的峰值和理想情况下会差距很大。

这个时候，我们就可以用iperf等工具，自己把参照物测试出来。

iperf2和iperf3都是测试网络性能的工具。具体介绍参见：

https://www.cnblogs.com/xuyaowen/p/iperf-for-network.html

大家可以通过yum或者apt-get安装iperf3。

如果我们要获得当前网络的吞吐量峰值，有两个和应用相关的特征要掌握：

1. 包大小
2. 并发连接数

在上一篇中，通过nmon的NET和NET PACKETS，我们可以知道包大小大概是500字节不到。通过和测试人员交流，我了解到TPS峰值时是128个并发。但是，因为我们的应用还有处理器和io的开销，未必和iperf3 128个连接完全等价， 所以我建议应该要多试几种连接数。

首先，在服务器端，我们启动iperf3的server。

```bash
iperf3 -s -i 1 --logfile iperf-server.txt
```

然后，在客户端，我们启动iperf3的client。

```bash
iperf3 -c 192.168.0.2 -t 60 -P 64 --length 512 --logfile iperfclient.txt
```

包大小我们通过--length参数设置为512。

通过调节-P参数，我们可以尝试16，32，64，128等不同连接数。 

在iperf-server.txt文件结尾，我们可以看到服务器端的吞吐量。SUM那一行显示服务器端的吞吐量是1.12Gbps。

```bash
[127]   0.00-60.02  sec   125 MBytes  17.5 Mbits/sec                  receiver
[129]   0.00-60.02  sec   125 MBytes  17.5 Mbits/sec                  receiver
[131]   0.00-60.02  sec   125 MBytes  17.5 Mbits/sec                  receiver
[133]   0.00-60.02  sec   125 MBytes  17.5 Mbits/sec                  receiver
[SUM]   0.00-60.02  sec  7.82 GBytes  1.12 Gbits/sec                  receiver
```

多试几种不同的连接数，我们就可以得到下面这张表。这张表告诉我们，如果有64个并发连接，这张万兆卡只有1.12Gbps的吞吐量。

| Block size | Parallel Connections- | Throughput Gb/s |
| ---------- | --------------------- | --------------- |
| 512        | 32                    | 1.53            |
| 512        | 64                    | 1.12            |
| 512        | 128                   | 1.45            |

