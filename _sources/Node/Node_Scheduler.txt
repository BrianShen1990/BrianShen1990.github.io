Node Task Queue Research / Node 任务队列学习
##############################################


:date: 2018-11-01
:tags: Node 
:category: Node
:slug: Node_Task_Queue_Research
:author: Brian Shen
:summary: Node Task Queue Research

.. _node_task_queue_research_rst:

.. contents::

Queue based on Node / 基于 Node 的队列
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Comparison / 对比
*****************

.. list-table:: 
   :widths: 28 18 18 18 18
   :header-rows: 1

   * - Feature  / 功能
     - Bull ☆3885
     - Kue  ☆8007 
     - Bee  ☆1141
     - Agenda ☆4637
   * - Backend / 后台支持
     - redis
     - redis
     - redis
     - mongo
   * - Priorities / 优先级支持
     - ✓
     - ✓
     - 
     - ✓
   * - Concurrency / 并行
     - ✓
     - ✓
     - ✓
     - ✓
   * - Delayed jobs / 延迟任务
     - ✓
     - ✓
     - 
     - ✓
   * - Global events / 全局事件
     - ✓
     - ✓
     - 
     - 
   * - Rate Limiter / 速度控制
     - ✓
     - 
     - 
     - 
   * - Pause/Resume / 停止/恢复
     - ✓
     - ✓
     - 
     - 
   * - Sandboxed worker / 沙箱工作节点
     - ✓
     - 
     - 
     - 
   * - Repeatable jobs / 重复任务
     - ✓
     - 
     - 
     - ✓
   * - Atomic ops / 原子性操作
     - ✓
     - 
     - ✓
     - 
   * - Persistence / 持久性
     - ✓
     - ✓
     - ✓
     - ✓
   * - UI  
     - ✓
     - ✓
     - 
     - ✓
   * - REST API
     - 
     - 
     - 
     - ✓
   * - Optimized for / 优化
     - Jobs / Messages
     - Jobs
     - Messages
     - Jobs
				
My opinion / 个人观点
*********************

After I've reviewed their documents, I listed my own opinion.

在查看过介绍 和 使用文档后，有一些自己的心得:

.. list-table:: 
   :widths: 20 80
   :header-rows: 1

   * - Products  / 产品
     - Descriptions / 描述
   * - Bull
     - | Job and Queue:  
       | One queue can contain one kind of job. 
       | 每一个队列包含一种任务
       | Every queue has its own Redis connection except for more configuration. 
       | 每个队列需要一个Redis连接， 需要额外的配置才可以共享
       | 
       | Advantages:  / 好处
       | Quicker and full functional.
       | 队列任务消除 相对较快，功能全面
   * - Kue
     - | Job and Queue:
       | One queue can contain multiple kinds of jobs. 
       | 一个队列 包含多种类型的任务
       | So one queue is enough and only 1 redis connection is needed. 
       | 
       | Speed: But the speed of time-consuming is not that fast from the benchmark test from Bee.
       | 队列任务消除缓慢， 而且维护较少
   * - Bee
     - | Job and Queue:
       | One queue can contain multiple kinds of jobs.
       | 每一个队列包含一种任务
       | Every queue has its own Redis connection.
       |
       | Quicker and lighter. / 更快 也更轻量级 
   * - Agenda
     - | Advantages:
       | Designed for Scheduler and Repeat Jobs.
       | 更偏向于 定期/周期任务 


Recommendation: :code:`Bull` .

推荐使用 :code:`Bull` .


Other Queues / 其他可选的队列
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

However, queues based on Node can satisfy us if the volume is OK. 

But if the number soars, we should seek help for other real messages queues.

如果我们的任务量比较小，整个架构也不复杂的话，基于 Node 的队列基本可以满足要求。

但是如果任务量大，构架复杂， 我们需要依赖于一些专业的标准化的队列服务。


RabbitMQ
*********

Implementation of AMQP (Advanced Message Queuing Protocol), 

an open standard application layer protocol for message-oriented middleware. 

是 AMQP 的一种实现。

- Standard Protocol / 标准协议
- No Language Limitation / 不是基于某种语言


Saas -  AWS Simple Queue Service / Saas AWS 简单队列服务
**********************************************************

Reference: https://aws.amazon.com/sqs/

The fee of first 1 million messages per mon is free. 
每个月首个一百万条消息是免费的...

- Standard Queues / 标准队列
    - Unlimited Throughput
    - At-Least-Once Delivery
    - Best-Effort Ordering
- FIFO Queues / 先进先出队列 
    - High Throughput
    - Exactly-Once Processing
    - First-In-First-Out Delivery


Saas - Azure Service Bus
***************************

Reference: https://docs.microsoft.com/en-us/azure/service-bus-messaging/service-bus-queues-topics-subscriptions

The fee of first 1000 brokered connections (744,000 messages) /per mon is free . (https://docs.microsoft.com/en-us/azure/service-bus-messaging/service-bus-pricing-billing).

每个月首个 74 万消息是免费的。

- Queues: One to one
- Topics and subscriptions: One to many


Queues I have encountered  / 我遇到的队列
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In TM, I used to be a member of CAS, we use two kind types of queues:

在 TM CAS 团队(Saas 产品), 我们使用了两种类型的队列:

- Azure Message Queue: Quite expensive 
    Azure 的Service Bus，Hook Email 之后会将Email事件存放在Queue 中，顺序处理， 也可以作为监控指标
- Queue designed by ourselves: / 自行设计的 Queue
    MS SQL backed, and every task are record. And micro services will get and handle them periodically. 

    基于 MS SQL，周期性任务会存在在 MSSQL 中 每一步会去更新状态， 直到最终完成。 
- Celery + RabbitMQ + Python
   Python Web Service 有一些长期的异步任务需要实现，使用的是 Celery (http://www.celeryproject.org/) , 基于 RabbitMQ。

.. disqus::
    :disqus_identifier: _node_task_queue_research_rst