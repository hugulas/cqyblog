# perf的计数器

perf有一系列的采样计数器，可以用于分析不同的性能问题，但是相关的文档确是很少。我会在后面的实践中边学边分享。

这篇文章会讲一些和 counter有关的基本的东西。

**1. 如何查看你的机器上都有哪些counter事件。**

通过 perf list 可以看到当前系统都支持哪些采样事件。

```bash
# perf list
List of pre-defined events (to be used in -e):

  alignment-faults                                   [Software event]
  bpf-output                                         [Software event]
  context-switches OR cs                             [Software event]
  cpu-clock                                          [Software event]
  cpu-migrations OR migrations                       [Software event]
  dummy                                              [Software event]
  emulation-faults                                   [Software event]
  major-faults                                       [Software event]
  minor-faults                                       [Software event]
  page-faults OR faults                              [Software event]
  task-clock                                         [Software event]

  cpum_cf/AES_BLOCKED_CYCLES,(null)=AES_BLOCKED_CYCLES/ [Kernel PMU event]
  cpum_cf/AES_BLOCKED_FUNCTIONS,(null)=AES_BLOCKED_FUNCTIONS/ [Kernel PMU event]
  cpum_cf/AES_CYCLES,(null)=AES_CYCLES/              [Kernel PMU event]
  cpum_cf/AES_FUNCTIONS,(null)=AES_FUNCTIONS/        [Kernel PMU event]
  cpum_cf/CPU_CYCLES,(null)=CPU_CYCLES/              [Kernel PMU event]
  cpum_cf/DEA_BLOCKED_CYCLES,(null)=DEA_BLOCKED_CYCLES/ [Kernel PMU event]
  cpum_cf/DEA_BLOCKED_FUNCTIONS,(null)=DEA_BLOCKED_FUNCTIONS/ [Kernel PMU event]
  cpum_cf/DEA_CYCLES,(null)=DEA_CYCLES/              [Kernel PMU event]
  cpum_cf/DEA_FUNCTIONS,(null)=DEA_FUNCTIONS/        [Kernel PMU event]
lines 1-24
```

如果按下 `G`, 调到最后一行，你会发现有上千号的计数器。(1279个计数器)。

```bash
  sdt_libpthread:rwlock_destroy                      [SDT event]
  sdt_libpthread:rwlock_unlock                       [SDT event]
  sdt_libpthread:wrlock_acquire_write                [SDT event]
  sdt_libpthread:wrlock_entry                        [SDT event]
  sdt_rtld:init_complete                             [SDT event]
  sdt_rtld:init_start                                [SDT event]
  sdt_rtld:longjmp                                   [SDT event]
  sdt_rtld:longjmp_target                            [SDT event]
  sdt_rtld:map_complete                              [SDT event]
  sdt_rtld:map_failed                                [SDT event]
  sdt_rtld:map_start                                 [SDT event]
  sdt_rtld:reloc_complete                            [SDT event]
  sdt_rtld:reloc_start                               [SDT event]
  sdt_rtld:setjmp                                    [SDT event]
  sdt_rtld:unmap_complete                            [SDT event]
  sdt_rtld:unmap_start                               [SDT event]
lines 1256-1279/1279 (END)
```

我们不可能都学会的，太可怕了。所以，最好的办法是打开 `perf help list`看看都有哪些分类。

```bash
PERF-LIST(1)                                           perf Manual                                           PERF-LIST(1)



NAME
       perf-list - List all symbolic event types

SYNOPSIS
       perf list [--no-desc] [--long-desc] [hw|sw|cache|tracepoint|pmu|sdt|event_glob]
```

perf可以通过hw|sw|cache|tracepoint|pmu|sdt|event_glob等选项过滤事件。下面的输出描述了每个分类的含义。

```
OPTIONS
       Without options all known events will be listed.

       To limit the list use:

        1. hw or hardware to list hardware events such as cache-misses, etc.

        2. sw or software to list software events such as context switches, etc.

        3. cache or hwcache to list hardware cache events such as L1-dcache-loads, etc.

        4. tracepoint to list all tracepoint events, alternatively use subsys_glob:event_glob to filter by tracepoint
           subsystems such as sched, block, etc.

        5. pmu to print the kernel supplied PMU events.

        6. sdt to list all Statically Defined Tracepoint events.

```

比如，我们可以通过 `perf list sw` 看到所有软件事件，这些软件事件大概是最通用的了，哪怕在虚拟机上你都能用上。你可以优先去学习他们。最常用的是 cpu-clock, task-clock 等。

