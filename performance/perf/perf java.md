# perf java 分析实战

![image-20200525203250713](/Users/cqy/Box Sync/cqyblog/performance/perf/image-20200525203250713.png)

![image-20200525211306847](/Users/cqy/Box Sync/cqyblog/performance/perf/image-20200525211306847.png)

![image-20200525211453992](/Users/cqy/Box Sync/cqyblog/performance/perf/image-20200525211453992.png)

![image-20200525230227951](/Users/cqy/Box Sync/cqyblog/performance/perf/image-20200525230227951.png)



iperf x86-z

| Block size | Parallel Connections- | Throughput Gb/s |
| ---------- | --------------------- | --------------- |
| 512        |                       |                 |
| 512        | 32                    | 1.53            |
| 512        | 64                    | 1.12  or 4.59   |
| 512        | 128                   | 1.45            |
|            |                       |                 |
|            |                       |                 |

 iperf z-z

| Block size | Parallel Connections- | Throughput Gb/s |
| ---------- | --------------------- | --------------- |
| 512        | 16                    | 8.17            |
| 512        | 32                    | 7.38            |
| 512        | 64                    | 7.99            |
| 512        | 128                   |                 |
|            |                       |                 |
|            |                       |                 |

 

