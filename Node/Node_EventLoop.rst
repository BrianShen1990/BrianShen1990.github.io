The Node.js Event Loop, Timers, and :code:`process.nextTick()`
#################################################################


:date: 2019-02-03
:tags: Node
:category: Node
:slug: The_Node_js_Event_Loop
:author: Brian Shen
:summary: The Node.js Event Loop, Timers, and :code:`process.nextTick()`

.. _the_node_js_event_loop.rst:

.. contents::

Intro
^^^^^

Reference: https://nodejs.org/en/docs/guides/event-loop-timers-and-nexttick/

什么是事件循环？
^^^^^^^^^^^^^^^^^^^

事件循环能够让 Node.js 处理非阻塞的I/O操作 -- 虽然JavaScript 是单线程的 -- 在可能的时候将这些操作转交给系统内核去处理。

因为大多数现代内核都是 多线程的，他们能在后台处理多项操作。当某一项操作完成时，内核会通知 Node.js，这样的话对应的回调就会被加入到 轮询队列中，最终会被执行。我们会在晚一些做一个详细的介绍。

事件循环解释
^^^^^^^^^^^^^^^^

当Node.js 启动时，会初始化事件循环，处理输入的脚本（或者丢给 REPL ，在这个文档中我们不包含），这些脚本可能会会有一步的API 调用， 定时器 或者 调用 :code:`process.nextTick()` ，然后，开始处理事件循环。

以下这张图 是 事件循环操作顺序的概览。

.. code-block:: bash 

       ┌───────────────────────────┐
    ┌─>│           timers          │
    │  └─────────────┬─────────────┘
    │  ┌─────────────┴─────────────┐
    │  │     pending callbacks     │
    │  └─────────────┬─────────────┘
    │  ┌─────────────┴─────────────┐
    │  │       idle, prepare       │
    │  └─────────────┬─────────────┘      ┌───────────────┐
    │  ┌─────────────┴─────────────┐      │   incoming:   │
    │  │           poll            │<─────┤  connections, │
    │  └─────────────┬─────────────┘      │   data, etc.  │
    │  ┌─────────────┴─────────────┐      └───────────────┘
    │  │           check           │
    │  └─────────────┬─────────────┘
    │  ┌─────────────┴─────────────┐
    └──┤      close callbacks      │
       └───────────────────────────┘

注意：每一个方框都会被定义成事件循环的一个阶段。

每个阶段都会有一个先进先出 FIFO 的队列，包含了需要执行的回调。每一个阶段都有自己独特的行为，通常来说，当事件循环到达指定的阶段时，他们会去执行指定给这个阶段的特定操作，然后去执行这个阶段的回调队列，一直到这个队列为空或者达到回调数目限制。此时，事件循环将会进入到下一个阶段，如此。

因为任何的操作都可能产生更多的操作 和 新的需要在轮询阶段由内核处理的事件，轮询事件能够在 轮询 阶段正在被处理的时候被加入轮询队列。最终的结果是，长期运行的回调能够使得轮询阶段运行的比定时器临界值 还要长。请查看 定时器 和 轮询 小节获得更多细节。

注意： 在 Windows 和 Unix/Linux上，这个实现会有所不同，但是对这个演示并不重要。最重要的部分在这，实际上有7-8个步骤，但是我们需要关心的，Node.js 实际使用的，就是上面这些阶段。

阶段概览
^^^^^^^^^^

- 定时器：这阶段执行 :code:`setTimeout()` 以及 :code:`setInterval()` 的定时任务
- 等待的回调：执行 延迟到下一个循环的 I/O 回调
- 空，准备：内部使用
- 轮询：获取新的I/O事件；执行I/O相关的回调（包含除关闭回调、由定时器或者 :code:`setImmediate()` 产生的回调 以外的所有的回调）；合适的时候node会在这边被阻塞
- 检查：:code:`setImmediate()` 产生的回调会在这边执行
- 关闭的回调：一些关闭的回调会在这边执行，比方说 :code:`socket.on('close', ...)` 

在每一轮事件循环中间，Node.js 会检查是否有异步的I/O 操作或者定时器操作， 如果没有的话，就会自动关闭。

阶段详情
^^^^^^^^^^^

定时器
*******

