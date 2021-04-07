

# 使用Linux跟踪点，perf和eBPF追踪数据包的旅程

【原文】https://blog.yadutaf.fr/2017/07/28/tracing-a-packet-journey-using-linux-tracepoints-perf-ebpf/

我一直在寻找一种底层的Linux网络调试工具。（译者：我也在做梦的时候找，网络调优比处理器费劲多了）Linux允许使用虚拟网落接口和[网络名称空间](https://blog.yadutaf.fr/2014/01/19/introduction-to-linux-namespaces-part-5-net/)的组合来构建在主机上直接运行的复杂网络。当出现问题时，故障排除相当繁琐。如果这是第三层的路由问题，`mtr`则很有可能会有所帮助。但是，如果这是一个较低层的问题，我通常最终会手动检查每个接口/网桥/网络名称空间/ iptables，并采集几个tcpdumps以试图了解正在发生的事情。如果您不具备网络设置的先验知识，那可能会感到这种调试就像个迷宫。

我需要的是一个可以告诉我的工具：“嘿，我看过您的数据包：在这个接口上，在这个网络名称空间中，它已经消失了”。

基本上，我需要的是`mtr`的第二层版本。

如果不存在？让我们创建一个！

在本文的结尾，我们将提供一个简单易用的底层数据包跟踪器。

如果您对本地Docker容器执行ping操作，它将显示以下内容：

```
# ping -4 172.17.0.2
[  4026531957]          docker0 request #17146.001 172.17.0.1 -> 172.17.0.2
[  4026531957]      vetha373ab6 request #17146.001 172.17.0.1 -> 172.17.0.2
[  4026532258]             eth0 request #17146.001 172.17.0.1 -> 172.17.0.2
[  4026532258]             eth0   reply #17146.001 172.17.0.2 -> 172.17.0.1
[  4026531957]      vetha373ab6   reply #17146.001 172.17.0.2 -> 172.17.0.1
[  4026531957]          docker0   reply #17146.001 172.17.0.2 -> 172.17.0.1
```

### 通过追踪来走出迷宫

从迷宫中逃脱的一种方法是探索。这是您迷宫游戏的一部分。摆脱迷宫的另一种方法是转移视角，从迷宫上方去看，观察那些知道路径的人所走的路径。

对Linux老鸟来说，这意味着切换到内核的视角，即网络名称空间只是标签，而不是“容器” [1](https://blog.yadutaf.fr/2017/07/28/tracing-a-packet-journey-using-linux-tracepoints-perf-ebpf/#fn:722df47ecbedbece281b05064cb93eb9:containers)。在内核中，数据包，接口等都是普通的可观察对象。

在本文中，我将重点介绍2种追踪工具。`perf`和`eBPF`。

### 介绍`perf`和`eBPF`

`perf`是Linux上的基准工具，可以用于任何与性能相关的分析。它是在与Linux内核相同的源代码树中开发的，并且必须针对被跟踪的内核专门进行编译。它可以跟踪内核以及用户程序。它也可以通过采样或使用跟踪点来工作。我们可以将perf视为`strace`具有低得多性能开销的大规模超集（太拗口了，译者注：perf功能更多，带来的额外性能开销低很多）。在这里，我们仅以非常简单的方式使用它。如果您想了解`perf`的更多信息，强烈建议您[访问Brendan Gregg的博客](http://www.brendangregg.com/perf.html)。

`eBPF`是相对较新的Linux内核附件。顾名思义，这是BPF字节码(“伯克利包过滤器”)的扩展版本，用于…过滤BSD系列上的包。 在Linux上，只要满足某些安全标准，它也可以用于在在线内核中安全地运行平台无关的代码。例如，可以在程序可以运行之前验证内存访问，并且必须有可能证明程序将在有限的时间内结束。如果内核无法证明它，即使它是安全的并且总是终止，它仍将被拒绝。

此类程序可用作QOS的网络分类器，非常低级的联网和筛选（作为eXpress Data Plane（XDP）的一部分），用于跟踪代理和许多其他地方。跟踪探针可以附加到导出了符号的任何函数`/proc/kallsyms`或任何跟踪点。在本文中，我将重点介绍跟踪点上附加的代理。

有关附加到内核功能的跟踪探针的示例，或者作为更[简要的](https://blog.yadutaf.fr/2016/03/30/turn-any-syscall-into-event-introducing-ebpf-kernel-probes/)介绍，我邀请您[阅读我在eBPF上的上一篇文章](https://blog.yadutaf.fr/2016/03/30/turn-any-syscall-into-event-introducing-ebpf-kernel-probes/)。

### 实验室设置

对于这篇文章，我们需要`perf`和一些工具一起使用eBPF。因为我不是手写汇编的忠实拥护者，所以在[`bcc`](https://github.com/iovisor/bcc)这里使用。这是一个功能强大且灵活的工具，可让您将内核探针编写为受限的C，并使用Python在用户环境中对其进行检测。重量级的产品，但完美的发展！

我将在此处复制Ubuntu 17.04（Zesty）的安装说明，这是为笔记本电脑供电的操作系统。关于“性能”的说明在发行版和其他发行版之间的区别不应太大，[`bcc`可以在Github上找到](https://github.com/iovisor/bcc/blob/master/INSTALL.md)特定的[安装说明](https://github.com/iovisor/bcc/blob/master/INSTALL.md)。

> 注意：将eBPF附加到跟踪点至少需要Linux内核> 4.7。

安装`perf`：

```bash
# Grab 'perf'
sudo apt install linux-tools-generic

# Test it
perf
```

如果看到错误消息，则可能表示您的内核最近已更新，但尚未重启。

安装`bcc`：

```bash
# Install dependencies
sudo apt install bison build-essential cmake flex git libedit-dev python zlib1g-dev libelf-dev libllvm4.0 llvm-dev libclang-dev luajit luajit-5.1-dev

# Grab the sources
git clone https://github.com/iovisor/bcc.git

# Build and install
mkdir bcc/build
cd bcc/build
cmake .. -DCMAKE_INSTALL_PREFIX=/usr
make
sudo make install
```

### 找到良好的跟踪点，也就是“使用“手动跟踪数据包的旅程`perf`”

有多种方法可以找到良好的跟踪点。在本文的上一个版本中，我从`veth`驱动程序的代码开始，然后按照从那里开始的路径查找要跟踪的函数。虽然确实可以产生可接受的结果，但我无法捕获所有数据包。实际上，所有数据包所经过的公用路径都是未导出（内联或静态）方法。这也是我意识到Linux具有跟踪点并决定改用跟踪点重写本文和相关代码的时候。这是相当令人沮丧的，但对我来说也更有趣。

关于我自己的话题已经足够，然后重新开始工作。

目标是跟踪数据包采用的路径。根据交叉的接口，交叉的跟踪点可能有所不同（扰流器警报：它们确实如此）。

为了找到合适的跟踪点，我在以下位置使用了ping和2个内部目标和2个外部目标`perf trace`：

1. IP *127.0.0.1的*本地主机
2. IP *172.17.0.2*的无辜Docker容器
3. 我的手机通过IP地址为*192.168.42.129的* USB网络共享
4. 我的手机通过IP *192.168.43.1的* WiFi

`perf trace`是perf的子命令，默认情况下会产生类似于strace的输出（开销要低得多）。我们可以轻松地对其进行调整，以隐藏系统调用本身，而是打印“ net”类别的事件。例如，将ping跟踪到IP为172.17.0.2的Docker容器将如下所示：

```
sudo perf trace --no-syscalls --event 'net:*' ping 172.17.0.2 -c1 > /dev/null
     0.000 net:net_dev_queue:dev=docker0 skbaddr=0xffff96d481988700 len=98)
     0.008 net:net_dev_start_xmit:dev=docker0 queue_mapping=0 skbaddr=0xffff96d481988700 vlan_tagged=0 vlan_proto=0x0000 vlan_tci=0x0000 protocol=0x0800 ip_summed=0 len=98 data_len=0 network_offset=14 transport_offset_valid=1 transport_offset=34 tx_flags=0 gso_size=0 gso_segs=0 gso_type=0)
     0.014 net:net_dev_queue:dev=veth79215ff skbaddr=0xffff96d481988700 len=98)
     0.016 net:net_dev_start_xmit:dev=veth79215ff queue_mapping=0 skbaddr=0xffff96d481988700 vlan_tagged=0 vlan_proto=0x0000 vlan_tci=0x0000 protocol=0x0800 ip_summed=0 len=98 data_len=0 network_offset=14 transport_offset_valid=1 transport_offset=34 tx_flags=0 gso_size=0 gso_segs=0 gso_type=0)
     0.020 net:netif_rx:dev=eth0 skbaddr=0xffff96d481988700 len=84)
     0.022 net:net_dev_xmit:dev=veth79215ff skbaddr=0xffff96d481988700 len=98 rc=0)
     0.024 net:net_dev_xmit:dev=docker0 skbaddr=0xffff96d481988700 len=98 rc=0)
     0.027 net:netif_receive_skb:dev=eth0 skbaddr=0xffff96d481988700 len=84)
     0.044 net:net_dev_queue:dev=eth0 skbaddr=0xffff96d481988b00 len=98)
     0.046 net:net_dev_start_xmit:dev=eth0 queue_mapping=0 skbaddr=0xffff96d481988b00 vlan_tagged=0 vlan_proto=0x0000 vlan_tci=0x0000 protocol=0x0800 ip_summed=0 len=98 data_len=0 network_offset=14 transport_offset_valid=1 transport_offset=34 tx_flags=0 gso_size=0 gso_segs=0 gso_type=0)
     0.048 net:netif_rx:dev=veth79215ff skbaddr=0xffff96d481988b00 len=84)
     0.050 net:net_dev_xmit:dev=eth0 skbaddr=0xffff96d481988b00 len=98 rc=0)
     0.053 net:netif_receive_skb:dev=veth79215ff skbaddr=0xffff96d481988b00 len=84)
     0.060 net:netif_receive_skb_entry:dev=docker0 napi_id=0x3 queue_mapping=0 skbaddr=0xffff96d481988b00 vlan_tagged=0 vlan_proto=0x0000 vlan_tci=0x0000 protocol=0x0800 ip_summed=2 hash=0x00000000 l4_hash=0 len=84 data_len=0 truesize=768 mac_header_valid=1 mac_header=-14 nr_frags=0 gso_size=0 gso_type=0)
     0.061 net:netif_receive_skb:dev=docker0 skbaddr=0xffff96d481988b00 len=84)
```

仅保留事件名称和skbaddr，这看起来更具可读性。

```
net_dev_queue           dev=docker0     skbaddr=0xffff96d481988700
net_dev_start_xmit      dev=docker0     skbaddr=0xffff96d481988700
net_dev_queue           dev=veth79215ff skbaddr=0xffff96d481988700
net_dev_start_xmit      dev=veth79215ff skbaddr=0xffff96d481988700
netif_rx                dev=eth0        skbaddr=0xffff96d481988700
net_dev_xmit            dev=veth79215ff skbaddr=0xffff96d481988700
net_dev_xmit            dev=docker0     skbaddr=0xffff96d481988700
netif_receive_skb       dev=eth0        skbaddr=0xffff96d481988700

net_dev_queue           dev=eth0        skbaddr=0xffff96d481988b00
net_dev_start_xmit      dev=eth0        skbaddr=0xffff96d481988b00
netif_rx                dev=veth79215ff skbaddr=0xffff96d481988b00
net_dev_xmit            dev=eth0        skbaddr=0xffff96d481988b00
netif_receive_skb       dev=veth79215ff skbaddr=0xffff96d481988b00
netif_receive_skb_entry dev=docker0     skbaddr=0xffff96d481988b00
netif_receive_skb       dev=docker0     skbaddr=0xffff96d481988b00
```

这里有很多事情要说。最明显的是`skbaddr`中间的变化，否则保持不变。这是在生成回音回复数据包作为对此回音请求（ping）的回复时。其余时间，相同的网络数据包在接口之间移动，希望没有副本。复制很昂贵…

另一个有趣的一点是，我们清楚地看到数据包通过`docker0`桥，然后是veth的主机端（`veth79215ff`在我的情况下），最后是veth的容器端，装作是`eth0`。我们还没有看到网络名称空间，但是已经提供了很好的概述。

最后，在看到数据包之后，`eth0`我们以相反的顺序命中了跟踪点。这不是响应，而是传输的完成。

通过在4种目标方案上重复类似的过程，我们可以选择最合适的跟踪点来跟踪数据包的行程。我选了其中的4个：

- `net_dev_queue`
- `netif_receive_skb_entry`
- `netif_rx`
- `napi_gro_receive_entry`

采取这四个跟踪点将使我没有任何重复的跟踪事件，从而节省了一些重复数据删除工作。还是不错的。

我们可以很容易地再次检查此选择，例如：

```
sudo perf trace --no-syscalls           \
  --event 'net:net_dev_queue'           \
  --event 'net:netif_receive_skb_entry' \
  --event 'net:netif_rx'                \
  --event 'net:napi_gro_receive_entry'  \
  ping 172.17.0.2 -c1 > /dev/null
     0.000 net:net_dev_queue:dev=docker0 skbaddr=0xffff8e847720a900 len=98)
     0.010 net:net_dev_queue:dev=veth7781d5c skbaddr=0xffff8e847720a900 len=98)
     0.014 net:netif_rx:dev=eth0 skbaddr=0xffff8e847720a900 len=84)
     0.034 net:net_dev_queue:dev=eth0 skbaddr=0xffff8e849cb8cd00 len=98)
     0.036 net:netif_rx:dev=veth7781d5c skbaddr=0xffff8e849cb8cd00 len=84)
     0.045 net:netif_receive_skb_entry:dev=docker0 napi_id=0x1 queue_mapping=0 skbaddr=0xffff8e849cb8cd00 vlan_tagged=0 vlan_proto=0x0000 vlan_tci=0x0000 protocol=0x0800 ip_summed=2 hash=0x00000000 l4_hash=0 len=84 data_len=0 truesize=768 mac_header_valid=1 mac_header=-14 nr_frags=0 gso_size=0 gso_type=0)
```

任务完成！

如果您想进一步研究可用的网络跟踪点列表，可以使用`perf list`：

```bash
sudo perf list 'net:*'
```

这应该返回跟踪点名称列表，例如`net:netif_rx`。冒号（'：'）之前的部分是事件类别（'net'）。后面的部分是事件名称，在此类别中。

### 用`eBPF`/ 编写自定义跟踪器`bcc`

对于大多数情况而言，这绰绰有余。如果您正在阅读这篇文章以了解如何在Linux机器上跟踪数据包的行程，那么您已经拥有了所需的一切。但是，如果您想更深入地研究，运行自定义过滤器，跟踪更多数据，例如数据包跨越的网络名称空间或源IP和目标IP，请耐心等待。

从Linux Kernel 4.7开始，可以将eBPF程序附加到内核跟踪点。在此之前，构建此跟踪器的唯一替代方法是将探针附加到导出的内核符号。尽管这可行，但它有两个缺点：

1. 内核内部API不稳定。跟踪点是（尽管数据结构不一定）。
2. 出于性能原因，大多数联网内部功能都是嵌入式的或静态的。两者都无法探测。
3. 找到用于此功能的所有潜在呼叫站点非常繁琐，并且有时在此阶段并非所有必需的数据都可用。

这篇文章的早期版本尝试使用kprobes，它比较容易使用，但结果充其量是不完整的。

现在，说实话，通过跟踪点访问数据比使用kprobe对应程序要乏味得多。尽管我尝试使本文尽可能地温和，但您可能[要从](https://blog.yadutaf.fr/2016/03/30/turn-any-syscall-into-event-introducing-ebpf-kernel-probes/)（稍旧）的文章[“如何将任何系统调用转换为事件：eBPF内核探针介绍”开始](https://blog.yadutaf.fr/2016/03/30/turn-any-syscall-into-event-introducing-ebpf-kernel-probes/)。

除了这个免责声明，让我们从一个简单的hello世界开始，并深入研究低级管道。在这个世界你好，我们将在4个跟踪点，每次1建立一个情况下，我们选择了较早的（`net_dev_queue`，`netif_receive_skb_entry`，`netif_rx`和`napi_gro_receive_entry`）被触发。为了使这一步更简单，我们将发送程序的`comm`，即16个字符的字符串，它基本上是程序名称。

```c
#include <bcc/proto.h>
#include <linux/sched.h>

// Event structure
struct route_evt_t {
        char comm[TASK_COMM_LEN];
};
BPF_PERF_OUTPUT(route_evt);

static inline int do_trace(void* ctx, struct sk_buff* skb)
{
    // Built event for userland
    struct route_evt_t evt = {};
    bpf_get_current_comm(evt.comm, TASK_COMM_LEN);

    // Send event to userland
    route_evt.perf_submit(ctx, &evt, sizeof(evt));

    return 0;
}

/**
  * Attach to Kernel Tracepoints
  */

TRACEPOINT_PROBE(net, netif_rx) {
    return do_trace(args, (struct sk_buff*)args->skbaddr);
}

TRACEPOINT_PROBE(net, net_dev_queue) {
    return do_trace(args, (struct sk_buff*)args->skbaddr);
}

TRACEPOINT_PROBE(net, napi_gro_receive_entry) {
    return do_trace(args, (struct sk_buff*)args->skbaddr);
}

TRACEPOINT_PROBE(net, netif_receive_skb_entry) {
    return do_trace(args, (struct sk_buff*)args->skbaddr);
}
```

该代码段附加到“ net”类别的4个跟踪点上，加载该`skbaddr`字段并将其传递到公共部分，该部分目前仅加载程序名称。如果您想知道它的`args->skbaddr`来源（我很高兴您这样做），则`args`每当您使用定义跟踪点时，密件抄送都会为您生成该结构`TRACEPOINT_PROBE`。由于它是动态生成的，因此没有简单的方法可以查看其定义，但是有更好的方法。我们可以直接从内核查看数据源。幸运的是`/sys/kernel/debug/tracing/events`，每个跟踪点都有一个条目。例如，对于`net:netif_rx`，可以只是“ cat” `/sys/kernel/debug/tracing/events/net/netif_rx/format`，它应该输出如下内容：

```
name: netif_rx
ID: 1183
format:
	field:unsigned short common_type;         offset:0; size:2; signed:0;
	field:unsigned char common_flags;         offset:2; size:1; signed:0;
	field:unsigned char common_preempt_count; offset:3; size:1; signed:0;
	field:int common_pid;                     offset:4; size:4; signed:1;

	field:void * skbaddr;         offset:8;  size:8; signed:0;
	field:unsigned int len;       offset:16; size:4; signed:0;
	field:__data_loc char[] name; offset:20; size:4; signed:1;

print fmt: "dev=%s skbaddr=%p len=%u", __get_str(name), REC->skbaddr, REC->len
```

您可能会注意到`print fmt`记录末尾的那一行。这正是`perf trace`生成其输出所使用的。

有了低级管道并很好理解之后，我们可以将其包装在Python脚本中，以显示探针eBPF端发送的每个事件的一行：

```python
#!/usr/bin/env python
# coding: utf-8

from socket import inet_ntop
from bcc import BPF
import ctypes as ct

bpf_text = '''<SEE CODE SNIPPET ABOVE>'''

TASK_COMM_LEN = 16 # linux/sched.h

class RouteEvt(ct.Structure):
    _fields_ = [
        ("comm",    ct.c_char * TASK_COMM_LEN),
    ]

def event_printer(cpu, data, size):
    # Decode event
    event = ct.cast(data, ct.POINTER(RouteEvt)).contents

    # Print event
    print "Just got a packet from %s" % (event.comm)

if __name__ == "__main__":
    b = BPF(text=bpf_text)
    b["route_evt"].open_perf_buffer(event_printer)

    while True:
        b.kprobe_poll()
```

您现在可以进行测试。您将需要成为root。

> 注意：此阶段没有过滤。即使后台网络使用率较低，也可能会淹没您的终端！

```
$> sudo python ./tracepkt.py
...
Just got a packet from ping6
Just got a packet from ping6
Just got a packet from ping
Just got a packet from irq/46-iwlwifi
...
```

在这种情况下，您可以看到我正在使用ping和ping6，而WiFi驱动程序刚刚收到了一些数据包。在这种情况下，这就是回声回复。

让我们开始添加一些有用的数据/过滤器。

在这篇文章中，我不会关注性能。这将更好地证明eBPF的强大功能和局限性。为了使其更快，我们可以假设没有奇怪的IP选项时将数据包大小用作启发式方法。按原样使用示例程序会降低网络流量。

> 注意：为了限制这篇文章的长度，我将在这里集中讨论C / eBPF部分。我将在这篇文章的结尾放置一个指向完整源代码的链接。

### 添加网络接口信息

首先，您可以安全地删除“ comm”字段，loading和sched.h标头。抱歉，这里没有实际用途。

然后，您可以包括在内，`net/inet_sock.h`以便我们拥有所有必需的声明并添加`char ifname[IFNAMSIZ];`到事件结构中。

现在，我们将从设备结构中加载设备名称。这很有趣，因为这是一条实际上有用的信息，并且以可管理的规模演示了加载任何数据的技术：

```c
// Get device pointer, we'll need it to get the name and network namespace
struct net_device *dev;
bpf_probe_read(&dev, sizeof(skb->dev), ((char*)skb) + offsetof(typeof(*skb), dev));

// Load interface name
bpf_probe_read(&evt.ifname, IFNAMSIZ, dev->name);
```

您可以对其进行测试，它按原样工作。不过不要忘记在Python端添加相关部分：)

好的，它如何运作？要加载接口名称，我们需要接口设备结构。我将从最后一句话开始，因为这是最容易理解的，而前一个实际上是公正或更棘手的版本。它采用`bpf_probe_read`读取长度的数据`IFNAMSIZ`来自`dev->name`并将其复制到`evt.ifname`。第一线遵循完全相同的逻辑。它将`skb->dev`指针的值加载到中`dev`。不幸的是，如果没有这种不错的offsetof / typeof技巧，我找不到其他加载字段地址的方法。

提醒一下，eBPF的目标是允许对内核进行*安全*脚本编写。这意味着禁止随机存储器访问。所有内存访问都必须经过验证。除非您要访问堆栈中的内存，否则需要使用`bpf_probe_read`读取访问器。这使代码的读取/写入很麻烦，但是也很安全。`bpf_probe_read`在某种程度上类似于的安全版本`memcpy`。它[在内核的bpf_trace.c中](http://elixir.free-electrons.com/linux/v4.10.17/source/kernel/trace/bpf_trace.c#L64)定义。有趣的部分是：

1. 就像memcpy。当心性能副本的成本。
2. 如果发生错误，它将返回一个初始化为0的缓冲区并返回一个错误。它*不会*崩溃或停止程序。

对于本文的其余部分，我将使用以下宏来帮助使内容保持可读性：

```c
#define member_read(destination, source_struct, source_member)                 \
  do{                                                                          \
    bpf_probe_read(                                                            \
      destination,                                                             \
      sizeof(source_struct->source_member),                                    \
      ((char*)source_struct) + offsetof(typeof(*source_struct), source_member) \
    );                                                                         \
  } while(0)
```

这使我们可以编写：

```c
member_read(&dev, skb, dev);
```

那更好！

### 添加网络名称空间ID

那可能是最有价值的信息。就其本身而言，这是所有这些努力的正当理由。不幸的是，这也是最难加载的。

可以从两个位置加载名称空间标识符：

1. 插座“ sk”结构
2. 设备的“开发”结构

我最初使用的是套接字结构，因为这是编写[solisten.py](https://github.com/iovisor/bcc/blob/master/tools/solisten.py)时使用的套接字结构。不幸的是，我不确定为什么，一旦数据包越过名称空间边界，就不再可读该名称空间标识符。该字段全为0，这清楚地指示了无效的内存访问（记住bpf_probe_read在出现错误的情况下是如何工作的）并破坏了整个点。

幸运的是，设备方法可行。可以将其想像为询问数据包位于哪个接口上，并询问该接口所属的名称空间。

```c
struct net* net;

// Get netns id. Equivalent to: evt.netns = dev->nd_net.net->ns.inum
possible_net_t *skc_net = &dev->nd_net;
member_read(&net, skc_net, net);
struct ns_common* ns = member_address(net, ns);
member_read(&evt.netns, ns, inum);
```

它使用以下附加宏来提高可读性：

```c
#define member_address(source_struct, source_member) \
({                                                   \
  void* __ret;                                       \
  __ret = (void*) (((char*)source_struct) + offsetof(typeof(*source_struct), source_member)); \
  __ret;                                             \
})
```

副作用是，它允许简化`member_read`宏。我将其留给读者作为练习。

将其塞在一起，然后……Tadaa！

```
$> sudo python ./tracepkt.py
[  4026531957]          docker0
[  4026531957]      vetha373ab6
[  4026532258]             eth0
[  4026532258]             eth0
[  4026531957]      vetha373ab6
[  4026531957]          docker0
```

如果将ping发送到Docker容器，这应该是您应该看到的。数据包通过本地`docker0`网桥，然后移动到该`veth`对，跨越网络名称空间边界，并且回复遵循确切的反向路径。

那真是令人讨厌！

### 更进一步：仅跟踪请求回复和回显回复数据包

另外，我们还将从数据包中加载IP。无论如何，我们必须读取IP标头。在这里我将坚持使用IPv4，但是相同的逻辑适用于IPv6。

坏消息是，没有什么真的很简单。记住，我们正在网络路径中处理内核。某些数据包尚未打开。这意味着某些标头偏移量仍未初始化。我们必须计算所有这些，从MAC头到IP头，最后到ICMP头。

让我们从加载MAC标头地址并推导IP标头地址开始。我们不会加载MAC标头本身，而是假定它的长度为14个字节。

```
// Compute MAC header address
char* head;
u16 mac_header;

member_read(&head,       skb, head);
member_read(&mac_header, skb, mac_header);

// Compute IP Header address
#define MAC_HEADER_SIZE 14;
char* ip_header_address = head + mac_header + MAC_HEADER_SIZE;
```

这基本上意味着IP标头开始于`skb->head + skb->mac_header + MAC_HEADER_SIZE;`。

现在，我们可以在IP标头的前4位（即第一个字节的前半部分）中解码IP版本，并确保它是IPv4：

```c
// Load IP protocol version
u8 ip_version;
bpf_probe_read(&ip_version, sizeof(u8), ip_header_address);
ip_version = ip_version >> 4 & 0xf;

// Filter IPv4 packets
if (ip_version != 4) {
    return 0;
}
```

现在，我们加载完整的IP标头，获取IP以使Python信息更加有用，确保下一个标头为ICMP并派生ICMP标头偏移量。是的，这一切：

```c
// Load IP Header
struct iphdr iphdr;
bpf_probe_read(&iphdr, sizeof(iphdr), ip_header_address);

// Load protocol and address
u8 icmp_offset_from_ip_header = iphdr.ihl * 4;
evt.saddr[0] = iphdr.saddr;
evt.daddr[0] = iphdr.daddr;

// Filter ICMP packets
if (iphdr.protocol != IPPROTO_ICMP) {
    return 0;
}
```

最后，我们可以加载ICMP标头本身，确保这是Reply的回显请求，并从中加载id和seq：

```c
// Compute ICMP header address and load ICMP header
char* icmp_header_address = ip_header_address + icmp_offset_from_ip_header;
struct icmphdr icmphdr;
bpf_probe_read(&icmphdr, sizeof(icmphdr), icmp_header_address);

// Filter ICMP echo request and echo reply
if (icmphdr.type != ICMP_ECHO && icmphdr.type != ICMP_ECHOREPLY) {
    return 0;
}

// Get ICMP info
evt.icmptype = icmphdr.type;
evt.icmpid   = icmphdr.un.echo.id;
evt.icmpseq  = icmphdr.un.echo.sequence;

// Fix endian
evt.icmpid  = be16_to_cpu(evt.icmpid);
evt.icmpseq = be16_to_cpu(evt.icmpseq);
```

那就是所有人！

如果要从特定的ping实例中过滤ICMP，则可以至少使用Linux的ping 假定`evt.icmpid` [是ping的PID](https://github.com/iputils/iputils/blob/master/ping_common.c)。

### 开演时间！

使用一些简单的Python处理事件，我们可以在几种情况下对其进行测试。以root用户身份启动程序，在另一个终端中启动“ ping”并观察：

```
# ping -4 localhost
[  4026531957]               lo request #20212.001 127.0.0.1 -> 127.0.0.1
[  4026531957]               lo request #20212.001 127.0.0.1 -> 127.0.0.1
[  4026531957]               lo   reply #20212.001 127.0.0.1 -> 127.0.0.1
[  4026531957]               lo   reply #20212.001 127.0.0.1 -> 127.0.0.1
```

进程20212（在Linux的ping上的ICMP ID）在回送接口上发送ICMP回显请求，该ICMP回送请求被传递到生成回显应答并发回的完全相同的回送接口。回送接口既是发送接口，也是接收接口。

那我的WiFi网关呢？

```
# ping -4 192.168.43.1
[  4026531957]           wlp2s0 request #20710.001 192.168.43.191 -> 192.168.43.1
[  4026531957]           wlp2s0   reply #20710.001 192.168.43.1 -> 192.168.43.191
```

在这种情况下，回显请求和回显应答将通过WiFi接口。简单。

稍微无关的一点，还记得我们何时仅打印拥有数据包的进程的“ comm”吗？在这种情况下，回声请求将属于ping进程，而应答将属于WiFi驱动程序，因为就Linux而言，这是生成它的那个。

最后一个，我个人最喜欢的，对Docker容器执行ping操作。由于Docker，这不是我的最爱。这是我的最爱，因为它最能体现eBPF的功能。它允许构建类似“ x射线”的ping工具。

```
# ping -4 172.17.0.2
[  4026531957]          docker0 request #17146.001 172.17.0.1 -> 172.17.0.2
[  4026531957]      vetha373ab6 request #17146.001 172.17.0.1 -> 172.17.0.2
[  4026532258]             eth0 request #17146.001 172.17.0.1 -> 172.17.0.2
[  4026532258]             eth0   reply #17146.001 172.17.0.2 -> 172.17.0.1
[  4026531957]      vetha373ab6   reply #17146.001 172.17.0.2 -> 172.17.0.1
[  4026531957]          docker0   reply #17146.001 172.17.0.2 -> 172.17.0.1
```

对于某些艺术品，现在看起来像：

```
       Host netns           | Container netns
+---------------------------+-----------------+
| docker0 ---> veth0e65931 ---> eth0          |
+---------------------------+-----------------+
```

### 最后的话

eBPF / bcc使我们能够编写一系列新工具来对以前无法访问的位置进行深入的故障排除，跟踪和跟踪，而无需修补内核。跟踪点也很方便，因为它们在有趣的地方提供了很好的提示，从而消除了繁琐地读取内核代码的需要，并且可以放置在代码的某些部分中，这些部分否则将无法通过kprobes进行访问，例如内联或静态函数。

更进一步，我们可以添加IPv6支持。这很容易做到，我将其留给读者练习。理想情况下，我还要衡量对性能的影响。但是这篇文章已经非常非常长了。通过跟踪路由和iptables决策以及跟踪ARP数据包来改进此工具可能会很有趣。所有这些将使该工具成为像我这样的人的完美“ X射线”数据包跟踪器，有时会遇到一些困难的Linux网络设置。

如所承诺的，您可以在Github上查看完整的代码（支持IPv6）：[https](https://github.com/yadutaf/tracepkt) : [//github.com/yadutaf/tracepkt](https://github.com/yadutaf/tracepkt)

最后，我还要感谢的帮助[@fcabestre](https://twitter.com/fcabestre)谁帮我救从错误的硬盘，这个职位的工作草案[@bluxte](https://twitter.com/bluxte)他耐心校对和人民[BCC](https://github.com/iovisor/bcc)谁发的这个帖子技术上是可行的。

### 笔记）

------

1. 我将“容器”用引号引起来，因为从技术上讲，网络名称空间是Linux容器的众多构建块之一。 [[返回\]](https://blog.yadutaf.fr/2017/07/28/tracing-a-packet-journey-using-linux-tracepoints-perf-ebpf/#fnref:722df47ecbedbece281b05064cb93eb9:containers)

← [为您的用户提供Docker-用户命名空间](http://blog.yadutaf.fr/2016/04/14/docker-for-your-users-introducing-user-namespace/) [简介关于我](http://blog.yadutaf.fr/about/) →

