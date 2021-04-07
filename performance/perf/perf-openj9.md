# Inspecting OpenJ9 performance with perf on Linux – JIT Compiled Methods

# 在Linux上使用perf检查OpenJ9性能-JIT编译方法

本人写的文章只是个人工作经验的免费分享，不代表本人供职公司的观点，不承担由此带来的任何责任。

上一篇文章中，我们泛泛介绍了[perf遇到java](perf-java.md)

这次，我翻译篇来自OpenJ9的文章。原文：[Inspecting OpenJ9 performance with perf on Linux – JIT Compiled Methods](https://blog.openj9.org/2019/07/18/inspecting-openj9-performance-with-perf-on-linux-jit-compiled-methods/)

本文略微吹了下openj9。我也爱openj9。

In the [first post](http://blog.openj9.org/2018/10/18/inspecting-openj9-performance-with-perf-on-linux/) of this series we learned how to profile modules within the JVM itself using `perf`. This is useful for diagnosing JVM related problems. However in typical applications the user application code (JCL included) will dominate the profile, so it is often desirable to want to profile the user application code as well.

在本系列的[第一篇文章中](http://blog.openj9.org/2018/10/18/inspecting-openj9-performance-with-perf-on-linux/)，我们学习了如何使用`perf`对JVM本身的模块采样。这对于诊断与JVM相关的问题很有用。但是，在典型的应用程序中，用户应用程序代码（包括JCL）才是采样中的性能大头，因此通常也希望对用户应用程序代码进行性能采样。

In a typical workload, past the start-up phase of the JVM, nearly all methods being executed will have been JIT compiled. Unfortunately this poses a problem for `perf` because the program counter (PC) addresses recorded during `perf record` are mapped to symbols in a post-processing step via `perf report` by examining the memory map of every binary loaded into the executable’s memory space during the record step. Because of this post-processing step and the nature of the JIT compiler, `perf` is unable to find the binaries corresponding to JIT method symbols, because these methods were generated just-in-time.

在典型的工作负载中，在JVM的启动阶段之后，几乎所有正在执行的方法都将被JIT编译。不幸的是，这引起了一个`perf`的问题，因为

- 在`perf record`采样过程中采集到了程序计数器（PC）地址映射；
- 然后在后处理步骤中`perf report`通过检查加载到程序内存空间中的每个二进制文件的内存映射
- 将采样关联到符号。

由于后处理步骤以及JIT编译器的性质，`perf`因此无法找到与JIT方法符号相对应的二进制文件，因为这些方法（的机器指令）是实时生成的。

Fortunately OpenJ9 and the `perf` tool itself provide support for both de-mangling of JIT method symbols and assembly level annotations of JIT method bodies. We’ll explore how to collect such diagnostics within this post.

幸运的是，OpenJ9和`perf`工具本身为JIT方法符号的拆解和JIT方法的汇编代码注释提供了支持。我们将在本文中探讨如何收集此类诊断信息。

注：

1. demangling是一个术语，C++和Java等面向对象编程的成员函数，类和对象本身是方法签名的一部分，如果要变成一个二进制码的符号，就需要把这些信息放进来，称为mangle,这样看起来就像一个C函数； 反过来，把符号名变成成员函数的签名，就称为demangle。
2. assembly level annotations：我们采集到二进制可执行代码后，可以反汇编成汇编语言，然后，通过把采样的计数器信息和代码行相关联，就能找到最热的汇编代码。这个关联过程称为annotation。

## A Case Study

## 案例研究

We’ll be basing this case study off of a vanilla Ubuntu 18.04 image. To begin we’ll need a workload to investigate. Microbenchmarking dynamic runtimes is [notoriously difficult](https://www.oracle.com/technetwork/articles/java/architect-benchmarking-2266277.html) to get right. Thankfully OpenJDK has us covered with the [JMH microbenchmark suite](https://openjdk.java.net/projects/code-tools/jmh/). First let’s install `maven`:

我们将基于Ubuntu vanilla 18.04映像进行此案例研究。首先，我们需要一个工作负载用于性能分析。微基准测试动态运行时[很难](https://www.oracle.com/technetwork/articles/java/architect-benchmarking-2266277.html)正确选择和使用。（译者：不知道要表达什么意思，随便吧，不影响情节发展）。值得庆幸的是，OpenJDK为我们提供了了[JMH微基准套件](https://openjdk.java.net/projects/code-tools/jmh/)。

### 生成和编译测试案例

首先让我们安装`maven`

```bash
# Install maven and the default JDK
> apt-get update
> apt-get -y install maven default-jdk
```

Next we’ll use the JMH archetype to create the boilerplate for our benchmark:

#### 代码生成

接下来，我们将使用JMH原型为我们的基准测试创建样板：

```bash
> mvn archetype:generate -DinteractiveMode=false -DarchetypeGroupId=org.openjdk.jmh -DarchetypeArtifactId=jmh-java-benchmark-archetype -DgroupId=org.openj9 -DartifactId=indexof-jmh -Dversion=1.0
```

A Maven project will be created in the `indexof-jmh` directory and will be setup with all the dependencies needed to run JMH. As the name of the project suggests, our case study benchmark will be exercising the `java.lang.String.indexOf` API. Next, let’s open up the generated `indexof-jmh/src/main/java/org/openj9/MyBenchmark.java` benchmark and modify it slightly to make use of the `indexOf` API:

将在`indexof-jmh`目录中创建一个Maven项目，并将配置运行JMH所需的所有依赖项。顾名思义，我们这案例研究的基准测试将使用`java.lang.String.indexOf`API。接下来，让我们打开生成的`indexof-jmh/src/main/java/org/openj9/MyBenchmark.java`基准测试，并对其进行稍加修改以使用`indexOf`API：

```java
// ...

package org.openj9;

import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.infra.Blackhole;

@Fork(value = 1)
@Warmup(iterations = 3)
@Measurement(iterations = 3)
public class MyBenchmark {
    public static String data = "Some long string which we are going to search for the character '#'";

    @Benchmark
    public void testMethod(Blackhole blackhole) {
        int indexOfHash = data.indexOf('#');
        blackhole.consume(indexOfHash);
    }
}
```

We can now build the Maven project and run the JMH benchmark using the default JDK available:

#### 编译并运行

现在，我们可以使用默认JDK构建Maven项目并运行JMH基准测试：

```bash
> cd indexof-jmh
> mvn clean install
> java -version
openjdk version "11.0.3" 2019-04-16
OpenJDK Runtime Environment (build 11.0.3+7-Ubuntu-1ubuntu218.04.1)
OpenJDK 64-Bit Server VM (build 11.0.3+7-Ubuntu-1ubuntu218.04.1, mixed mode, sharing)

> java -jar indexof-jmh/target/benchmarks.jar
...
Benchmark                Mode  Cnt         Score         Error  Units
MyBenchmark.testMethod  thrpt    3  37004629.640 ± 1644503.443  ops/s
```

## Measuring OpenJ9

## 测量OpenJ9

OpenJDK Java 11 with HotSpot achieved a score of 37004629 on our machine. How does OpenJDK Java 11 with OpenJ9 compare? To measure we’ll use the [AdoptOpenJDK API](https://api.adoptopenjdk.net/) to grab the latest nightly OpenJDK Java 11 with OpenJ9:

带有HotSpot的OpenJDK Java 11在我们的计算机上得分为37004629。OpenJDK Java 11与OpenJ9相比如何？为了进行衡量，我们将使用[AdoptOpenJDK API](https://api.adoptopenjdk.net/)来获取最新的夜间OpenJDK Java 11和OpenJ9：

```bash
> curl -L 'https://api.adoptopenjdk.net/v2/binary/nightly/openjdk11?openjdk_impl=openj9&os=linux&arch=x64&release=latest&type=jdk&heap_size=normal' > openj9.tar.gz
> tar xvf openj9.tar.gz
```

And repeat the same measurement:

并重复相同的测量：

```bash
> jdk-11.0.4+10/bin/java -version
openjdk version "11.0.4" 2019-07-16
OpenJDK Runtime Environment AdoptOpenJDK (build 11.0.4+10-201907151830)
Eclipse OpenJ9 VM AdoptOpenJDK (build master-9409a4266, JRE 11 Linux amd64-64-Bit Compressed References 20190715_284 (JIT enabled, AOT enabled)
OpenJ9   - 9409a4266
OMR      - 4beca561
JCL      - 411f32dbbb based on jdk-11.0.4+10)

> jdk-11.0.4+10/bin/java -jar indexof-jmh/target/benchmarks.jar
...
Benchmark                Mode  Cnt         Score          Error  Units
MyBenchmark.testMethod  thrpt    3  90224587.381 ± 41943779.975  ops/s
```

OpenJ9 has achieved a much higher score compared to HotSpot for our microbenchmark. But why?

与我们的微基准测试的HotSpot相比，OpenJ9得分更高。但为什么？

## Investigating with Linux perf

`perf` is not installed on our vanilla image so let’s install it using the package manager:

`perf` 未安装在我们的原始映像上，因此让我们使用软件包管理器进行安装：

```bash
# Install perf
> apt-get update
> apt-get -y install linux-tools-generic linux-tools-`uname -r`
```

We can now use the `perf record` utility to capture a profile of our JMH microbenchmark. Hopefully this will tell us where time is being spent, which may give as a hint as to why OpenJ9 is performing so well. We will collect a profile of the cpu-cycles hardware event as we are interested in the assembly level annotation of the profile:

现在，我们可以使用`perf record`来捕获JMH微基准的剖析采样。希望这可以告诉我们时间花在哪里，这可以让我们知道到底为什么OpenJ9表现出色。我们将收集cpu-cycles硬件事件的濮阳采样，因为我们希望对汇编语句的做性能采样注释：

```bash
> perf record -k 1 -e cycles jdk-11.0.4+10/bin/java -jar indexof-jmh/target/benchmarks.jar
```

`perf record` will have generated a `perf.data` file which is our profile. This is the default input to the `perf report` utility which we will use to view the profile:

`perf record`将生成一个`perf.data`文件，这是我们的剖析采样文件。这是`perf report`实用程序的默认输入，我们将使用它来查看剖析采样：

```bash
> perf report
# Overhead  Command          Shared Object       Symbol
# ........  ...............  ..................  ......................
#
     3.58%  org.openj9.MyBe  [JIT] tid 5465      [.] 0x00007f6ad2a24192
     2.93%  org.openj9.MyBe  [JIT] tid 5465      [.] 0x00007f6ad2a2418a
     2.82%  org.openj9.MyBe  [JIT] tid 5465      [.] 0x00007f6ad2a24199
     1.76%  org.openj9.MyBe  [JIT] tid 5465      [.] 0x00007f6ad2a252cd
     1.65%  org.openj9.MyBe  [JIT] tid 5465      [.] 0x00007f6ad2a2418e
     1.58%  org.openj9.MyBe  [JIT] tid 5465      [.] 0x00007f6ad2a25480
     1.54%  org.openj9.MyBe  [JIT] tid 5465      [.] 0x00007f6ad2a1ce97
     1.54%  org.openj9.MyBe  [JIT] tid 5465      [.] 0x00007f6ad2a25553
...
...
     0.09%  org.openj9.MyBe  perf-10944.map      [.] 0x00007f3bcd81d6cb                                                         
     0.09%  org.openj9.MyBe  perf-10944.map      [.] 0x00007f3bcd81bce1                                                         
     0.09%  Thread-6         libj9vm29.so        [.] VM_BytecodeInterpreter::run                                                
     0.09%  org.openj9.MyBe  perf-10944.map      [.] 0x00007f3bcd81dfd4                                                         
     0.09%  org.openj9.MyBe  perf-10944.map      [.] 0x00007f3bcd81dd21
```

Why are we not seeing valid symbol names? This is expected. As described earlier, `perf` is unable to map the profile ticks to symbols because of the JIT compiler. Note that the distance between the “symbols” in the `perf report` are quite small, sometimes a few bytes apart. This is because `perf report` is not able to group a set of profile ticks to one particular symbol (a method or function) so it can aggregate the ticks in the profile. The “symbols” we are seeing here are actually instruction addresses within the JIT method bodies.

为什么我们看不到有效的符号名称？这是预期的。如前所述，`perf`由于JIT编译器的原因，无法将剖析采样样本映射到符号。请注意，`perf report`中的“符号”之间的距离很小，有时相隔几个字节。这是因为`perf report`无法将一组剖析采样样本归纳到一个特定的符号（一种方法或函数）。我们在这里看到的“符号”实际上是JIT方法中的指令地址。

To fix this `perf` provides built-in support for mapping JIT method symbols to address ranges. It does this by looking for a textual file `/tmp/perf-.map` which it uses to map addresses to symbols. The OpenJ9 JIT compiler has an option `-Xjit:perfTool` which will generate such a file which `perf report` will then use. Let’s try again:

要解决此问题，`perf`提供了将JIT方法符号映射到地址范围的内置支持。它通过查找将地址映射到符号的文本文件`/tmp/perf-.map`来实现此目的。OpenJ9 JIT编译器具有一个选项`-Xjit:perfTool`，该选项将生成`perf report`将要使用的这个临时文件。

让我们再试一次：

```
> perf record -k 1 -e cycles jdk-11.0.4+10/bin/java -Xjit:perfTool -jar indexof-jmh/target/benchmarks.jar
> perf report
# Overhead  Command          Shared Object       Symbol
# ........  ...............  ..................  ......................
#
    31.63%  org.openj9.MyBe  perf-12610.map      [.] org/openj9/generated/MyBenchmark_testMethod_jmhTest.testMethod_thrpt_jmhStub(Lorg/openjdk/jmh/runner/InfraControl;Lorg/openjdk/jmh/results  
    15.75%  org.openj9.MyBe  perf-12610.map      [.] java/io/ObjectOutputStream$HandleTable.lookup(Ljava/lang/Object;)I_warm
    15.60%  org.openj9.MyBe  perf-12610.map      [.] org/openj9/generated/MyBenchmark_testMethod_jmhTest.testMethod_thrpt_jmhStub(Lorg/openjdk/jmh/runner/InfraControl;Lorg/openjdk/jmh/results  
    13.86%  org.openj9.MyBe  perf-12610.map      [.] java/net/PlainSocketImpl.socketClose0(Z)V_cold
     9.92%  org.openj9.MyBe  perf-12610.map      [.] java/lang/String.indexOf(II)I_warm
     3.46%  org.openj9.MyBe  perf-12610.map      [.] org/openj9/generated/MyBenchmark_testMethod_jmhTest.testMethod_thrpt_jmhStub(Lorg/openjdk/jmh/runner/InfraControl;Lorg/openjdk/jmh/results   
     1.26%  org.openj9.MyBe  perf-12610.map      [.] org/openjdk/jmh/infra/Blackhole.consume(I)V_warm
     0.89%  org.openj9.MyBe  perf-12610.map      [.] java/lang/String.indexOf(II)I_cold
     0.39%  main             libj9vm29.so        [.] VM_BytecodeInterpreter::run
```

Much better! Note that the symbols have a suffix “_cold”, “_warm”, etc. These represent the JIT compiler optimization level at which each method was compiled. Further note that the top method symbol in the profile is seen several times. This is because the JIT compiler has recompiled this method several times to improve performance.

好多了！请注意，这些符号具有后缀“ _cold”，“ _ warm”等。它们表示在每种方法被JIT编译器编译时的优化级别。还要注意，剖析文件中顶部的方法符号被多次看到。这是因为JIT编译器已多次重新编译此方法以提高性能。

Selecting the top method in the profile using the keyboard arrow keys and using the `a` hotkey will attempt to display the assembly annotation for the selected symbol. Because of the nature of the JIT `perf` cannot locate the binary which corresponds to the symbol and thus is unable to annotate where the hot spots are within the assembly of the JIT compiled method.

使用键盘箭头键和`a`热键在配置文件中选择顶部方法将尝试显示所选符号的反汇编注释。由于JIT的性质，`perf`无法找到与符号相对应的二进制文件，因此无法注释在JIT编译方法的汇编代码的热点。

## Building the Latest perf From Source

## 从源代码构建最新的`perf`

As of `perf` version 4.0.0-rc6 the folks over at Google have [committed a patch](https://lwn.net/Articles/638566/) to `perf` to provide support for assembly annotated profiling of JITed code with a built-in JVMTI agent for profiling the JVM out-of-the box. Unfortunately many Linux distributions do not ship with the compiled JVMTI agent, so we will have to build `perf` from source:

从`perf`4.0.0-rc6版本开始，Google的人员已经[提交了一个补丁程序](https://lwn.net/Articles/638566/)，`perf`可以使用内置的JVMTI代理为JIT代码的汇编注释分析提供支持，以对现成的JVM进行剖析采样分析。不幸的是，许多Linux发行版都不随`perf`一起提供编译好的JVMTI代理，因此我们将必须从源代码构建`perf`：

```bash
# Install dependencies needed to build perf and the JVMTI agent
> apt-get -y install build-essential make gcc g++ flex bison libelf-dev libdw-dev libslang2-dev libssl-dev libiberty-dev default-jdk

# Clone the latest Linux kernel source (perf is included in the tools directory)
> git clone --depth 1 https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git

# Build perf
> cd linux/tools/perf
> make
```

The build process will have built the `perf` JVMTI agent using the default JVM on the `PATH` which will be located in `linux/tools/perf/libperf-jvmti.so`. This JVMTI agent will query the JVM during the `perf record` step and extract the symbol and binary information of JIT method bodies and store it into the profile. A post-processing step will then transform such data to make the JIT method symbols look like other valid native functions. This enables us to view the annotation of the JIT compiled methods.

构建过程将为`PATH`中指令的默认JVM构建`perf`JVMTI代理，jvmti代理会被放在`linux/tools/perf/libperf-jvmti.so`。该JVMTI代理将在`perf record`步骤时查询JVM，提取JIT方法主体的符号和二进制信息并将其存储到剖析采样文件中。然后，后处理步骤将转换这些数据，以使JIT方法符号看起来像其他有效的本地函数（也就是二进制机器指令函数）。这使我们能够查看JIT编译方法的剖析采样注释。

## Assembly Annotation of JIT Compiled Methods

## JIT编译方法的汇编注释

We can now repeat the `perf record` step using the `perf` we just built and add the JVMTI agent to our `java` command:

现在，我们可以将JVMTI代理添加到我们的`java`命令中，使用刚刚构建的perf`的重复`perf record`采样步骤：

```bash
> ./linux/tools/perf/perf record -k 1 -e cycles jdk-11.0.4+10/bin/java -agentpath:`pwd`/linux/tools/perf/libperf-jvmti.so -jar indexof-jmh/target/benchmarks.jar
```

Note that the `-Xjit:perfTool` option is no longer needed as the symbol mapping is taken care of by the JVMTI agent. We now need to post-process the profile to map the JIT symbols to assembly annotations:

请注意，由于JVMTI代理负责符号映射，因此不再需要`-Xjit:perfTool`选项。现在，我们需要对剖析采样文件进行后处理，以将JIT符号映射到程序集注释：

```bash
> ./linux/tools/perf/perf inject -i perf.data --jit -o perf.data.jitted
```

This creates a new `perf.data.jitted` profile with the injected JIT symbols which we can view using the `perf report -i` tool:

这将使用注入的JIT符号创建一个新的剖析采样文件`perf.data.jitted`，我们可以使用该`perf report -i`工具查看该文件：

```bash
> ./linux/tools/perf/perf report -i perf.data.jitted
```

Again, using the arrow keys select the top method and use the `a` hotkey to annotate the method. The disassembly of the hot spots within the JIT compiled method will be shown. Using the `H` hotkey will navigate us to the hottest instruction within the method which appears to be in a tight loop:

同样，使用箭头键选择顶部方法，然后使用`a`热键注释该方法。将显示JIT编译方法中热点的汇编。使用`H`热键将使我们导航到方法中最热的指令，该指令似乎处于紧密循环中：

```
  7.89 │ 1dc:   vmovdqu   0x8(%rsi,%rbx,2),%xmm0
  8.73 │        vpcmpeqw  %xmm1,%xmm0,%xmm0
 14.00 │        vpmovmskb %xmm0,%edx
 10.53 │        test      %edx,%edx
  0.01 │      ↓ jne       1f5
  7.80 │        add       $0x8,%ebx
  7.60 │        cmp       %eax,%ebx
  0.01 │      ↑ jl        1dc
```

Indeed `vpmovmskb` is an AVX/SSE instruction which the JIT has used to implement the core logic of the `indexOf` operation which explains why OpenJ9 is able to achieve such high throughput performance. Digging deeper into the OpenJ9 repository we can find this acceleration has been implemented on x86 as part of [eclipse/openj9#1681](https://github.com/eclipse/openj9/pull/1681).

实际上`vpmovmskb`是一条AVX / SSE指令，JIT已使用它来实现`indexOf`操作的核心逻辑，这解释了OpenJ9为什么能够实现如此高的吞吐性能。深入研究OpenJ9存储库，我们发现此加速已作为[eclipse / openj9＃1681的](https://github.com/eclipse/openj9/pull/1681)一部分在x86上实现。

The `perf` JVMTI agent is spec. compliant, so the same assembly annotation approach will work on other spec. compliant JVMs such as HotSpot. As regular contributors to the JIT component of the OpenJ9 project we do not to look at the disassembly of JIT methods from other JVMs so as to provoke healthy competition. Therefore I leave it as an exercise to the reader to annotate the HotSpot JVM using the same approach and check whether it makes use of AVX/SSE instructions to accelerate the `indexOf` API.

该`perf`对JVMTI代理规范兼容，因此相同的汇编注释方法将适用于其他规范，比如兼容的JVM，例如HotSpot。作为OpenJ9项目的JIT组件的定期贡献者，我们不希望将JIT方法与其他JVM汇编的比较，引发竞争。因此，我将其作为练习供读者使用，读者可以用相同的方法注释HotSpot JVM，并检查它是否利用AVX / SSE指令来加速`indexOf`API。

## Conclusion

## 结论

In this post we learned some of the caveats of profiling dynamic runtimes, such as the JVM, and how to overcome them using the features provided alongside the Linux `perf` tool. We were successfully able to use assembly annotations to identify the reason for an unexpected performance difference between the HotSpot and OpenJ9 JVMs. The same method described in this post can be used to diagnose any JIT related performance issue.

在本文中，我们了解了对动态运行时进行剖析采样分析的一些注意事项，例如JVM，以及如何使用Linux `perf`工具附带的功能克服它们。我们成功地使用了汇编注释来识别HotSpot和OpenJ9 JVM之间出现意外的性能差异的原因。这篇文章中描述的方法可用于诊断任何与JIT相关的类似性能问题。