定时器规定了回调被执行的时间间隔的临界值，而不是准确的值。定时器回到会在一定时间过去之后执行，当然，操作系统调度 或者 其他的回调可能会使得他们被延迟。

注意：技术上来说，轮询阶段控制着 什么时候定时器会被执行。

举例来说，你安排了一个在100ms以后的定时器，之后你的脚本启动了并且异步的读取一个文件内容，消耗95ms。

.. code-block:: javascript

  const fs = require('fs');

  function someAsyncOperation(callback) {
    // Assume this takes 95ms to complete
    fs.readFile('/path/to/file', callback);
  }

  const timeoutScheduled = Date.now();

  setTimeout(() => {
    const delay = Date.now() - timeoutScheduled;

    console.log(`${delay}ms have passed since I was scheduled`);
  }, 100);


  // do someAsyncOperation which takes 95 ms to complete
  someAsyncOperation(() => {
    const startCallback = Date.now();

    // do something that will take 10ms...
    while (Date.now() - startCallback < 10) {
        // do nothing
    }
  });

当事件循环进入到轮询 阶段后，有一个空队列（ :code:`fs.readFile()` 还没完成），所以会等待一段时间直到最近的定时器临界值到达。当它等待了95ms之后。:code:`fs.readFile()` 结束了读取数据，他的回调需要消耗10ms去完成，这个回调会被添加到 轮询队列并且被执行。完成后，没有更多在队列中的回调了，所以事件循环会去查看最近的定时器，并且重新循环到 定时器 阶段 去执行定时器回调。

在这个例子中，你可以看到定时器被执行实际上是在 105ms。

注意：为了阻止轮询阶段一直占用事件循环，:code:`libuv` 有一个硬编码的最大的值（系统相关），来限定轮询阶段获取更多的事件。

等待的回调
**************

这个阶段会去执行一些系统操作相关的回调，比方说 TCP 错误。举例来说， 如果TCP socket 在尝试连接的时候接收到了 :code:`ECONNREFUSED` ，一些*nix 系统会等待汇报这个错误。他们会在等待的回调阶段 被执行

轮询
*****

轮询阶段主要有两个功能：

1. 计算他应该阻塞多长时间 并且 轮询 I/O， 然后
2. 处理在轮询队列中的事件。

当事件循环进入到 轮询阶段 并且没有定时器时，会发生两件事情：

- 如果 轮询队列不为空，时间循环会一次执行回调队列中的回调 直到队列为空， 或者依赖系统的 硬编码的时间限制。
- 如果队列为空，那么会有更多的两件事情发生：

  - 如果脚本设定了 :code:`setImmediate()` ，那么事件循环会结束 轮询阶段 并且进入到 检查阶段 去执行这些设定的脚本
  - 如果脚本没有安排 :code:`setImmediate()` ，事件循环会去等待回调被加入到队列中，然后立即去执行。

一旦轮询队列为空，事件循环就会去检查哪些定时器到达了临界值， 如果有一个或者多个定时器准备好了， 那么事件循环就循环回去执行 定时器阶段的回调。

检查
*******

这一阶段允许我们在 轮询阶段 结束之后立马执行回调。如果 轮询阶段为空 并且脚本 设定了 :code:`setImmediate()` ，那么事件循环会继续执行检查阶段 而不是等待。

:code:`setImmediate()` 实际上是一种运行在事件循环 不同阶段的特殊定时器。它使用 libuv 的API 来设定在 轮询阶段完成后的回调。

总体来说，当代码运行后，事件循环最终会到达 轮询阶段，这个阶段回去等待接入的连接、请求等等。当然，如果使用 ·:code:`setImmediate()`  安排了一个回调，并且 轮询阶段为空，那么 轮询阶段就会结束并且进入到检查阶段，而不是在轮询阶段等待。

关闭的回调
**************

如果一个socket 或者处理函数 被强制关闭 （比方说 :code:`socket.destroy()` ）, :code:`'close'` 事件会在这个阶段被触发。否则的话他们会在 :code:`process.nextTick()` 阶段触发。


:code:`setImmediate()` 与 :code:`setTimeout()`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:code:`setImmediate()` 以及 :code:`setTimeout()` 很像，但却会根据他们何时被调用 有不同的行为。

