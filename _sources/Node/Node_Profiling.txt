Easy profiling for Node.js Applications
########################################


:date: 2019-02-05
:tags: Node
:category: Node
:slug: easy_profiling_for_node_js_applications
:author: Brian Shen
:summary: Easy profiling for Node.js Applications

.. _easy_profiling_for_node_js_applications.rst:

.. contents::

Intro
^^^^^

Reference: 

https://nodejs.org/en/docs/guides/simple-profiling/


有很多的第三方工具可以来分析 Node.js 应用程序，但是，在许多情况下，最简单的选项是使用 Node.js 自带的分析器。自带的分析器使用V8 内部的分析器，在程序执行期间定时的采样程序状态。然后记录这些采样的结果以及诸如jit 编译，呈现为以下一系列的刻度。

.. code-block:: bash 

    code-creation,LazyCompile,0,0x2d5000a337a0,396,"bp native array.js:1153:16",0x289f644df68,~
    code-creation,LazyCompile,0,0x2d5000a33940,716,"hasOwnProperty native v8natives.js:198:30",0x289f64438d0,~
    code-creation,LazyCompile,0,0x2d5000a33c20,284,"ToName native runtime.js:549:16",0x289f643bb28,~
    code-creation,Stub,2,0x2d5000a33d40,182,"DoubleToIStub"
    code-creation,Stub,2,0x2d5000a33e00,507,"NumberToStringStub"

在过去，你需要V8的源代码才能够中断刻度，幸运的是，在 Node.js 4.4.0 中引入了新的工具，使得不需要 V8的原始代码， 就能获得这些消耗信息。我们看看 内置的 分析器 如何帮助提供 应用程序的性能概览。

为了示例 刻度分析器，我们将会使用一个简单的 Express 应用程序。 我们的应用程序有两个处理函数，一个是为了添加用户到我们的系统：