```bash
#perf list sw
List of pre-defined events (to be used in -e):

  alignment-faults                                   [Software event]
  bpf-output                                         [Software event]
  context-switches OR cs                             [Software event]
  cpu-clock                                          [Software event]
  cpu-migrations OR migrations                       [Software event]
  dummy                                              [Software event]
  emulation-faults                                   [Software event]
  major-faults                                       [Software event]
  minor-faults                                       [Software event]
  page-faults OR faults                              [Software event]
  task-clock                                         [Software event]
```

我更喜欢PMU事件。参见：http://rts.lab.asu.edu/web_438/project_final/CSE_598_Performance_Monitoring_Unit.pdf

PMU事件的优点：

1. 硬件支持的计数器，
2. 更精确
3. 额外开销更小
4. 功能强大的底层事件

同样是，CPU_CYCLES的计数器，我宁可用 PMU 分类下的，而不是软件的。

缺点：

1. 和硬件平台绑定，比如 ARM，Intel，AMD，IBM s390x, Power 都有自己的 PMU
2. 可能支持没有软件计数器好
3. 需要更多的硬件架构相关的知识

```bash
# perf list pmu
List of pre-defined events (to be used in -e):

  cpum_cf/AES_BLOCKED_CYCLES,(null)=AES_BLOCKED_CYCLES/ [Kernel PMU event]
  cpum_cf/AES_BLOCKED_FUNCTIONS,(null)=AES_BLOCKED_FUNCTIONS/ [Kernel PMU event]
  cpum_cf/AES_CYCLES,(null)=AES_CYCLES/              [Kernel PMU event]
  cpum_cf/AES_FUNCTIONS,(null)=AES_FUNCTIONS/        [Kernel PMU event]
  cpum_cf/CPU_CYCLES,(null)=CPU_CYCLES/              [Kernel PMU event]
  cpum_cf/DEA_BLOCKED_CYCLES,(null)=DEA_BLOCKED_CYCLES/ [Kernel PMU event]
  cpum_cf/DEA_BLOCKED_FUNCTIONS,(null)=DEA_BLOCKED_FUNCTIONS/ [Kernel PMU event]
  cpum_cf/DEA_CYCLES,(null)=DEA_CYCLES/              [Kernel PMU event]
  cpum_cf/DEA_FUNCTIONS,(null)=DEA_FUNCTIONS/        [Kernel PMU event]
  cpum_cf/INSTRUCTIONS,(null)=INSTRUCTIONS/          [Kernel PMU event]
  cpum_cf/L1D_DIR_WRITES,(null)=L1D_DIR_WRITES/      [Kernel PMU event]
  cpum_cf/L1D_PENALTY_CYCLES,(null)=L1D_PENALTY_CYCLES/ [Kernel PMU event]
  cpum_cf/L1I_DIR_WRITES,(null)=L1I_DIR_WRITES/      [Kernel PMU event]
  cpum_cf/L1I_PENALTY_CYCLES,(null)=L1I_PENALTY_CYCLES/ [Kernel PMU event]
  cpum_cf/PRNG_BLOCKED_CYCLES,(null)=PRNG_BLOCKED_CYCLES/ [Kernel PMU event]
  cpum_cf/PRNG_BLOCKED_FUNCTIONS,(null)=PRNG_BLOCKED_FUNCTIONS/ [Kernel PMU event]
  cpum_cf/PRNG_CYCLES,(null)=PRNG_CYCLES/            [Kernel PMU event]
  cpum_cf/PRNG_FUNCTIONS,(null)=PRNG_FUNCTIONS/      [Kernel PMU event]
  cpum_cf/PROBLEM_STATE_CPU_CYCLES,(null)=PROBLEM_STATE_CPU_CYCLES/ [Kernel PMU event]
  cpum_cf/PROBLEM_STATE_INSTRUCTIONS,(null)=PROBLEM_STATE_INSTRUCTIONS/ [Kernel PMU event]
  cpum_cf/SHA_BLOCKED_CYCLES,(null)=SHA_BLOCKED_CYCLES/ [Kernel PMU event]
  cpum_cf/SHA_BLOCKED_FUNCTIONS,(null)=SHA_BLOCKED_FUNCTIONS/ [Kernel PMU event]
  cpum_cf/SHA_CYCLES,(null)=SHA_CYCLES/              [Kernel PMU event]
  cpum_cf/SHA_FUNCTIONS,(null)=SHA_FUNCTIONS/        [Kernel PMU event]
  cpum_sf/SF_CYCLES_BASIC,(null)=SF_CYCLES_BASIC/    [Kernel PMU event]
  cpum_sf/SF_CYCLES_BASIC_DIAG,(null)=SF_CYCLES_BASIC_DIAG/ [Kernel PMU event]

lines 7-30/30 (END)
```

