# RHEL8上怎么安装并使用CUSTOMKERNEL

本人写的文章只是个人工作经验的免费分享，不代表本人供职公司的观点，不承担由此带来的任何责任。

参考文章：

https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/managing_monitoring_and_updating_the_kernel/managing-kernel-modules_managing-monitoring-and-updating-the-kernel#listing-all-installed-kernels_managing-kernel-modules

有的时候，我会遇到Linux kernel的bug，就需要安装kernel补丁。

kernel开发团队很快提供了补丁。

环境：LinuxOne III s390

操作系统：RHEL 8.1

1. 第一步，我一把装上所有的kernel-*.rpm：（ 出了个错，不去管他）

```bash
[root@lpar36 ~]# rpm -ivh kernel-*
Verifying...                          ################################# [100%]
Preparing...                          ################################# [100%]
Updating / installing...
   1:kernel-core-4.18.0-147.el8.CUSTOM################################# [ 33%]
   2:kernel-modules-4.18.0-147.el8.CUS################################# [ 67%]
   3:kernel-4.18.0-147.el8.CUSTOMKERNE################################# [100%]
dracut-install: ERROR: installing '/etc/dasd.conf'
dracut: FAILED: /usr/lib/dracut/dracut-install -D /var/tmp/dracut.8iX7R6/initramfs -H /etc/dasd.conf
```

2. 第二步，看看gruppy菜单里是不是有这个内核了。

```bash
[root@lpar36 ~]#  grubby --info=ALL
index=0
kernel="/boot/vmlinuz-4.18.0-147.el8.s390x+debug"
args="crashkernel=auto rd.zfcp=0.0.0001,0x5005076802305c49,0x0000000000000000 rd.zfcp=0.0.0002,0x5005076802105c49,0x0000000000000000 rd.zfcp=0.0.0004,0x5005076802305c48,0x0000000000000000 rd.zfcp=0.0.0003,0x5005076802105c48,0x0000000000000000 rd.znet=qeth,0.0.3000,0.0.3001,0.0.3002,layer2=1,portno=0 $tuned_params"
root="UUID=59def7d8-f33f-4aa7-a967-6162cb3efcdf"
initrd="/boot/initramfs-4.18.0-147.el8.s390x+debug.img"
title="Red Hat Enterprise Linux (4.18.0-147.el8.s390x+debug) 8.1 (Ootpa)"
id="7fe4e6a2302e4d9a8c03e3ba4b958c20-4.18.0-147.el8.s390x+debug"
index=1
kernel="/boot/vmlinuz-4.18.0-147.el8.s390x"
args="crashkernel=auto rd.zfcp=0.0.0001,0x5005076802305c49,0x0000000000000000 rd.zfcp=0.0.0002,0x5005076802105c49,0x0000000000000000 rd.zfcp=0.0.0004,0x5005076802305c48,0x0000000000000000 rd.zfcp=0.0.0003,0x5005076802105c48,0x0000000000000000 rd.znet=qeth,0.0.3000,0.0.3001,0.0.3002,layer2=1,portno=0 $tuned_params"
root="UUID=59def7d8-f33f-4aa7-a967-6162cb3efcdf"
initrd="/boot/initramfs-4.18.0-147.el8.s390x.img"
title="Red Hat Enterprise Linux (4.18.0-147.el8.s390x) 8.1 (Ootpa)"
id="7fe4e6a2302e4d9a8c03e3ba4b958c20-4.18.0-147.el8.s390x"
index=2
kernel="/boot/vmlinuz-4.18.0-147.el8.CUSTOMKERNEL.s390x"
args="crashkernel=auto rd.zfcp=0.0.0001,0x5005076802305c49,0x0000000000000000 rd.zfcp=0.0.0002,0x5005076802105c49,0x0000000000000000 rd.zfcp=0.0.0004,0x5005076802305c48,0x0000000000000000 rd.zfcp=0.0.0003,0x5005076802105c48,0x0000000000000000 rd.znet=qeth,0.0.3000,0.0.3001,0.0.3002,layer2=1,portno=0 $tuned_params"
root="UUID=59def7d8-f33f-4aa7-a967-6162cb3efcdf"
initrd="/boot/initramfs-4.18.0-147.el8.CUSTOMKERNEL.s390x.img"
title="Red Hat Enterprise Linux (4.18.0-147.el8.CUSTOMKERNEL.s390x) 8.1 (Ootpa)"
id="7fe4e6a2302e4d9a8c03e3ba4b958c20-4.18.0-147.el8.CUSTOMKERNEL.s390x"
index=3
kernel="/boot/vmlinuz-0-rescue-7fe4e6a2302e4d9a8c03e3ba4b958c20"
args="crashkernel=auto rd.zfcp=0.0.0001,0x5005076802305c49,0x0000000000000000 rd.zfcp=0.0.0002,0x5005076802105c49,0x0000000000000000 rd.zfcp=0.0.0004,0x5005076802305c48,0x0000000000000000 rd.zfcp=0.0.0003,0x5005076802105c48,0x0000000000000000 rd.znet=qeth,0.0.3000,0.0.3001,0.0.3002,layer2=1,portno=0"
root="UUID=59def7d8-f33f-4aa7-a967-6162cb3efcdf"
initrd="/boot/initramfs-0-rescue-7fe4e6a2302e4d9a8c03e3ba4b958c20.img"
title="Red Hat Enterprise Linux (0-rescue-7fe4e6a2302e4d9a8c03e3ba4b958c20) 8.1 (Ootpa)"
id="7fe4e6a2302e4d9a8c03e3ba4b958c20-0-rescue"
```

