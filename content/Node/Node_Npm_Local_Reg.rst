
NPM Local Registry and debug
#############################

:date: 2019-07-19
:tags: Log, Web
:category: Linux
:slug: NPM_Local_Registry_and_debug
:author: Brian Shen
:summary: NPM Local Registry and debug

.. _Node_Npm_Local_Reg.rst:

.. contents::

Why we should use local npm registry
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Decouple building from Internet.
   Especially in China, where connections to npm default registry ( :code:`https://registry.npmjs.org/` ) are very unstable. If our build process depends on such kind of connection, build system could be very fragile and can lead to failures more frequently. 

2. Improve download speed. 

how to establish a local registry 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Please refer to cnpmjs:

- https://github.com/cnpm/cnpmjs.org
- https://github.com/cnpm/cnpmjs.org/wiki/Deploy-a-private-npm-registry-in-5-minutes


How to get basic information of local npm registry 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- UI (default 7002)

  http://ipaddress:7002 

- MySQL - Package versions

  .. code-block:: bash 

    mysql -u root -p
    use cnpmjs
    show tables;
    describe module;

    select name, version, dist_tarball from module WHERE name='bluebird' AND version='3.4.0' LIMIT 10;
    +----------+---------+--------------------------------+
    | name     | version | dist_tarball                   |
    +----------+---------+--------------------------------+
    | bluebird | 3.4.0   | /bluebird/-/bluebird-3.4.0.tgz |
    +----------+---------+--------------------------------+

- Package Locations 

  :code:`~/.cnpmjs.org/nfs/` 

How to use 
^^^^^^^^^^^

.. code-block:: bash 

  npm config set registry http://ipaddress:7001

Other Tips 
^^^^^^^^^^^

- Using local registry doesn't mean that internet can be totally disconnected

  Packages such as  :code:`phantom-prebuild` contains some system dependencies ( :code:`phantomjs` ). Without it, npm will try to download binaries from internet.

  Other examples: 
  
  - :code:`phantom-prebuild` : need to install :code:`phantomjs` manually first. 
  - :code:`ffi` : need to be compiled with node libraries. I'm using node 8.16.0, so  https://nodejs.org/download/release/v8.16.0/node-v8.16.0-headers.tar.gz is needed.
  
    Download from internet and then config nodedir： 

    :code:`/plugins-scripts/Dockfile` 。

    .. code-block:: bash 

      tar -xvf /plugins-scripts/node-v6.14.3-headers.tar.gz
      npm config set nodedir /node-v6.14.3
  
  - :code:`vis-react` : This package wrappers :code:`vis` , and it will secretly download :code:`vis` from github. Totally a disaster. Try use :code:`react-graph-vis` . 


- Sync can be a long progress

  Many reasons. The first is the internet speed. The second is that all dependencies and all versions should be downloaded.

  So what if we need a package urgently? 

  Try go to http://ipaddress:7002 to search and sync manually.

- How to debug why npm fails with local registry?

  :code:`npm install --loglevel verbose` 

  By using this, it will print nearly all information you need. Especially steps about internet connections.
