Mount disk to VG / 磁盘挂载到虚拟分区
#######################################


:date: 2018-11-24
:tags: Linux, CentOS7, LVM, Disk
:category: Tools
:slug: Tools_mount_disk_to_vg
:author: Brian Shen
:summary: Tools - Mount Disk to VG

.. _mount_disk_to_vg.rst:

.. contents::

All lines started with :code:`#` should be input. / 所有 :code:`#` 前缀的都是 输入的部分。

Mount A New Disk / 挂载新的磁盘
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Env / 环境
*************

Current, we have 100G Disk. / 当前我们有 100G 磁盘。

.. code-block:: bash

    # lsblk

        NAME                          MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
        sda                             8:0    0  100G  0 disk 
        ├─sda1                          8:1    0  500M  0 part /boot
        └─sda2                          8:2    0 99.5G  0 part 
            ├─centos-root               253:0    0 92.5G  0 lvm  /
            ├─centos-swap               253:1    0    2G  0 lvm  [SWAP]
            └─centos-home               253:2    0    5G  0 lvm  /home
        sr0                            11:0    1 1024M  0 rom  
        loop0                           7:0    0  100G  0 loop 
        └─docker-253:0-134516294-pool 253:3    0  100G  0 dm   
        loop1                           7:1    0    2G  0 loop 
        └─docker-253:0-134516294-pool 253:3    0  100G  0 dm

As we can see, all disks are assigned to root directory. / 所有的磁盘指定给了 根目录。


Add a Disk / 添加一块磁盘
****************************

.. figure:: /images/tools/mount_disk_01.png


.. code-block:: bash
    
    # ls /dev/sd*
        /dev/sda  /dev/sda1  /dev/sda2

Since we didn't restart the PC, OS wouldn't be able to detect the new disk. / 因为我们没有重启， 所有系统发现不了这个新的磁盘。

To force OS reloading disk information, we can execute this: / 为了强制刷新磁盘信息， 我们可以执行以下命令

.. code-block:: bash

    # echo '- - -' > /sys/class/scsi_host/host0/scan
    # ls /dev/sd*
        /dev/sda  /dev/sda1  /dev/sda2  /dev/sdb

Let's see what happened: / 看看发生了什么。

.. code-block:: bash

    # lsblk
        NAME                          MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
        sda                             8:0    0  100G  0 disk 
        ├─sda1                          8:1    0  500M  0 part /boot
        └─sda2                          8:2    0 99.5G  0 part 
            ├─centos-root               253:0    0 92.5G  0 lvm  /
            ├─centos-swap               253:1    0    2G  0 lvm  [SWAP]
            └─centos-home               253:2    0    5G  0 lvm  /home
        sdb                             8:16   0   16G  0 disk 
        sr0                            11:0    1 1024M  0 rom  
        loop0                           7:0    0  100G  0 loop 
        └─docker-253:0-134516294-pool 253:3    0  100G  0 dm   
        loop1                           7:1    0    2G  0 loop 
        └─docker-253:0-134516294-pool 253:3    0  100G  0 dm    

Now we can see a new disk named :code:`sdb` in the disk information.

Creating Linux Partitions in the new added disk / 在新加硬盘上创建 Linux 分区
*******************************************************************************

.. code-block:: bash

    # fdisk /dev/sdb
        Welcome to fdisk (util-linux 2.23.2).

        Changes will remain in memory only, until you decide to write them.
        Be careful before using the write command.

        Device does not contain a recognized partition table
        Building a new DOS disklabel with disk identifier 0x111936e6.

    # Command (m for help): c
        DOS Compatibility flag is set (DEPRECATED!)

    # Command (m for help): u
        Changing display/entry units to cylinders (DEPRECATED!).

    # Command (m for help): p

        Disk /dev/sdb: 17.2 GB, 17179869184 bytes, 33554432 sectors
        255 heads, 63 sectors/track, 2088 cylinders
        Units = cylinders of 16065 * 512 = 8225280 bytes
        Sector size (logical/physical): 512 bytes / 512 bytes
        I/O size (minimum/optimal): 512 bytes / 512 bytes
        Disk label type: dos
        Disk identifier: 0x111936e6

        Device Boot      Start         End      Blocks   Id  System

    # Command (m for help): n
        Partition type:
        p   primary (0 primary, 0 extended, 4 free)
        e   extended
    # Select (default p): p
        Partition number (1-4, default 1): 
        First cylinder (1-2088, default 1): 
        Using default value 1
        Last cylinder, +cylinders or +size{K,M,G} (1-2088, default 2088): 
        Using default value 2088
        Partition 1 of type Linux and of size 16 GiB is set

    # Command (m for help): w
        The partition table has been altered!

        Calling ioctl() to re-read partition table.
        Syncing disks.

Creating a File System / 创建文件系统
****************************************

Let's see what happened: 

.. code-block:: bash

    # lsblk
        NAME                          MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
        sda                             8:0    0  100G  0 disk 
        ├─sda1                          8:1    0  500M  0 part /boot
        └─sda2                          8:2    0 99.5G  0 part 
            ├─centos-root               253:0    0 92.5G  0 lvm  /
            ├─centos-swap               253:1    0    2G  0 lvm  [SWAP]
            └─centos-home               253:2    0    5G  0 lvm  /home
        sdb                             8:16   0   16G  0 disk 
        └─sdb1                          8:17   0   16G  0 part 
        sr0                            11:0    1 1024M  0 rom  
        loop0                           7:0    0  100G  0 loop 
        └─docker-253:0-134516294-pool 253:3    0  100G  0 dm   
        loop1                           7:1    0    2G  0 loop 
        └─docker-253:0-134516294-pool 253:3    0  100G  0 dm

