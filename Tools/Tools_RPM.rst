
Build RPM / 构建 RPM
#####################

:date: 2018-07-16
:tags: Linux, CentOS7, RPM
:category: Tools
:author: Brian Shen
:slug: Build_RPM
:summary: Build RPM

.. _build_rpm.rst:

.. contents::

Why I need RPM packages? / 为什么需要RPM包
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here is the thing, I have to delivery my softwares to my customers. I developed it , deployed it and configured it. Everything works just perfect fine. But how should my customers use them, I cannot just gave it to them all the jar, js and shell packages. They need a packed executable binary and it would be more welcome if little configuration is needed.

我需要向客户提交最终的安装软件。所有的事情在本地都是OK的，开发，部署 以及 配置。但是，客户们应该怎么使用他们？ 我不能将所有的开发编译文件直接发给客户，复杂的配置 会让客户失去耐心。他们需要的只是一个安装包，如果开箱即用 或者 根本不用配置的话，那么将会非常棒。

Based on the situation, it is necessarily to give customers what they want, a RPM package.
However, it is either easy or difficult, but I have to say I spend a whole day in successfully building one.  

在这种情况下，最好是给出一个rpm安装包。 这项工作其实不简单 也 不困难，但是我实实在在用了一整天。

How to set Env / 搭建环境
^^^^^^^^^^^^^^^^^^^^^^^^^^

Preparations / 准备
********************

- CentOS 7 1511
- Minimal installation  / 最小化安装
- Network configured / 配置好网络

Needed dev and build environments / 需要的开发环境
****************************************************

    :code:`sudo yum install rpmdevtools rpmlint -y`

Make Essential Directories / 创建必要的目录
*********************************************

    Now go to home directory and make essential sub directories. 
    
    去往 用户目录 并且创建他们。

    .. code-block:: bash
        
        cd ~
        rpmdev-setuptree

    Let's see what happened. ( :code:`tree` ) / 看看发生了什么。

    .. code-block:: bash

        rpmbuild/
        ├── BUILD     : All files will be put here during rpm building
        ├── RPMS      : Built packages will finally be in RPMS and SRPMS 
        ├── SOURCES   : Source files you want to include or use in RPM
        ├── SPECS     : Instruction of how to build RPM 
        └── SRPMS     : Built packages will finally be in RPMS and SRPMS 

Prepare a sample file / 准备一个示例文件
******************************************

To avoid any complexities, we only build a rpm package including a bash command.

为了避免复杂，我们开发一个只包含一个bash命令的rpm包。

.. code-block:: bash

    mkdir briansample-1.0
    cd briansample-1.0/
    vi briansample.sh

In the shell file, the content is :code:`echo "Brian Sample"` .

shell文件的内容是： :code:`echo "Brian Sample"` 。

And we compress them into a tar file. :code:`tar -cf briansample.tar briansample-1.0/` .
Remember the folder name :code:`briansample-1.0` (name-version) because it will usually be used in somewhere else.

将这个文件放入tar包。
记住，这个文件夹的名字是 :code:`briansample-1.0` ， 也就是 是 名字 + 版本号。 这会在其他地方用到。 而且名字版本号的匹配至关重要。

Copy the tar file to :code:`SOURCE` directory.
将这个源文件 tar 包 拷贝到 :code:`SOURCE` 目录下。

Define a SPEC file to list steps / 定义SPEC文件
*************************************************

.. code-block:: bash

    cd rpmbuild/SPECS/
    rpmdev-newspec

This command will create a SPEC file under the directory. ( :code:`tree` )

上一条命令将会创建一个 SPEC 规范文件。

.. code-block:: bash

    .
    └── newpackage.spec

See what it contains ( :code:`cat newpackage.spec` ) :

看看里面的内容。

.. code-block:: bash

    Name:
    Version:
    Release:        1%{?dist}
    Summary:

    License:
    URL:
    Source0:

    BuildRequires:
    Requires:

    %description


    %prep
    %setup -q


    %build
    %configure
    make %{?_smp_mflags}


    %install
    rm -rf $RPM_BUILD_ROOT
    %make_install


    %files
    %doc



    %changelog


It is very clear that it consists of two many parts:

非常直观，其实包括两个部分：

    - Basic descriptions / 基本描述
    - RPM steps / RPM 编译步骤

- Definitions / 一些定义:

    - :code:`%description`

        A full description of the software packaged in the RPM. This description can span multiple lines and can be broken into paragraphs.

    - :code:`%prep`

        Command or series of commands to prepare the software to be built, for example, unpacking the archive in Source0. This directive can contain a shell script.

    - :code:`%build`

        Command or series of commands for actually building the software into machine code (for compiled languages) or byte code (for some interpreted languages).

    - :code:`%install`

        Command or series of commands for copying the desired build artifacts from the %builddir (where the build happens) to the %buildroot directory (which contains the directory structure with the files to be packaged). This usually means copying files from ~/rpmbuild/BUILD to ~/rpmbuild/BUILDROOT and creating the necessary directories in ~/rpmbuild/BUILDROOT. This is only run when creating a package, not when the end-user installs the package. See Working with SPEC files for details.

    - :code:`%check`

        Command or series of commands to test the software. This normally includes things such as unit tests.

    - :code:`%files`

        The list of files that will be installed in the end user’s system.

    - :code:`%changelog`

        A record of changes that have happened to the package between different Version or Release builds.