这个时候，我们看到新打的补丁index=2

```bash
id="7fe4e6a2302e4d9a8c03e3ba4b958c20-4.18.0-147.el8.s390x"
index=2
kernel="/boot/vmlinuz-4.18.0-147.el8.CUSTOMKERNEL.s390x"


```



3. 第三步，把新打的补丁设置为默认选项

   ```bash
   [root@lpar36 ~]#  grubby --set-default-index=2
   The default is /boot/loader/entries/7fe4e6a2302e4d9a8c03e3ba4b958c20-4.18.0-147.el8.CUSTOMKERNEL.s390x.conf with index 2 and kernel /boot/vmlinuz-4.18.0-147.el8.CUSTOMKERNEL.s390x	
   ```

4. 第四步，通过zipl，让配置生效。

   ```bash
   [root@lpar36 ~]# zipl
   Using config file '/etc/zipl.conf'
   Using BLS config file '/boot/loader/entries/7fe4e6a2302e4d9a8c03e3ba4b958c20-4.18.0-147.el8.s390x+debug.conf'
   Using BLS config file '/boot/loader/entries/7fe4e6a2302e4d9a8c03e3ba4b958c20-4.18.0-147.el8.s390x.conf'
   Using BLS config file '/boot/loader/entries/7fe4e6a2302e4d9a8c03e3ba4b958c20-4.18.0-147.el8.CUSTOMKERNEL.s390x.conf'
   Using BLS config file '/boot/loader/entries/7fe4e6a2302e4d9a8c03e3ba4b958c20-0-rescue.conf'
   Run /lib/s390-tools/zipl_helper.device-mapper /boot
   Building bootmap in '/boot'
   Building menu 'zipl-automatic-menu'
   Adding #1: IPL section 'Red Hat Enterprise Linux (4.18.0-147.el8.s390x+debug) 8.1 (Ootpa)'
   Adding #2: IPL section 'Red Hat Enterprise Linux (4.18.0-147.el8.s390x) 8.1 (Ootpa)'
   Adding #3: IPL section 'Red Hat Enterprise Linux (4.18.0-147.el8.CUSTOMKERNEL.s390x) 8.1 (Ootpa)' (default)
   Adding #4: IPL section 'Red Hat Enterprise Linux (0-rescue-7fe4e6a2302e4d9a8c03e3ba4b958c20) 8.1 (Ootpa)'
   Preparing boot device: dm-0.
   Done.	
   ```

   

重启系统，检查一下，果然是用了新的补丁。

```bash
[root@lpar36 ~]# uname -a
Linux lpar36 4.18.0-147.el8.CUSTOMKERNEL.s390x #1 SMP Tue Jun 9 10:48:58 CEST 2020 s390x s390x s390x GNU/Linux
```

