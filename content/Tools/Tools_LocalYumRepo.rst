
Local Yum Repo (CentOS 7) / 本地Yum源
#######################################

:date: 2017-11-14
:tags: Linux, CentOS
:category: Tools
:slug: local_yum_repo
:author: Brian Shen
:summary: Local Yum Repo

.. _local_yum_repo.rst:

.. contents::

Intro 简介
^^^^^^^^^^^

This article is sampled by installing Java.

基于JAVA介绍如何使用本地Yum源。

Prepare the packages / 准备安装包
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Find a clean CentOS with network available.

    找一个干净的 CentOS 环境，并且接通网络。

- Download Software Packages 下载软件包

    To download software and their dependencies, you can just use native :code:`yum` .

    只需要使用 :code:`yum` 就可以下载并且解析依赖包。

    - Create a folder / 创建文件夹

        .. code-block:: bash

            mkdir ais_repo
            cd ais_repo

    - Download OpenJDK / 下载 OpenJDK

        .. code-block:: bash

            sudo yum install --downloadonly --downloaddir ./ java-1.8.0-openjdk-headless.x86_64

        .. figure::  /images/tools/local_repo_01.png


- Make Local Repo / 制作本地 Yum 库

    It seems quite hard to create your own repo, since there are lots of package information to create and add.
    But actually it is quite simple, and you can just make repo with simple commands.

    看起来很是复杂，因为有很多的依赖关系，但实际上，只需要很简单的命令就可以。

    - Install :code:`createrepo` / 安装 :code:`createrepo`

        :code:`sudo yum install createrepo`

    - create a directory to put packages and then make repo in that folder

        创建一个目录来保存这些安装包。并且，制作安装包的元文件信息。

        .. code-block:: bash

            sudo mkdir /usr/share/ais_repo
            sudo mv ./* /usr/share/ais_repo
            sudo createrepo -v /usr/share/ais_repo

        Let's see what happened: / 看看发生了什么

        .. figure::  /images/tools/local_repo_02.png

        As you can notice, there is an extra folder :code:`repodata` . Now, this is a local repo.

        可以看出来，文件夹中多了一个 :code:`repodata` 。

Use your own REPO / 使用这个Yum源
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Backup all the repo files. / 备份已经存在的 Yum 源配置文件

    .. code-block:: bash

        cd /etc/yum.repos.d/
        sudo mkdir bak
        sudo mv *.repo ./bak

- Create local repo source file :code:`/etc/yum.repos.d/local.repo`

    为本地的Yum源添加配置

    .. code-block:: bash

        #name
        [local_server]
        #description
        name=Thisis a local repo
        #yum source
        baseurl=file:///usr/share/ais_repo
        enabled=1
        #check GPG-KEY
        gpgcheck=0

- Make local yum source, clear cache and start cache. 清除缓存，开始使用本地Yum源。

    .. code-block:: bash

        sudo yum clean all
        sudo yum makecache

Installation / 安装
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    cd /usr/share/ais_repo/
    sudo yum install java-1.8.0-openjdk-headless-1.8.0.144-0.b01.el7_4.x86_64.rpm

Reference 
^^^^^^^^^

- https://yq.aliyun.com/ziliao/97558/