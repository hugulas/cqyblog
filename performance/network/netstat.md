# 容器中都在用哪些端口

我最近经常需要用容器来做一些快速的实验，github和dockerhub上有大量的Dockerfile和image可以用。

但是，有的容器镜像不止一个端口，在容器启动时，我要决定暴露哪些端口。那么首先我们要知道容器内部有哪些端口？

最常见的办法是用netstat。但是镜像内部默认很可能没有装，你需要安装net-tools.

```bash
#  apt-get install net-tools
```

然后，通过netstat -pa就可以看到哪些进程分别用着哪些端口。-p表示需要进程信息，-a表示显示全部。（如果不加-a的话，那么就不会显示LISTEN状态的信息）

```
root@6e5fec1a4f46:/# netstat -pa
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:61530           0.0.0.0:*               LISTEN      75/java
tcp        0      0 6e5fec1a4f46:61500      0.0.0.0:*               LISTEN      75/java
tcp        0      0 0.0.0.0:2181            0.0.0.0:*               LISTEN      75/java
tcp        0      0 0.0.0.0:61510           0.0.0.0:*               LISTEN      75/java
tcp        0      0 localhost:8838          0.0.0.0:*               LISTEN      200/java
tcp        0      0 0.0.0.0:21000           0.0.0.0:*               LISTEN      928/java
tcp        0      0 0.0.0.0:9838            0.0.0.0:*               LISTEN      200/java
tcp        0      0 6e5fec1a4f46:61520      0.0.0.0:*               LISTEN      75/java
tcp        0      0 localhost:48350         localhost:2181          ESTABLISHED 200/java
tcp        0      0 localhost:2181          localhost:48348         ESTABLISHED 75/java
tcp        0      0 6e5fec1a4f46:54318      6e5fec1a4f46:9838       ESTABLISHED 200/java
tcp        0      0 localhost:48408         localhost:2181          ESTABLISHED 928/java
tcp        0      0 localhost:2181          localhost:48340         ESTABLISHED 75/java
tcp        0      0 localhost:48342         localhost:2181          ESTABLISHED 75/java
tcp        0      0 6e5fec1a4f46:61500      6e5fec1a4f46:56683      ESTABLISHED 75/java
tcp        0      0 localhost:2181          localhost:48408         ESTABLISHED 75/java
tcp        0      0 localhost:48356         localhost:2181          ESTABLISHED 200/java
tcp        0      0 6e5fec1a4f46:56683      6e5fec1a4f46:61500      ESTABLISHED 75/java
tcp        0      0 6e5fec1a4f46:9838       6e5fec1a4f46:54318      ESTABLISHED 200/java
tcp        0      0 6e5fec1a4f46:61520      6e5fec1a4f46:40310      ESTABLISHED 75/java
tcp        0      0 localhost:48340         localhost:2181          ESTABLISHED 75/java
tcp        0      0 6e5fec1a4f46:40310      6e5fec1a4f46:61520      ESTABLISHED 928/java
tcp        0      0 localhost:2181          localhost:48350         ESTABLISHED 75/java
tcp        0      0 localhost:2181          localhost:48356         ESTABLISHED 75/java
tcp        0      0 localhost:48348         localhost:2181          ESTABLISHED 75/java
tcp        0      0 localhost:2181          localhost:48342         ESTABLISHED 75/java
Active UNIX domain sockets (servers and established)
Proto RefCnt Flags       Type       State         I-Node   PID/Program name     Path
unix  2      [ ]         STREAM     CONNECTED     2422540  928/java
unix  2      [ ]         STREAM     CONNECTED     2385097  75/java
unix  2      [ ]         STREAM     CONNECTED     2385093  75/java
unix  2      [ ]         STREAM     CONNECTED     2383959  200/java
unix  2      [ ]         STREAM     CONNECTED     2397878  928/java
unix  2      [ ]         STREAM     CONNECTED     2386270  200/java
```

从上面的例子中LISTEN state的几条记录可以看到，