And now, we should format the partition. / 现在我们格式化这个分区。

.. code-block:: bash

    # /sbin/mkfs.ext4 /dev/sdb1


Mount it to Linux Virtual System (LVS) / 挂载到 Linux 虚拟分区
****************************************************************

Let's check LVS. / 查看当前的 Linux 虚拟分区。

.. code-block:: bash

    # lvs
        WARNING: Not using lvmetad with older version.
        LV   VG     Attr       LSize  Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
        home centos -wi-ao----  5.00g                                                    
        root centos -wi-ao---- 92.50g                                                    
        swap centos -wi-ao----  2.00g

Remember the value of column :code:`VG` ( :code:`centos` ). / 记住 :code:`VG` 的值 ( :code:`centos` )。

Now we create a new physical volume. / 现在我们创建一块物理盘。

.. code-block:: bash

    # pvcreate /dev/sdb1
        WARNING: Not using lvmetad with older version.
    # WARNING: ext4 signature detected on /dev/sdb1 at offset 1080. Wipe it? [y/n]: y
        Wiping ext4 signature on /dev/sdb1.
        Physical volume "/dev/sdb1" successfully created.

And extend it to :code:`VG`  :code:`centos` . / 并且将它拓展到 :code:`VG`  :code:`centos` 。

.. code-block:: bash

    # vgextend centos /dev/sdb1
        WARNING: Not using lvmetad with older version.
        Volume group "centos" successfully extended

Check whether it has been extended correctly: / 检查是否正确的被扩展了。

.. code-block:: bash

    # vgdisplay
        WARNING: Not using lvmetad with older version.
        --- Volume group ---
        VG Name               centos
        System ID             
        Format                lvm2
        Metadata Areas        2
        Metadata Sequence No  6
        VG Access             read/write
        VG Status             resizable
        MAX LV                0
        Cur LV                3
        Open LV               3
        Max PV                0
        Cur PV                2
        Act PV                2
        VG Size               <115.50 GiB
        PE Size               4.00 MiB
        Total PE              29567
        Alloc PE / Size       25472 / 99.50 GiB
        Free  PE / Size       4095 / <16.00 GiB
        VG UUID               RVnCi9-U8gt-DbgA-lu11-pdeO-6o0o-cEfQkC

Notice that there is a Free PE with 8G. So let's extend it logically. / 可以看到存在没有被用到的 PE 16GiB ， 所以是成功的。

Now let's add the free PE to root. / 现在我们可以将这些空余的 PE 指定给根目录。 

.. code-block:: bash

    # lvextend -L +15.9G /dev/centos/root /dev/sdb1
        WARNING: Not using lvmetad with older version.
        Rounding size to boundary between physical extents: 15.90 GiB.
        Size of logical volume centos/root changed from 92.50 GiB (23680 extents) to 108.40 GiB (27751 extents).
        Logical volume centos/root successfully resized.

OK. Only 15.9 Can be added. / 请注意留 0.1G 的空余。 

Now the last step: tell OS  that the file system has been extended. / 最后一步就是告诉系统，文件系统被扩展了

.. code-block:: bash

    # xfs_growfs /dev/centos/root
        meta-data=/dev/mapper/centos-root isize=256    agcount=4, agsize=6062080 blks
                 =                        sectsz=512   attr=2, projid32bit=1
                 =                        crc=0        finobt=0 spinodes=0
        data     =                        bsize=4096   blocks=24248320, imaxpct=25
                 =                        sunit=0      swidth=0 blks
        naming   =version 2               bsize=4096   ascii-ci=0 ftype=0
        log      =internal                bsize=4096   blocks=11840, version=2
                 =                        sectsz=512   sunit=0 blks, lazy-count=1
        realtime =none                    extsz=4096   blocks=0, rtextents=0
        data blocks changed from 24248320 to 28417024

    #### Default installed, if not , type this:  yum install -y xfsprogs.x86_64 

And have a check: / 现在我们看下系统信息：

.. code-block:: bash

    # df -hl
        Filesystem               Size  Used Avail Use% Mounted on
        /dev/mapper/centos-root  109G   17G   92G  16% /
        devtmpfs                 910M     0  910M   0% /dev
        tmpfs                    921M     0  921M   0% /dev/shm
        tmpfs                    921M   17M  904M   2% /run
        tmpfs                    921M     0  921M   0% /sys/fs/cgroup
        /dev/mapper/centos-home  5.0G   33M  5.0G   1% /home
        /dev/sda1                497M  125M  373M  26% /boot
        tmpfs                    185M  4.0K  185M   1% /run/user/0

It succeeds! / 完成了！


Reference
**********

    - CentOS6调整LVM SWAP分区大小 https://www.haiyun.me/archives/centos6-change-lvm-swap.html
    - resize2fs: Bad magic number in super-block while trying to open  https://stackoverflow.com/questions/26305376/resize2fs-bad-magic-number-in-super-block-while-trying-to-open
    - centos7 lvm管理 把/home空间转移给/ https://www.2cto.com/os/201708/668992.html
    - 实战：CentOS不重启，在线添加硬盘  http://blog.51cto.com/skypegnu1/1429375
    - http://blog.csdn.net/rainbow702/article/details/50761380





