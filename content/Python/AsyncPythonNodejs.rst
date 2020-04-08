Async Syntax Comparison between Python and Nodejs
###################################################

:date: 2020-04-08
:tags: Python, Nodejs, Async
:category: Python
:slug: Async_Syntax_Comparison_between_Python_and_Nodejs
:author: Brian Shen
:summary: Async Syntax Comparison between Python and Nodejs

.. _Async_Syntax_Comparison_between_Python_and_Nodejs.rst:

.. contents::


Python asyncio Basic
^^^^^^^^^^^^^^^^^^^^

- run -> execute coroutine 
- create_task 
- sleep 
- gather -> Run all awaitable objects
- shield -> make awaitable objects cancallable 
- wait_for -> wait for an awaitable  within a timeout
- wait -> don't throw timeout exception, but will return the Future object

- run_coroutine_threadsafe -> Submit a coroutine to the given event loop
- current_tasks 
- all_tasks
- iscoroutine 
- iscoroutinefunction 


Python Sample 
^^^^^^^^^^^^^

.. code-block:: python

    #!/usr/bin/python3
    # -*- coding: UTF-8 -*-
    import asyncio
    import time

    #### Basic

    async def helloWorld():
    print('hello')
    # around 2 seconds
    await asyncio.sleep(2)
    print('world')

    # asyncio.run(helloWorld())

    async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

    #### Async Series

    async def async_series():
    print(f"started at {time.strftime('%X')}")

    await say_after(1, 'hello')
    await say_after(2, 'world')
    # around 3 seconds
    print(f"finished at {time.strftime('%X')}")

    # asyncio.run(async_series())


    #### Async Parallel

    async def async_parallel():
    print(f"started at {time.strftime('%X')}")

    task1 = asyncio.create_task( say_after(1, 'hello') )
    task2 = asyncio.create_task( say_after(2, 'world') )
    # around 2 seconds
    await task1
    await task2

    print(f"finished at {time.strftime('%X')}")

    # asyncio.run(async_parallel())

    async def async_parallel2():
    print(f"started at {time.strftime('%X')}")

    await asyncio.gather( say_after(1, 'hello'), 
        say_after(2, 'world') )
    # around 2 seconds

    print(f"finished at {time.strftime('%X')}")

    asyncio.run(async_parallel2())

Nodejs Sample 
^^^^^^^^^^^^^^


.. code-block:: javascript

    ///// Basic

    const helloWorld = async () => {
    console.log('hello')
    // around 2 seconds
    await ( new Promise(r => setTimeout(r, 2000)) );
    console.log('World')
    }

    // helloWorld().then( () => { console.log('Done') })

    const say_after =  async (delay, what) => {
    await ( new Promise(r => setTimeout(r, delay * 1000)) );
    console.log(what)
    }

    ///////  Async Series

    const async_series = async () => {
    console.log(`started at ${(new Date()).toString()}`)
    // around 3 seconds
    await say_after(1, 'hello')
    await say_after(2, 'world')

    console.log(`finished at ${(new Date()).toString()}`)
    }

    // async_series().then( () => { console.log('') })

    ////////// Async Parallel

    const async_parallel = async () => {
    console.log(`started at ${(new Date()).toString()}`)
    // around 2 seconds
    await Promise.all(
        [ say_after(1, 'hello'), say_after(2, 'world') ]
    );
    console.log(`finished at ${(new Date()).toString()}`)
    }

    async_parallel().then( () => { console.log('') })

Reference
*********

- https://docs.python.org/3/library/asyncio-task.html

