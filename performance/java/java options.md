# Java和性能相关的选项

```bash
JAVA_OPTS=“-server -Xms4G -Xmx4G -XX:MaxDirectMemorySize=24G”
#with G1 Garbage Collection
#JAVA_OPTS=“-server -Xms16G -Xmx16G -XX:MaxDirectMemorySize=24G”
#JRE7
#JAVA_OPTS=“$JAVA_OPTS -XX:-UseSplitVerifier”
#JRE8
JAVA_OPTS=“$JAVA_OPTS -noverify”
#performance Options
JAVA_OPTS=“$JAVA_OPTS -XX:+PrintFlagsFinal”
JAVA_OPTS=“$JAVA_OPTS -XX:+AggressiveOpts”
#JAVA_OPTS=“$JAVA_OPTS -XX:AutoBoxCacheMax=20000”
JAVA_OPTS=“$JAVA_OPTS -XX:ReservedCodeCacheSize=128M”
JAVA_OPTS=“$JAVA_OPTS -XX:-DontCompileHugeMethods”
JAVA_OPTS=“$JAVA_OPTS -XX:FreqInlineSize=2048"
JAVA_OPTS=“$JAVA_OPTS -XX:InlineSmallCode=2000”
JAVA_OPTS=“$JAVA_OPTS -XX:MaxInlineLevel=64"
JAVA_OPTS=“$JAVA_OPTS -XX:MaxRecursiveInlineLevel=64”
#JAVA_OPTS=“$JAVA_OPTS -XX:-UseBiasedLocking”
#JAVA_OPTS=“$JAVA_OPTS -XX:+AlwaysPreTouch”
#JAVA_OPTS=“$JAVA_OPTS -XX:+PerfDisableSharedMem”
#GC Options
#JAVA_OPTS=“$JAVA_OPTS -XX:ParallelGCThreads=32”
#JAVA_OPTS=“$JAVA_OPTS -XX:+DisableExplicitGC”
#JAVA_OPTS=“$JAVA_OPTS -XX:+ParallelRefProcEnabled”
#CMS Garbage Collection Options
JAVA_OPTS=“$JAVA_OPTS -XX:+UseConcMarkSweepGC”
JAVA_OPTS=“$JAVA_OPTS -XX:+UseParNewGC”
JAVA_OPTS=“$JAVA_OPTS -XX:NewRatio=1"
JAVA_OPTS=“$JAVA_OPTS -XX:SurvivorRatio=2”
JAVA_OPTS=“$JAVA_OPTS -XX:TargetSurvivorRatio=90"
JAVA_OPTS=“$JAVA_OPTS -XX:MaxTenuringThreshold=15”
#JAVA_OPTS=“$JAVA_OPTS -XX:CMSMarkStackSize=2M”
#JAVA_OPTS=“$JAVA_OPTS -XX:CMSMarkStackSizeMax=8M”
#JAVA_OPTS=“$JAVA_OPTS -XX:+CMSClassUnloadingEnabled”
#JAVA_OPTS=“$JAVA_OPTS -XX:+CMSPermGenSweepingEnabled ”
#Garbage First (G1) Garbage Collection Options
#JAVA_OPTS=“$JAVA_OPTS -XX:+UseG1GC”
#JAVA_OPTS=“$JAVA_OPTS -XX:MaxGCPauseMillis=200”
#JAVA_OPTS=“$JAVA_OPTS -XX:InitiatingHeapOccupancyPercent=45"
#JAVA_OPTS=“$JAVA_OPTS -XX:ConcGCThreads=24”
#JAVA_OPTS=“$JAVA_OPTS -XX:G1ReservePercent=10"
#JAVA_OPTS=“$JAVA_OPTS -XX:G1HeapRegionSize=32M”
#GC Log Options
#JAVA_OPTS=“$JAVA_OPTS -Xloggc:/$HOTDB_HOME/logs/gc.log -XX:+PrintGCDetails -XX:+PrintGCDateStamps -XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=10 -XX:GCLogFileSize=100M”
#debug Options
#JAVA_OPTS=“$JAVA_OPTS -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.port=9005 -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false”
#JAVA_OPTS=“$JAVA_OPTS -Xdebug -Xrunjdwp:transport=dt_socket,address=8065,server=y,suspend=n”
#TCP Options
JAVA_OPTS=“$JAVA_OPTS -Djava.net.preferIPv4Stack=true”
```