- Java进程（PID 75）监听了2181，615xx等几个端口（2181在这里是zookeeper的端口）
- Java进程（PID 928）监听了21000端口 （21000端口是Atlas Web UI的端口）
- Java进程（PID 200）监听了8838，9838端口 (9838端口是Solr UI端口,8838是Solr的STOP.PORT）

```
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:61530           0.0.0.0:*               LISTEN      75/java
tcp        0      0 6e5fec1a4f46:61500      0.0.0.0:*               LISTEN      75/java
tcp        0      0 0.0.0.0:2181            0.0.0.0:*               LISTEN      75/java
tcp        0      0 0.0.0.0:61510           0.0.0.0:*               LISTEN      75/java
tcp        0      0 localhost:8838          0.0.0.0:*               LISTEN      200/java
tcp        0      0 0.0.0.0:21000           0.0.0.0:*               LISTEN      928/java
tcp        0      0 0.0.0.0:9838            0.0.0.0:*               LISTEN      200/java
tcp        0      0 6e5fec1a4f46:61520      0.0.0.0:*               LISTEN      75/java

```

ps的结果进一步证明了这个结论。

```bash
root@6e5fec1a4f46:/# ps -ef|grep java
root         1     0  0 02:32 pts/0    00:00:00 bash -c /opt/atlas/bin/atlas_start.py;tail --pid=`pidof -s java` -f /dev/null
root        75    63  2 02:32 pts/0    00:01:35 /opt/java/openjdk/bin/java -Dproc_master -XX:OnOutOfMemoryError=kill -9 %p -XX:+UseConcMarkSweepGC -Dhbase.log.dir=/opt/atlas/hbase/bin/../logs -Dhbase.log.file=hbase--master-6e5fec1a4f46.log -Dhbase.home.dir=/opt/atlas/hbase/bin/.. -Dhbase.id.str= -Dhbase.root.logger=INFO,RFA -Dhbase.security.logger=INFO,RFAS org.apache.hadoop.hbase.master.HMaster start
root       200     1  0 02:32 pts/0    00:00:37 /opt/java/openjdk/bin/java -server -Xms512m -Xmx512m -XX:NewRatio=3 -XX:SurvivorRatio=4 -XX:TargetSurvivorRatio=90 -XX:MaxTenuringThreshold=8 -XX:+UseConcMarkSweepGC -XX:ConcGCThreads=4 -XX:ParallelGCThreads=4 -XX:+CMSScavengeBeforeRemark -XX:PretenureSizeThreshold=64m -XX:+UseCMSInitiatingOccupancyOnly -XX:CMSInitiatingOccupancyFraction=50 -XX:CMSMaxAbortablePrecleanTime=6000 -XX:+CMSParallelRemarkEnabled -XX:+ParallelRefProcEnabled -XX:-OmitStackTraceInFastThrow -verbose:gc -XX:+PrintHeapAtGC -XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:+PrintGCTimeStamps -XX:+PrintTenuringDistribution -XX:+PrintGCApplicationStoppedTime -Xloggc:/opt/atlas/solr/server/logs/solr_gc.log -XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=9 -XX:GCLogFileSize=20M -DzkClientTimeout=15000 -DzkHost=localhost:2181 -Dsolr.log.dir=/opt/atlas/solr/server/logs -Djetty.port=9838 -DSTOP.PORT=8838 -DSTOP.KEY=solrrocks -Duser.timezone=UTC -Djetty.home=/opt/atlas/solr/server -Dsolr.solr.home=/opt/atlas/solr/server/solr -Dsolr.data.home= -Dsolr.install.dir=/opt/atlas/solr -Dsolr.default.confdir=/opt/atlas/solr/server/solr/configsets/_default/conf -Xss256k -Dsolr.jetty.https.port=9838 -Dsolr.log.muteconsole -XX:OnOutOfMemoryError=/opt/atlas/solr/bin/oom_solr.sh 9838 /opt/atlas/solr/server/logs -jar start.jar --module=http
root       928     6  1 02:33 pts/0    00:00:50 /opt/java/openjdk/bin/java -Datlas.log.dir=/opt/atlas/logs -Datlas.log.file=application.log -Datlas.home=/opt/atlas -Datlas.conf=/opt/atlas/conf -Xmx1024m -Dlog4j.configuration=atlas-log4j.xml -Djava.net.preferIPv4Stack=true -server -classpath /opt/atlas/conf:/opt/atlas/server/webapp/atlas/WEB-INF/classes:/opt/atlas/server/webapp/atlas/WEB-INF/lib/*:/opt/atlas/libext/*:/opt/atlas/hbase/conf org.apache.atlas.Atlas -app /opt/atlas/server/webapp/atlas
root      1413  1263  0 03:50 pts/1    00:00:00 grep --color=auto java
```

而ESTABLISHED状态的信息，体现了进程间的交互情况。比如Java进程（PID 200）Solr 和 Java进程（PID 928）Atlas需要访问Java进程（PID 75）HBase的2181端口。