- :code:`setImmediate()` 是为了在 轮询阶段结束运行的脚本
- :code:`setTimeout()` 是为了在一个设定的最小临界值后运行的脚本

哪一个定时器会被执行 会与他们的上下文环境相关。如果两个函数在同一个 模块中被调用，那么定时器会依赖于这个进程的性能（会被这台机器上其他的程序影响）。

举例来说，如果我们在非 I/O 循环中（比方说 主模块）运行下面的脚本，哪一个定时器会被先执行是无法确定的，因为与进程的性能相关。

.. code-block:: javascript

    // timeout_vs_immediate.js
    setTimeout(() => {
      console.log('timeout');
    }, 0);

    setImmediate(() => {
      console.log('immediate');
    });

.. code-block:: javascript 

    $ node timeout_vs_immediate.js
    timeout
    immediate

    $ node timeout_vs_immediate.js
    immediate
    timeout

当然， 如果我们在I/O 循环中 去执行这两个函数，那么 :code:`setImmediate()` 总是会被优先执行。

.. code-block:: javascript

    // timeout_vs_immediate.js
    const fs = require('fs');

    fs.readFile(__filename, () => {
      setTimeout(() => {
        console.log('timeout');
      }, 0);
      setImmediate(() => {
        console.log('immediate');
      });
    });

.. code-block:: javascript

    $ node timeout_vs_immediate.js
    immediate
    timeout

    $ node timeout_vs_immediate.js
    immediate
    timeout

相比 :code:`setTimeout()` ， 使用 :code:`setImmediate()` 的最大好处是 :code:`setImmediate()` 在 I/O 循环中 总是会被优先执行，无论存在多少定时器。

:code:`process.nextTick()`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

理解 :code:`process.nextTick()`
********************************

你可能已经注意到了， :code:`process.nextTick()` 并不在图中， 虽然他是 异步 API 的一部分。这是因为 :code:`process.nextTick()` 并不是 事件循环中的一部分。 实际上，无论处在那一个事件循环阶段， :code:`nextTickQueue` 会在当前的操作完成后，立马被执行。

重新看一下之前的图，任何时候你调用 :code:`process.nextTick()` ，他都会被立马执行。这会造成一些很坏的情况 因为这样会允许你用循环的 :code:`process.nextTick()` 去阻塞 I/O 。这意味着 事件循环不会到达轮询阶段。 

为什么这样被允许？
******************

为什么这样的事情在 Node.js 中会被允许？部分的原因是因为 这样的一种设计思路：API 应当总是被异步执行，即使并不需要。 我们通过下面的代码片段来查看：

.. code-block:: javascript 

    function apiCall(arg, callback) {
      if (typeof arg !== 'string')
        return process.nextTick(callback,
                                new TypeError('argument should be string'));
    }

此处的代码片段会做一个简单的参数检测，如果不对的话，会给回调抛出一个异常。这个 API 最近进行了更新，可以传递参数给 :code:`process.nextTick()` 来传给回调，这样就不需要函数嵌套了。

我们所做的就是 传递一个错误 给用户，但是需要在我们允许其他代码被执行的情况下。 利用 :code:`process.nextTick()` 我们保证了 :code:`apiCall()` 在其他代码被执行之后、事件循环继续之前 总是会运行回调。为达到这个效果，JS 调用栈 被允许 展开 然后 立马执行 提供的回调，这样就能够递归调用 :code:`process.nextTick()` 而不会产生 :code:`RangeError: Maximum call stack size exceeded from v8` 的错误。

这种哲学可能会产生一些潜在的问题，以下面的代码片段为例：

.. code-block:: javascript

    let bar;

    // this has an asynchronous signature, but calls callback synchronously
    function someAsyncApiCall(callback) { callback(); }

    // the callback is called before `someAsyncApiCall` completes.
    someAsyncApiCall(() => {
      // since someAsyncApiCall has completed, bar hasn't been assigned any value
      console.log('bar', bar); // undefined
    });

    bar = 1;

用户定义的 :code:`someAsyncApiCall()` 包含了一些异步的标志，但实际上是一个同步的操作。当它被调用时，提供的回调 会在同一个事件循环阶段被调用 因为 :code:`someAsyncApiCall()` 实际上并不是异步操作。结果是，回调读取 :code:`bar` 的值，然后他并不在当前作用域，因为脚本还没有完成。