.. code-block:: javascript 

    app.get('/newUser', (req, res) => {
      let username = req.query.username || '';
      const password = req.query.password || '';

      username = username.replace(/[!@#$%^&*]/g, '');

      if (!username || !password || users.username) {
        return res.sendStatus(400);
      }

      const salt = crypto.randomBytes(128).toString('base64');
      const hash = crypto.pbkdf2Sync(password, salt, 10000, 512, 'sha512');

      users[username] = { salt, hash };

      res.sendStatus(200);
    });

另一个是验证用户授权尝试：

.. code-block:: javascript

    app.get('/auth', (req, res) => {
      let username = req.query.username || '';
      const password = req.query.password || '';

      username = username.replace(/[!@#$%^&*]/g, '');

      if (!username || !password || !users[username]) {
        return res.sendStatus(400);
      }

      const { salt, hash } = users[username];
      const encryptHash = crypto.pbkdf2Sync(password, salt, 10000, 512, 'sha512');

      if (crypto.timingSafeEqual(hash, encryptHash)) {
        res.sendStatus(200);
      } else {
        res.sendStatus(401);
      }
    });

请注意，这些只是为了纯粹的示例，并不推荐在正式的Node.js应用程序中使用。通常来说，你不应该尝试设计自己的加密验证机制，采用现有的 被证明安全的解决方案更为合适。

现在 假设我们已经部署了应用，用户抱怨请求延迟太严重。我们可以很容易的使用内置分析器来运行这个程序：

.. code-block:: bash

    NODE_ENV=production node --prof app.js

然后使用 :code:`ab` (ApacheBench) 设置一些负载：

.. code-block:: bash

    curl -X GET "http://localhost:8080/newUser?username=matt&password=password"
    ab -k -c 20 -n 250 "http://localhost:8080/auth?username=matt&password=password"


ab 的输出如下：

.. code-block:: bash

    Concurrency Level:      20
    Time taken for tests:   46.932 seconds
    Complete requests:      250
    Failed requests:        0
    Keep-Alive requests:    250
    Total transferred:      50250 bytes
    HTML transferred:       500 bytes
    Requests per second:    5.33 [#/sec] (mean)
    Time per request:       3754.556 [ms] (mean)
    Time per request:       187.728 [ms] (mean, across all concurrent requests)
    Transfer rate:          1.05 [Kbytes/sec] received

    ...

    Percentage of the requests served within a certain time (ms)
      50%   3755
      66%   3804
      75%   3818
      80%   3825
      90%   3845
      95%   3858
      98%   3874
      99%   3875
    100%   4225 (longest request)

从这个输出中，我们可以看到我们每秒只能处理 5 个请求，每个请求的处理大约是 4 秒。 在现实程序中，我们在接收到用户请求后会做很多的工作，但是在这个示例中，时间可能被花费在了编译 正则表达式，产生随机数盐 以及 为用户的密码生成唯一的hash， 或者是Express 这个框架本身。

既然我们使用的 :code:`--prof` 选项来运行我们的脚本，一个刻度文件就会在程序运行的同目下产生。他会是这样的格式： :code:`isolate-0xnnnnnnnnnnnn-v8.log` （其中 :code:`n` 是数字）。

为了让这个文件有意义，我们需要使用 刻度处理器 以及 Node.js 可执行程序的协同工作。为了运行这个处理器， 使用 :code:`--prof-process` 标志位。

.. code-block:: bash 

    node --prof-process isolate-0xnnnnnnnnnnnn-v8.log > processed.txt

使用你最喜欢的文本编辑器打开这个文件，你会看到许多不同类型的信息。这个文件会被拆分成很多小节，每一小节都代表了一中语言。 首先，我们看下总体概况小节：

.. code-block:: bash 

    [Summary]:
      ticks  total  nonlib   name
        79    0.2%    0.2%  JavaScript
      36703   97.2%   99.2%  C++
          7    0.0%    0.0%  GC
        767    2.0%          Shared libraries
        215    0.6%          Unaccounted

这些信息向我们展示了 全部用例的 97%都集中在了 C++ 代码上，当我们查看其他小节时，我们就最应该留意 C++ 部分 （而不是 JavaScript ）。把这点牢记在心后，我们接下来找到 C++ 小节，包含了 C++ 程序使用 CPU 时间的信息：

.. code-block:: bash

    [C++]:
      ticks  total  nonlib   name
      19557   51.8%   52.9%  node::crypto::PBKDF2(v8::FunctionCallbackInfo<v8::Value> const&)
      4510   11.9%   12.2%  _sha1_block_data_order
      3165    8.4%    8.6%  _malloc_zone_malloc

我们可以看到占用CPU 高达 72.1% 的前 3 的入口。 从这个输出中，我们立马看到至少 51.8 的CPU 时间都被用在执行函数 PBKDF2 上了，这个函数负责从用户的密码产生hash。当然，我们暂时不能立马的观察出 后两名的入口对我们的程序有什么样的影响（或者为了这个示例假装不关心）。为了更好的理解这些函数的关系，我们接下来要查看 [Bottom up (heavy) profile] 这一小节，他提供了每个函数主调用的基本信息。检查这个章节，我们可以发现：

.. code-block:: bash 

    ticks parent  name
    19557   51.8%  node::crypto::PBKDF2(v8::FunctionCallbackInfo<v8::Value> const&)
    19557  100.0%    v8::internal::Builtins::~Builtins()
    19557  100.0%      LazyCompile: ~pbkdf2 crypto.js:557:16

    4510   11.9%  _sha1_block_data_order
    4510  100.0%    LazyCompile: *pbkdf2 crypto.js:557:16
    4510  100.0%      LazyCompile: *exports.pbkdf2Sync crypto.js:552:30

    3165    8.4%  _malloc_zone_malloc
    3161   99.9%    LazyCompile: *pbkdf2 crypto.js:557:16
    3161  100.0%      LazyCompile: *exports.pbkdf2Sync crypto.js:552:30

解析这一小节要比原始的刻度计数需要更多工作。在每一个 “call stack” 上，父列的百分数告诉你这个函数占用了上面一行函数的百分比。比方说，在 sha1block_data_order 上方中间的中间 “call stack” ，占用了示例的11.9%的运行时间，我们在前面已经得到了这个数据。当然，这边我们可以看到在 Node.js 加密模块内部他总是会被 pbkdf2 函数调用。我们能看到相似的现象，_malloc_zone_malloc 被 同样的 pbkdf2 递归调用了。所以，从上面的信息可以看出来，我们能够看出来，从用户的密码到hash 的计算占用的绝对不止 51.8% ，因为 sha1block_data_order 和 _malloc_zone_malloc 也是由 pbkdf2 函数调用的。

到这里，一切都清楚了，我们需要去优化 基于密码的hash生成器。 幸运的是，你知道异步编程的好处，并且意识到这边使用的是同步的生成方式，所以导致了事件循环的缓慢。这会阻止我们接受处理更多用用户请求。

为了修复这个问题，你可以做一个很小的修改，只需要使用 异步版本的 pbkdf2 就可以：

.. code-block:: javascript 

    app.get('/auth', (req, res) => {
      let username = req.query.username || '';
      const password = req.query.password || '';

      username = username.replace(/[!@#$%^&*]/g, '');

      if (!username || !password || !users[username]) {
        return res.sendStatus(400);
      }

      crypto.pbkdf2(password, users[username].salt, 10000, 512, (err, hash) => {
        if (users[username].hash.toString() === hash.toString()) {
          res.sendStatus(200);
        } else {
          res.sendStatus(401);
        }
      });
    });

重新运行一遍 ab 测试上面的程序，结果如下：

.. code-block:: bash 

    Concurrency Level:      20
    Time taken for tests:   12.846 seconds
    Complete requests:      250
    Failed requests:        0
    Keep-Alive requests:    250
    Total transferred:      50250 bytes
    HTML transferred:       500 bytes
    Requests per second:    19.46 [#/sec] (mean)
    Time per request:       1027.689 [ms] (mean)
    Time per request:       51.384 [ms] (mean, across all concurrent requests)
    Transfer rate:          3.82 [Kbytes/sec] received

    ...

    Percentage of the requests served within a certain time (ms)
      50%   1018
      66%   1035
      75%   1041
      80%   1043
      90%   1049
      95%   1063
      98%   1070
      99%   1071
    100%   1079 (longest request)

耶！你的应用程序现在每秒能处理 20 个请求了，大概是之前使用同步方法的 4 倍。另外，平均延迟从 4 秒 降到了 1 秒。

希望 从上面的性能分析示例中，你能够看到 V8 刻度处理器 能够如何帮助你更好的理解 Node.js 应用程序的效率。

