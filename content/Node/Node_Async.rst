Node Async - Make your code more readable 
##########################################


:date: 2019-08-19
:tags: Node, async, promise
:category: Web
:slug: Node_Async_Make_your_code_more_readable 
:author: Brian Shen
:summary: Node Async - Make your code more readable 

.. _Node_Async.rst:

.. contents::


Intro
^^^^^^

I love promises because promises make node magic and advanced and the most important, promise will keep me aware that: you are writing asynchronous code. Sometimes, beginners and even professionals forget this point and then they will spend miserable amount of time debugging.

However, we write code to make works done and to make others understood, especially when others are responsible for maintenance.

Actually, for most people, JavaScript is quite easy to understand without promises. So why don't make it easy. Use less promise and use more async.

How to use promises in async
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Just use :code:`await` for a promise in an :code:`async` function. And it will wait for the promise to finish until it goes on. 

.. code-block:: javascript 

  const promisesFunc  = (output) => {
    return new Promise(resolve => {
      setTimeout( () => {
        resolve(`resolved ${output}`);
      }, 2000);
    });
  }

  const asyncCall = async () => {
    const result = await promisesFunc("call from async");
    console.log(result);
    // expected output: 'resolved'
  }
  console.log("=== begin")
  asyncCall();
  console.log("=== end")

  // === begin
  // === end
  // resolved call from async

How to handle errors in async
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ordinary :code:`try..catch..` .

.. code-block:: javascript

  const promisesErrorFunc = (output) => {
    return new Promise( (_, reject) => {
      setTimeout( () => {
        reject(`reject ${output}`);
      }, 2000);
    });
  }

  const asyncCall = async () => {
    try {
      const result = await promisesErrorFunc("call from async");
      console.log(result);
    } catch (err) {
      console.log(err);
    }
  }
  console.log("=== begin")
  asyncCall();
  console.log("=== end")
  // === begin
  // === end
  // reject call from async

However, it will only handle traditional promise rejects. If we don't handle properly within promise, then the outside :code:`try..catch..` also cannot do anything.

.. code-block:: javascript

  const promisesErrorFunc = (output) => {
    return new Promise( (_, reject) => {
      setTimeout( () => {
        notExistVar.attrSome = 9;
        reject(`reject ${output}`);
      }, 2000);
    });
  }

  const asyncCall = async () => {
    try {
      const result = await promisesErrorFunc("call from async");
      console.log(result);
    } catch (err) {
      console.log("falls async error");
      console.log(err);
    }
  }
  console.log("=== begin")
  asyncCall();
  console.log("=== end")

  // === begin
  // === end
  // /Users/houweishen/Code/Brian/tset/Node/async/test.js:11
  //       notExistVar.attrSome = 9;
  //       ^
  // 
  // ReferenceError: notExistVar is not defined
  //     at Timeout._onTimeout (/Users/houweishen/Code/Brian/tset/Node/async/test.js:11:7)
  //   at listOnTimeout (internal/timers.js:531:17)
  //   at processTimers (internal/timers.js:475:7)

And, to avoid such kind of crash: 

.. code-block:: javascript

  const promisesErrorSafeFunc = (output) => {
    return new Promise( (_, reject) => {
      setTimeout( () => {
        try {
          notExistVar.attrSome = 9;
          reject(`reject ${output}`);
        } catch(error) {
          console.log("falls inside here");
          reject(error);
        }
      }, 2000);
    });
  }

  const asyncCall = async () => {
    try {
      const result = await promisesErrorSafeFunc("call from async");
      console.log(result);
    } catch (err) {
      console.log("falls async error");
    }
  }
  console.log("=== begin")
  asyncCall();
  console.log("=== end")

  // === begin
  // === end
  // falls inside here
  // falls async error


Async, series
^^^^^^^^^^^^^

Async, as its own name, make everything seems async in syntax.

.. code-block:: javascript

  const promisesFunc  = (output) => {
    return new Promise(resolve => {
      setTimeout( () => {
        resolve(`resolved ${output}`);
      }, 1000);
    });
  }
  const asyncCallSeries = async () => {
    const result1 = await promisesFunc("call from async 01");
    console.log(result1);
    const result2 = await promisesFunc("call from async 02");
    console.log(result2);
  }
  console.log("=== begin")
  asyncCallSeries();
  console.log("=== end")

  // === begin
  // === end
  // resolved call from async 01
  // resolved call from async 02


Make async synchronous
^^^^^^^^^^^^^^^^^^^^^^^

We have to rely on the power of promises.

.. code-block:: bash 

  const promisesFunc  = (output) => {
    return new Promise(resolve => {
      setTimeout( () => {
        resolve(`resolved ${output}`);
      }, 1000);
    });
  }

  const asyncCallAsync = async () => {
    const result = await Promise.all([promisesFunc("01"), promisesFunc("02")]);
    console.log(result);
  }

  console.log("=== begin")
  asyncCallAsync();
  console.log("=== end")

  // === begin
  // === end
  // [ 'resolved 01', 'resolved 02' ]

Async in iteration 
^^^^^^^^^^^^^^^^^^^

async cannot be resided inside :code:`map` , :code:`forEach` 
****************************************************************

.. code-block:: javascript

  const promisesFunc  = (output) => {
    return new Promise(resolve => {
      setTimeout( () => {
        resolve(`resolved ${output}`);
      }, 1000);
    });
  }
  const asyncMapFunc = async () => {
    [1,2,3].map( (_, index) => {
      const res = await promisesFunc(index);
      console.log(res);
    });
  }
  console.log("=== begin")
  asyncMapFunc();
  console.log("=== end")
  // /Users/houweishen/Code/Brian/tset/Node/async/test.js:53
  //   const res = await promisesFunc(index);
  //               ^^^^^
  // 
  // SyntaxError: await is only valid in async function
  
  

async in for each 
*****************


.. code-block:: javascript

  const promisesFunc  = (output) => {
    return new Promise(resolve => {
      setTimeout( () => {
        resolve(`resolved ${output}`);
      }, 1000);
    });
  }
  const asyncMapFunc = async () => {
    [1,2,3].map( async(_, index) => {
      const res = await promisesFunc(`MAP ${index}`);
      console.log(res);
    });
  }
  const asyncForEachFunc = async () => {
    [1,2,3].forEach( async(_, index) => {
      const res = await promisesFunc(`ForEach ${index}`);
      console.log(res);
    });
  }
  const asyncForInFunc = async () => {
    for (let index in [1,2,3] ) {
      const res = await promisesFunc(`ForIn ${index}`);
      console.log(res);
    }
  }
  const asyncForOfFunc = async () => {
    for (let item of [1,2,3] ) {
      const res = await promisesFunc(`ForOf ${item}`);
      console.log(res);
    }
  }

  console.log("=== begin")
  asyncForInFunc();
  asyncForOfFunc();
  asyncMapFunc();
  asyncForEachFunc();
  console.log("=== end")

  // === begin
  // === end
  // resolved ForIn 0
  // resolved ForOf 1
  // resolved MAP 0
  // resolved MAP 1
  // resolved MAP 2
  // resolved ForEach 0
  // resolved ForEach 1
  // resolved ForEach 2
  // resolved ForIn 1
  // resolved ForOf 2
  // resolved ForIn 2
  // resolved ForOf 3

So async iterations in :code:`map` , :code:`forEach` are async, and :code:`for..in..` , :code:`for..of..` are sync.

Reference
^^^^^^^^^^^

- https://ithelp.ithome.com.tw/articles/10201420?sc=iThelpR
- http://objcer.com/2017/10/12/async-await-with-forEach/