在回调中 加入 :code:`process.nextTick()` ，脚本仍然能被执行完，使得所有的变量 函数 等等 被优先初始化。这样做的另一个好处是，不允许事件循环 继续。 这对某些 需要警告错误的用户来说很有用。 这边是之前的例子 :code:`process.nextTick()` 。（因为需要完成当前的操作才会切换到 :code:`process.nextTick()` ）

.. code-block:: javascript 

    let bar;

    function someAsyncApiCall(callback) {
      process.nextTick(callback);
    }

    someAsyncApiCall(() => {
      console.log('bar', bar); // 1
    });

    bar = 1;


这是另一个例子：

.. code-block:: javascript 

    const server = net.createServer(() => {}).listen(8080);

    server.on('listening', () => {});

只有当一个端口被传递之后，才会立马绑定。 所以 :code:`listening` 能够被立马调用。 问题是， :code:`.on('listening')` 回调还没有被设定。

为了解决这个问题， :code:`listening` 会被放在 :code:`netxTick()` 中 以允许当前的代码运行完毕。这使得用户能够随意的设定事件处理函数。

:code:`process.nextTick()` 与 :code:`setImmediate()`
*******************************************************

用户可能会很疑虑，因为我们 有两个调用很相似，但他们的名字却很混乱：

- :code:`process.nextTick()` 会在相同的阶段 立马被执行
- :code:`setImmediate()` 会在事件循环的下一个阶段 或者 时钟 执行

实际上，这两个名字应当替换的，因为 :code:`process.nextTick()` 比起 :code:`setImmediate()` 会更快的执行，但这是以前的产物，不大可能被改变。 如果要做改变的话 可能会使得大部分的 NPM 包跟着修改。 每天都有更多的新模块被添加，这意味着 每过一天，更多可能的损坏会发生。 所以 即使他们令人困惑，名字本身不会改变。

我们推荐开发者使用 :code:`setImmediate()` ， 因为者更容易理解 (这使得代码的兼容性也更好，比方说浏览器 JS)。 

为什么我们使用 :code:`process.nextTick()`
*****************************************

主要有两个原因：

1. 使得用户能够处理错误，清理不需要的资源， 或者 在事件循环继续之前重新的 请求资源。
2. 有些时候 需要使得回调能够在 事件循环继续之前 在 调用栈上被展开。

一个例子 就是符合用户的预期。简单的例子：

.. code-block:: javascript 

    const server = net.createServer();
    server.on('connection', (conn) => { });

    server.listen(8080);
    server.on('listening', () => { });

:code:`listen()` 在事件循环的一开始就被执行了， 但是事件循环的回调被安排在了 :code:`setImmediate()` 中，除非一个 主机名 被传递，否则端口绑定会立马执行。当 事件循环继续时，最终会到达 轮询阶段，这就意味着，有非0的概率发生这样的情况：已经接收到了连接 但是 连接事件却仍然没有被触发。

另一个例子就是 运行一个构造函数，继承自 :code:`EventEmitter` ，他想在构造函数中调用事件。

.. code-block:: javascript

    const EventEmitter = require('events');
    const util = require('util');

    function MyEmitter() {
      EventEmitter.call(this);
      this.emit('event');
    }
    util.inherits(MyEmitter, EventEmitter);

    const myEmitter = new MyEmitter();
    myEmitter.on('event', () => {
      console.log('an event occurred!');
    });

你不能立马在构造函数中发出事件，因为脚本不会到达 用户指定回调事件的点。所以，在一个构造函数内部，你可以使用 :code:`process.nextTick()` 去设定一个回调函数，并且在构造函数结束时发出事件，这样就能取得期望的结果。

.. code-block:: javascript 

    const EventEmitter = require('events');
    const util = require('util');

    function MyEmitter() {
      EventEmitter.call(this);

      // use nextTick to emit the event once a handler is assigned
      process.nextTick(() => {
        this.emit('event');
      });
    }
    util.inherits(MyEmitter, EventEmitter);

    const myEmitter = new MyEmitter();
    myEmitter.on('event', () => {
      console.log('an event occurred!');
    });
