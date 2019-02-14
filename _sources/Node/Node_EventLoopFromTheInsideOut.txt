Node Event Loop From The Inside Out
#####################################


:date: 2019-02-12
:tags: Node, Event Loop
:category: Node
:slug: Node_Event_Loop_From_The_Inside_Out
:author: Brian Shen
:summary: Node Event Loop From The Inside Out

.. _Node_Event_Loop_From_The_Inside_Out_rst:

.. contents::

Linux/Unix Programer
*********************

- Scale Problem

  .. code-block:: C 

    int server = socket();
    bind(server, 80);
    listen(server);

    while(int connection = accept(server)){
      pthread_create(echo, connection);
    }

    void echo(int connection){
      char buf[4096];
      while(int size = read(connection, buffer, sizeof buf)) {
        write(connection, buffer, size);
      }
    }

  Old system can only handle about hundreds threads. So it doesn't scale out.

- Scale solution: epoll - setup

  epoll -> Linux
  KQ -> Mac 

  .. code-block:: C 

    int server = .. // like before
    int evetfd = epoll_create1(0);
    struct epoll_event ev = (.event = EPOLLIN, .data.fd = server);
    epoll_ctl(epollfd, EPOLL_CTL_ADD, server, &ev);

    ...
    struct epoll_event events[10];
    while( int max = epoll_wait(eventfd, event, 10)) {
      for(n = 0; n< max; n++){
        if(events[n].data.fd.fd == server) {
          // Server socket has connection!
          int connection = accept(server);
          ev.events = EPOLLIN;
          ev.data.fd = connection;
          epoll_ctl(fd, EPOLL_CTL_ADD, connection, &ev);
        } else {
          // connection socket has data
          char buf[4096];
          int size = read(connection, buffer, sizeof buf);
          write(connection, buffer, size);
        }
      }
    }

What is Node Event Loop?
*************************

A semi-infinite loop, polling and blocking on the O/S until in a set of file descriptors are ready.

Something interesting happened, and node will pass it to JavaScript.

- event 
- callback 
- fs thing

When does Node exit?
*********************

It exits when it no longer had any events to wait for, at which points the loop must complete.

can everything be async?
************************

Can we poll for all system activity Node.js wants to be notified of? In other words, can everything be async?

Yes and no? There are basically three cases of things:

1. Pollable file descriptors: can be directly waited on 

  sockets (net/dgram/http/tls/https/child_process pipes/stdin,out,err)
  classic, well supported

2. Time: next timeout can be directly wait on 

  (timeouts and intervals)
  poll(..., int timeout)
  kqueue(..., struct timespec * timeout)
  epoll_wait(..., int timeout, ...)

  timeout resolution is milliseconds, timespec is nanoseconds, but both are rounded up to system clock granularity.

  Only one timeout at a time can be waited on, but Node.js keeps all timeout sorted, and sets the timeout value to the next one.

3. Everything else: must happen off loop, and signal back to the loop when done.

Details
********

- Not pollable: file system 

  Everything in fs.* uses uv thread poll (unless they are sync).
  The blocking call is made by a thread, and when it completes, readiness is signaled back to the event loop using either an eventfd or a self pipe. 

  .. tip::

    self-pipe: 
    A pipe, where one end is written to by a thread or a signal handler, and the other end is polled in the loop. Traditional way to "wake up" a polling loop when the event to wait for is not directly representable as a file descriptor. 

- Sometimes pollable: dns 

  - :code:`dns.lookup()` calls :code:`getaddrinfo()` , a function in the system resolver library that makes blocking socket calls and cannot be integrated into a polling loop. Like fs.*, it's called in the thread pool. 
  - :code:`dns.<everything else>` calls functions in c-ares, a non-blocking DNS resolver, and integrates with the loop, not the thread poll.

  Docs bend over backwards to explain how these two differ, but now that you know that blocking library calls must be shunted off to the thread pool, whereas DNS queries use TCP/UDP and can integrate into the event loop, the distinction should be clear.

- Pollable: signals 

  The ultimate async... uses the self-pipe pattern to write the signal number to the loop.

  Note that listening for signals doesn't "ref" the event loop, which is consistent with signal usage as "probably won't happen" IPC mechanism.

- Pollable: child processes 

  - Unix signals child process termination with SIGCHILD.
  - Pipes between the parent and child are pollable.

- Sometimes pollable: C++ addons 

  Addons should use the UV thread pool or integrate with the loop, but can do anything, including making loop-blocking system calls (perhaps unintentionally).

  Hints:

  - Review addon code 
  - Track loop metrics


Important notes about the UV thread pool
*******************************************

It is shared by: 

  - fs 
  - dns (only dns.lookup(), rest is fine)
  - crypto (only crypto.randomBytes() and crypto.pbkdf2())
  - http,get/request() (if called with a name, dns.lookup() is used)
  - any C++ addons that use it

Default number of threads is 4, significantly parallel users of the above should increase the size. 

Hints:

- Resolve DNS names yourself, using the direct APIs to avoid dns.lookup(), and stay out of the thread pool 
- Increase the thread pool size with UV_THREADPOOL_SIZE

You should now be able to describe:

- What is the event loop
- When is node multi-threaded 
- Why it "scales well"