When we want to ignore some steps / 如果我们想忽略一些步骤的话
**************************************************************

.. warning::

    When I wanted to ignore some steps, I like to comment out them. For example, NodeJS and Python programs do not need build step.
    
    当我想要忽略这些步骤的时候，本能的反映是 注释掉他们。 比方说 NodeJS 或者Python 程序，就不需要 build 步骤。

    .. code-block:: bash

        %build
        with 
        #%build

    But !!!!!!! This doesn't actually comment it out. and it will still run.
    So deleting :code:`%build` and :code:`%configure` makes things work as expected.

    但是！！！ 这并不会阻止这些程序继续运行。需要去删除这些步骤 才能工作正常。

Continue with our sample / 继续
*********************************

Copy our project tar files to :code:`rpmbuild/SOURCES/` by code:

将整个工程拷贝至 :code:`rpmbuild/SOURCES/` 。

.. code-block:: bash

    cd ~
    cp briansample.tar rpmbuild/SOURCES/

Now edit our SPEC file: / 现在我们来更改SPEC 文件：

.. code-block:: bash

    Name:           briansample  #####watch the name  注意名称
    Version:        1.0          #####watch the version 注意版本
    Release:        1%{?dist}
    Summary:        sample

    License:        GPL
    Source0:        briansample.tar

        
    %description

    %prep
    echo "BrianSample Prepare"
    # this Step will unpack the tar file briansample.tar
    %setup -q

    %install
    echo "BrianSample Install"
    # this Step will enter ./briansample-1.0 , just like the name and Version
    # And then you can execute commands here
    # So we copy file (ths bash file) to virtual directory %{buildroot}/usr/briansample 
    mkdir -p %{buildroot}/usr/briansample
    pwd
    cp -rf ./* %{buildroot}/usr/briansample

    %post 
    # execute when installed in the real machine

    %files
    %doc
    # files will in teh virtual directory will be copied here in teh real machine
    /usr/briansample/*

    %changelog

And we can now build our RPM package. / 现在我们可以去编译 RPM 包了。

    :code:`rpmbuild -ba newpackage.spec`

.. code-block:: bash

    rpmbuild -ba newpackage.spec
        Executing(%prep): /bin/sh -e /var/tmp/rpm-tmp.h7l5eo
        + umask 022
        + cd /home/admin/rpmbuild/BUILD
        + echo 'BrianSample Prepare'
        BrianSample Prepare
        + cd /home/admin/rpmbuild/BUILD
        + rm -rf briansample-1.0
        + /usr/bin/tar -xf /home/admin/rpmbuild/SOURCES/briansample.tar
        + cd briansample-1.0
        + /usr/bin/chmod -Rf a+rX,u+w,g-w,o-w .
        + exit 0
        Executing(%install): /bin/sh -e /var/tmp/rpm-tmp.HEqZg2
        + umask 022
        + cd /home/admin/rpmbuild/BUILD
        + '[' /home/admin/rpmbuild/BUILDROOT/briansample-1.0-1.el7.centos.x86_64 '!=' / ']'
        + rm -rf /home/admin/rpmbuild/BUILDROOT/briansample-1.0-1.el7.centos.x86_64
        ++ dirname /home/admin/rpmbuild/BUILDROOT/briansample-1.0-1.el7.centos.x86_64
        + mkdir -p /home/admin/rpmbuild/BUILDROOT
        + mkdir /home/admin/rpmbuild/BUILDROOT/briansample-1.0-1.el7.centos.x86_64
        + cd briansample-1.0
        + echo 'BrianSample Install'
        BrianSample Install
        + mkdir -p /home/admin/rpmbuild/BUILDROOT/briansample-1.0-1.el7.centos.x86_64/usr/briansample
        + pwd
        /home/admin/rpmbuild/BUILD/briansample-1.0
        + cp -rf ./briansample.sh ./briansample.tar /home/admin/rpmbuild/BUILDROOT/briansample-1.0-1.el7.centos.x86_64/usr/briansample
        + '[' '%{buildarch}' = noarch ']'
        + QA_CHECK_RPATHS=1
        + case "${QA_CHECK_RPATHS:-}" in
        + /usr/lib/rpm/check-rpaths
        + /usr/lib/rpm/check-buildroot
        + /usr/lib/rpm/redhat/brp-compress
        + /usr/lib/rpm/redhat/brp-strip /usr/bin/strip
        + /usr/lib/rpm/redhat/brp-strip-comment-note /usr/bin/strip /usr/bin/objdump
        + /usr/lib/rpm/redhat/brp-strip-static-archive /usr/bin/strip
        + /usr/lib/rpm/brp-python-bytecompile /usr/bin/python 1
        + /usr/lib/rpm/redhat/brp-python-hardlink
        + /usr/lib/rpm/redhat/brp-java-repack-jars
        Processing files: briansample-1.0-1.el7.centos.x86_64
        Provides: briansample = 1.0-1.el7.centos briansample(x86-64) = 1.0-1.el7.centos
        Requires(interp): /bin/sh
        Requires(rpmlib): rpmlib(CompressedFileNames) <= 3.0.4-1 rpmlib(FileDigests) <= 4.6.0-1 rpmlib(PayloadFilesHavePrefix) <= 4.0-1
        Requires(post): /bin/sh
        Checking for unpackaged file(s): /usr/lib/rpm/check-files /home/admin/rpmbuild/BUILDROOT/briansample-1.0-1.el7.centos.x86_64
        Wrote: /home/admin/rpmbuild/SRPMS/briansample-1.0-1.el7.centos.src.rpm
        Wrote: /home/admin/rpmbuild/RPMS/x86_64/briansample-1.0-1.el7.centos.x86_64.rpm
        Executing(%clean): /bin/sh -e /var/tmp/rpm-tmp.UhdYZ0
        + umask 022
        + cd /home/admin/rpmbuild/BUILD
        + cd briansample-1.0
        + /usr/bin/rm -rf /home/admin/rpmbuild/BUILDROOT/briansample-1.0-1.el7.centos.x86_64
        + exit 0

Now let's see what had been generated :code:` tree /home/admin/rpmbuild/`
现在看看生成了什么！

.. code-block:: bash

    /home/admin/rpmbuild/
    ├── BUILD
    │   └── briansample-1.0
    │       ├── briansample.sh
    │       └── briansample.tar
    ├── BUILDROOT
    ├── RPMS
    │   └── x86_64
    │       └── briansample-1.0-1.el7.centos.x86_64.rpm
    ├── SOURCES
    │   └── briansample.tar
    ├── SPECS
    │   └── newpackage.spec
    └── SRPMS
        └── briansample-1.0-1.el7.centos.src.rpm

And we can just install the package:
我们可以去安装这个 RPM 包。

:code:`sudo yum install ./briansample-1.0-1.el7.centos.x86_64.rpm`

And after installation, let's see what happened. Do all files copied to the destination?
安装完毕后，看看是否执行正确。

.. code-block:: bash

    tree /usr/briansample/
    /usr/briansample/
    ├── briansample.sh
    └── briansample.tar

Yes, now our work is done.
是的，工作完成

Concerns / 一些考量
^^^^^^^^^^^^^^^^^^^

- How can I install other packages during the installation. 

    如果我有一些 依赖的 rpm 包应该怎么办？

    For example, I also want to install some helper tools like :code:`vim` and I have the rpm packages. But we cannot do this, because yum will lock DB during installation, you will get DB locked error in the :code:`%post` section.

    比方说，我需要安装一些辅助的工具，比如 :code:`vim` ， 并且我能下载这些rpm包。其实很难做到这一点。因为 yum 在安装过程中会将 DB 锁住。 如果我们在 :code:`%post`  安装其他rpm 包的时候，会得到一个 DB 锁无法获取的错误。

    One solution is to  remove the lock :code:`rm -rf /var/lib/rpm/.rpm.lock` . However, this is not recommended.

    有一个解决方法是 ， 移除这个锁，但是并不推荐。

- What about un-installation?

- What about patch?

Other tips / 其他的技巧
^^^^^^^^^^^^^^^^^^^^^^^^^

- Unpack the rpm file / 如何解压一个 rpm 包

    In Windows, you can use 7z software todo this. 
    Windows 下可以使用 7z 这样的软件。

    In Linux: :code:`rpm2cpio ./packagecloud-test-1.1-1.x86_64.rpm | cpio -idmv`
    Linux 下使用这个命令工具； rpm2cpio 。

- How to force to install packages / 如何强制安装软件包

    If your rpm database is destroyed, it is much difficult to restore it. 
    The only way that I found is to download in the same machine and install it then.

    如果 rpm 元数据库被损坏的话，非常难去恢复。
    一个办法就是 去同样环境的机器上 下载，强制安装软件。

.. code-block:: bash

    rpm -Uvh /usr/uap/repo/*rpm --nodeps --scripts --force 
    -i install packages
    -v provide more details
    -h print hash marks to show progress
    --nodepes:  don't verify package dependencies
    --scripts: list install/erase scriptlets from package(s)
    --force:   
        --replacefiles                   ignore file conflicts between packages
        --replacepkgs                    reinstall if the package is already present

    rpm -ivh ./*rpm --justdb --nodeps --scripts --force


Reference:
^^^^^^^^^^^^^

    - Set Up an RPM Build Environment under CentOS : https://wiki.centos.org/HowTos/SetupRpmBuildEnvironment
    - Rpmbuild Tutorial https://rpmbuildtut.wordpress.com/
    - RPM Packaging Guide https://rpm-packaging-guide.github.io/