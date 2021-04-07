# 容器里IP命令居然也没有

我用的基于ubuntu的容器里居然IP命令都没有

```bash
root@9482621bee0b:/opt/atlas/logs# ip
bash: ip: command not found
```

怎么办？

我先装了net-tools玩玩, 好歹有了ifconfig。

```bash
root@9482621bee0b:/opt/atlas/logs# apt-get install net-tools

root@9482621bee0b:/opt/atlas/logs# ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 172.17.0.5  netmask 255.255.0.0  broadcast 172.17.255.255
        ether 02:42:ac:11:00:05  txqueuelen 0  (Ethernet)
        RX packets 92  bytes 202911 (202.9 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 73  bytes 4959 (4.9 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 48964  bytes 10684224 (10.6 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
```

stackoverflow翻了下，https://stackoverflow.com/questions/51834978/ip-command-is-missing-from-ubuntu-docker-image/51835279

安装iproute2，舒服了。

```bash
apt-get install -y iproute2
```

可以用ip命令了

```bash
root@bd90a5390cf9:/# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
124: eth0@if125: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default
    link/ether 02:42:ac:11:00:05 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 172.17.0.5/16 brd 172.17.255.255 scope global eth0
       valid_lft forever preferred_lft forever
```

马上ping一下host，结果ping也没有，赶紧装一个

```bash
 # apt-get install iputils-ping
```

终于基本上东西齐了。

```bash
root@bd90a5390cf9:/# ping 172.17.0.1
PING 172.17.0.1 (172.17.0.1) 56(84) bytes of data.
64 bytes from 172.17.0.1: icmp_seq=1 ttl=64 time=0.078 ms
64 bytes from 172.17.0.1: icmp_seq=2 ttl=64 time=0.049 ms
64 bytes from 172.17.0.1: icmp_seq=3 ttl=64 time=0.067 ms
```





