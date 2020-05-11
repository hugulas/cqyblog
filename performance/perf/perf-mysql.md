# perf实战mysql

我遇到了一个和 mysql 有关的性能问题，需要看看我做的优化，有没有发挥作用。我第一反应，就是用 perf 采样看看。

但是，动手之前，我们要先想一下，怎么采样。我们先来看看 mysql 有哪些进程和线程。我们 pstree 一下就知道了他们的父子关系。

```bash
linux-abcde:~ # pstree -p|grep mysql
           |-sudo(23409)---mysqld_safe(23412)---mysqld(23553)-+-{mysqld}(23554)
           |                                                  |-{mysqld}(23555)
           |                                                  |-{mysqld}(23556)
           |                                                  |-{mysqld}(23557)
           |                                                  |-{mysqld}(23558)
           |                                                  |-{mysqld}(23559)
           |                                                  |-{mysqld}(23560)
           |                                                  |-{mysqld}(23561)
           |                                                  |-{mysqld}(23562)
           |                                                  |-{mysqld}(23563)
           |                                                  |-{mysqld}(23564)
           |                                                  |-{mysqld}(23565)
           |                                                  |-{mysqld}(23566)
           |                                                  |-{mysqld}(23567)
           |                                                  |-{mysqld}(23568)
           |                                                  |-{mysqld}(23571)
           |                                                  |-{mysqld}(23572)
           |                                                  |-{mysqld}(23573)
           |                                                  |-{mysqld}(23574)
           |                                                  |-{mysqld}(23575)
           |                                                  |-{mysqld}(23576)
           |                                                  |-{mysqld}(23577)
           |                                                  |-{mysqld}(23578)
           |                                                  |-{mysqld}(23579)
           |                                                  |-{mysqld}(23580)
           |                                                  |-{mysqld}(23581)
           |                                                  |-{mysqld}(23582)
           |                                                  |-{mysqld}(23583)
           |                                                  `-{mysqld}(23584)
```

在前面的文章中，我介绍了如何使用 perf record 子命令。我们这次要采好几组perf 数据用于对比，所以我要把 perf.data 写到不同目录以防覆盖。但是我有点不记得怎么去制定输出文件了。我们可以用 `perf help subcommand` 去查看子命令的帮助。

```bash
linux-abcde:~ #perf help record
PERF-RECORD(1)                                         perf Manual                                         PERF-RECORD(1)



NAME
       perf-record - Run a command and record its profile into perf.data

SYNOPSIS
       perf record [-e <EVENT> | --event=EVENT] [-l] [-a] <command>
       perf record [-e <EVENT> | --event=EVENT] [-l] [-a] — <command> [<options>]

DESCRIPTION
       This command runs a command and gathers a performance counter profile from it, into perf.data - without displaying
       anything.

       This file can then be inspected later on, using perf report.

OPTIONS
       <command>...
           Any command you can specify in a shell.

       -e, --event=
           Select the PMU event. Selection can be:
```

通过`/out`就可以找到只要加上`-o outfilename`就好了。(这一段是写给 linux 小白看的，熟悉 linux 的跳过啊)

```
           Collect data without buffering.

       -c, --count=
           Event period to sample.

       -o, --output=
           Output file name.

       -i, --no-inherit
           Child tasks do not inherit counters.

       -F, --freq=
           Profile at this frequency.

       -m, --mmap-pages=
           Number of mmap data pages (must be a power of two) or size specification with appended unit character -
           B/K/M/G. The size is rounded up to have nearest pages power of two value. Also, by adding a comma, the number
           of mmap pages for AUX area tracing can be specified.

       --group
           Put all events in a single event group. This precedes the --event option and remains only for backward
           compatibility. See --event.

       -g
/out
```

我们把负载起来, 看看 perf record能采集到点什么吧。