Linux/Unix 程序员问题
**********************

- 扩展问题

  .. code-block:: C 

    int server = socket();
    bind(server, 80);
    listen(server);

    while(int connection = accept(server)){
      pthread_create(echo, connection);
    }

    void echo(int connection){
      char buf[4096];
      while(int size = read(connection, buffer, sizeof buf)) {
        write(connection, buffer, size);
      }
    }

  像这样为每一个连接创建一个进程，非常的耗费系统资源。老旧的系统只能处理几百个进程，所以这样的设计思想是不能扩展的。

- 扩展问题解决方案 epoll

  epoll -> Linux
  KQ -> Mac 

  .. code-block:: C 

    int server = .. // like before
    int evetfd = epoll_create1(0);
    struct epoll_event ev = (.event = EPOLLIN, .data.fd = server);
    epoll_ctl(epollfd, EPOLL_CTL_ADD, server, &ev);

    ...
    struct epoll_event events[10];
    while( int max = epoll_wait(eventfd, event, 10)) {
      for(n = 0; n< max; n++){
        if(events[n].data.fd.fd == server) {
          // Server socket has connection!
          int connection = accept(server);
          ev.events = EPOLLIN;
          ev.data.fd = connection;
          epoll_ctl(fd, EPOLL_CTL_ADD, connection, &ev);
        } else {
          // connection socket has data
          char buf[4096];
          int size = read(connection, buffer, sizeof buf);
          write(connection, buffer, size);
        }
      }
    }

什么是 Node 事件循环
*************************

一个近似无限的循环，轮询并且阻塞系统，直到一系列的文件句柄准备完成。

当一些Node感兴趣的事件发生时，Node会将这些事件转发给 JavaScript。

- 事件 
- 回调 
- 文件操作相关

Node什么时候退出？
*********************

当不在有等待的事件时，循环就完成了，不再继续执行。

所有事件都可以异步么？
************************

我们能够轮询所有Node想知道的系统活动么？所有的事件都可以是异步的么？

有的可以，有的不可以。基本来说，有 3 中事件：

1. 可轮询的文件句柄：能够被直接等待

  sockets (net/dgram/http/tls/https/child_process pipes/stdin,out,err)
  经典的，支持的很好

2. 定时器：下一个超时时间能够被直接等待

  (timeouts and intervals)
  poll(..., int timeout)
  kqueue(..., struct timespec * timeout)
  epoll_wait(..., int timeout, ...)

  timeout的精度是 毫秒， timespec 是纳秒。 但是两者都会按照系统时钟刻度去近似。

  只能等待一个超时，所以 Node.js 会将所有的超时排序，并且每次都等待最近的一个。

3. 其他： 一定要在循环外部发生，并且完成时发送信号给循环。

详情
********

- 不可轮询： 文件系统 

  所有的 fs.* 相关的，都会使用 uv 进程池（除非调用是同步的）。
  这些阻塞调用是由单独一个进程调用的，当动作完成时，可读信号会被发送给循环，通过 eventfd 或者 self pipe。

  .. tip::

    self pipe : 
    一种管道，一端是由一个进程 或者 信号处理写入，另一端是循环读取。
    如果等待的事件不能被直接的表示为一个文件句柄，传统的方式是叫醒事件循环。

- 有时可轮询 : dns 

  - :code:`dns.lookup()` 会调用 :code:`getaddrinfo()` , 这个函数会调用阻塞的套接字，素以不能够被集成到循环中。像 fs.* 一样，他是在进程池中被调用的。 
  - :code:`dns.<everything else>` 调用是非阻塞的，可以集成进循环，不是在进程池中执行的。

  这两者是有区别的，但是你现在可以知道，阻塞的库调用必须在进程池中调用，而DNS 查找等可以被集成到事件循环中。一定要清楚这些区别。

- 可轮询: 信号 

  最终的异步 使用 self pipe 向循环中写入信号量标号。

  请注意 监听信号 并不被推荐在事件循环中，因为他们有可能不会发生。

- 可轮询 : 子进程 

  - Unix 子进程结束时会发出 SIGCHILD.
  - 父子管道直接是可以轮询的

- 有时可轮询 :  C++ addons 

  插件应该使用 UV 的进程池 或者 和 循环集成，但是实际上他是可以做任何事情的，包括调用 阻塞循环的系统调用。

  使用插件时要注意:
  
  - 审核插件代码
  - 追踪循环指标

关于 UV 进程池的重要信息
*******************************************

他是被以下共享的：

  - fs 
  - dns (only dns.lookup(), rest is fine)
  - crypto (only crypto.randomBytes() and crypto.pbkdf2())
  - http,get/request() (if called with a name, dns.lookup() is used)
  - any C++ addons that use it

默认情况下，进程数是 4， 大量使用以上功能的，需要扩大这个大小。


一些技巧:

- 自行解析 DNS名称，避免调用 dns.lookup()
- 使用 UV_THREADPOOL_SIZE 扩大进程池大小

你现在应该能够知道： 

- 什么是事件循环
- 什么时候 Node 是多进程的
- 为什么，它能够很好的扩展


.. disqus::
    :disqus_identifier: _Node_Event_Loop_From_The_Inside_Out_rst