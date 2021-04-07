# perf遇到java

本人写的文章只是个人工作经验的免费分享，不代表本人供职公司的观点，不承担由此带来的任何责任。

上一篇文章中，我提到了可以用perf寻找瓶颈。[用Perf寻找程序中的性能热点](perf-hotspot-1.md)

但是如果你遇到了Java怎么办？

## Java采样的问题

使用perf等采样工具进行采样的时候，采样工具会得到每次采样时正在执行的指令的进程号和指令地址。

然后，我们需要按照进程号和指令地址从进程的内存映射中找到相应的模块，函数和代码。我们称这样的映射文件为maps文件，描述了地址段和代码块的关系。

比如Linux就有/proc/$pid/maps文件用于记录这样的映射关系。从下面这行可以看出，PID为77350进程中地址段3ef3e100000-3ef3e115000属于libnio.so。

```bash
#less /proc/73350/maps
address                 perms offset  dev   inode  pathname
3ef3e100000-3ef3e115000 r-xp 00000000 fd:04 594822 ...libnio.so
```

- **address 地址** -这是进程地址空间中区域的开始和结束地址
- **perms 权限** -描述如何访问区域中的页面。有四种不同的权限：读取，写入，执行和共享。如果禁用了读/写/执行，`-`将显示a而不是`r`/ `w`/ `x`。如果区域不*共享的*，它是*进程私有的*，所以`p`会出现，而不是一个`s`。如果该进程尝试以不允许的方式访问内存，则会产生分段错误。可以使用`mprotect`系统调用来更改权限。
- **offset-**如果从文件（使用`mmap`）映射了区域，则这是映射开始的文件中的偏移量。如果内存不是从文件映射的，则永远为0。
- **设备** -如果从文件映射了区域，则这是文件所在的主要和次要设备编号（十六进制）。
- **索引节点** -如果该区域是从文件映射的，则为文件号。
- **pathname-**如果区域是从文件映射的，则这是文件的名称。对于匿名映射区域，此字段为空白。此外还有一些与名特殊地区，如`[heap]`，`[stack]`或`[vdso]`。`[vdso]`代表虚拟动态共享对象。系统调用使用它来切换到内核模式

我们还可以进一步找到指令具体相关的函数。从nm结果可以看到，地址偏移量从e768到e0d8属于JNI函数Java_sun_nio_fs_UnixNativeDispatcher_utimes0。

```
#nm /opt/ibm/java-s390x-80/jre/lib/s390x/libnio.so
...
000000000000ef28 T Java_sun_nio_fs_UnixNativeDispatcher_unlinkat0
000000000000e768 T Java_sun_nio_fs_UnixNativeDispatcher_utimes0
000000000000e0d8 T Java_sun_nio_fs_UnixNativeDispatcher_write
                 U NET_AllocSockaddr@@SUNWprivate_1.1
                 U NET_Bind@@SUNWprivate_1.1
                 U NET_GetPortFromSockaddr@@SUNWprivate_1.1
                 U NET_GetSockOpt@@SUNWprivate_1.1
                 U NET_InetAddressToSockaddr@@SUNWprivate_1.1
                 U NET_SetSockOpt@@SUNWprivate_1.1
                 U NET_SockaddrEqualsInetAddress@@SUNWprivate_1.1
                 U NET_SockaddrToInetAddress@@SUNWprivate_1.1
0000000000000000 A SUNWprivate_1.1
0000000000015d90 a _DYNAMIC
0000000000016000 a _GLOBAL_OFFSET_TABLE_
                 w _ITM_deregisterTMCloneTable
                 w _ITM_registerTMCloneTable
0000000000014050 r __FRAME_END__
0000000000010948 r __GNU_EH_FRAME_HDR
0000000000016448 d __TMC_END__
```

但是，除了少数JNI函数，我们的普通Java代码的地址到代码的映射关系并不能通过这种方式找到。

为什么呢？

Java语言写的代码编译产生的并不是二进制可执行文件，而是一个.class字节码文件。在Java虚拟机执行Java程序时，是一条条解释执行的。但是，Java还有更特殊的行为，即时编译JIT。Java虚拟机很多都带了即时编译器，会在Java运行时把字节码编译成性能更高的二进制机器指令。而且即使编译器会反复优化编译结果，以获得最好的性能。

引用：[深入浅出 JIT 编译器](https://www.ibm.com/developerworks/cn/java/j-lo-just-in-time/index.html)

这带来的问题是：

1. Java的代码和指令的关系，并不能在Java程序启动时确定，没有办法绕过Java虚拟机从操作系统获得。
2. JIT编译的结果，同一份代码会有多个结果。

这样子，我们在perf里就没有办法看到热点在哪个Java函数上。

那怎么办呢？

## Java的热点怎么找

我们需要Java JIT编译器来告诉我们指令和Java函数间的映射关系。

如果是hotspot编译器，github上可以找到perf-map-agent工具

https://github.com/jvm-profiling-tools/perf-map-agent

如果是openj9编译器，就更简单了，直接在执行Java时加上“-Xjit:perfTool"选项就好。

在JVM虚拟机起来后，/tmp目录下会有一个perf-<pid>.map文件描述了Java代码和指令的映射关系。

```bash
#less perf-73350.map
000003EF3FA9A004 180 java/util/zip/ZipFile.getEntryFlag(J)I_cold
000003EF3FA9A204 188 java/util/zip/ZipFile.getEntryTime(J)J_cold
000003EF3FA9A404 188 java/util/zip/ZipFile.getEntryCrc(J)J_cold
```

通过perf script或者perf report，这个时候我们就能看到一堆Java函数了。

```
 $Thread-10 73350/78531  1153.229658: cycles:       3ff9ec9ac00 VM_BytecodeInterpreter::run (/opt/ibm/java-s390x-80/jre/lib/s390x/default/libj9vm29.so)
 $Thread-27 73350/79166  1153.230179: cycles:       3ef40858134 sun/nio/ch/SocketChannelImpl.write(Ljava/nio/ByteBuffer;)I_warm (/tmp/perf-73350.map)
 $Thread-27 73350/79166  1153.230180: cycles:       3ef405daa1a cn/hotpu/hotdb/parser/c/A.a(Ljava/lang/Object;)V_hot (/tmp/perf-73350.map)
 $NIOREACTOR-1-R 73350/73422  1153.230696: cycles:            123660 cpumsf_pmu_enable ([kernel.kallsyms])
 $Thread-22 73350/79128  1153.231006: cycles:       3ef3feb872c sun/nio/cs/UTF_8$Decoder.decode([BII[C)I_warm (/tmp/perf-73350.map)
 $Thread-22 73350/79128  1153.231006: cycles:       3ff9cef7d5e L2L19 (/opt/ibm/java-s390x-80/jre/lib/s390x/default/libj9gc29.so)
```



