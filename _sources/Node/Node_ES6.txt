ES6 Reference
###############


:date: 2018-12-21
:tags: Node
:category: Node
:slug: ES6_Reference
:author: Brian Shen
:summary: ES6 Reference 

.. _es6_reference_rst:

.. contents::

let & const 
^^^^^^^^^^^^

Just use them.

destructuring
^^^^^^^^^^^^^^

Usage
******

- Exchange value

  .. code-block:: bash

      let x = 1;
      let y = 2;
      [x, y] = [y, x];

- Return many values

  .. code-block:: bash 

      function example() {
        return {
          foo: 1,
          bar: 2
        };
      }
      let { foo, bar } = example();

- Function definition

  .. code-block:: bash 

      function f([x, y, z]) { ... }
      f([1, 2, 3]);

      function f({x, y, z}) { ... }
      f({z: 3, y: 2, x: 1});

- JSON extraction

  .. code-block:: bash 

      let jsonData = {
        id: 42,
        status: "OK",
        data: [867, 5309]
      };
      let { id, status, data: number } = jsonData;

- Default function parameter 

  .. code-block:: bash 

      jQuery.ajax = function (url, {
        async = true,
        beforeSend = function () {},
        cache = true,
        complete = function () {},
        crossDomain = false,
        global = true,
        // ... more config
      } = {}) {
        // ... do stuff
      };

- Map iteration

  .. code-block:: bash 

      for (let [key, value] of map) {
        console.log(key + " is " + value);
      }

- Module import 

  .. code-block:: bash

      const { SourceMapConsumer, SourceNode } = require("source-map");

String
^^^^^^^

Unicode
*******

.. code-block:: bash 

    '\z' === 'z'  // true
    '\172' === 'z' // true
    '\x7A' === 'z' // true
    '\u007A' === 'z' // true // less than FFFF
    '\u{7A}' === 'z' // true  // greater than FFFF (4 byte)

codePointAt 
************

Handle characters taken more than 4 bytes.

.. code-block:: bash 

    var s = "𠮷a";

    s.length // 2
    s.charAt(0) // ''
    s.charAt(1) // ''
    s.charCodeAt(0) // 55362
    s.charCodeAt(1) // 57271
    s.codePointAt(0) // 134071
    s.codePointAt(1) // 57271
    s.codePointAt(2) // 97

fromCodePoint
**************

Only handle characters taken more than 4 bytes.

.. code-block:: bash

  String.fromCodePoint(0x20BB7)
  // "𠮷"

iteration 
**************

:code:`for...of` syntax can handler all kinds of characters.

.. code-block:: bash

    let text = String.fromCodePoint(0x20BB7);
    for (let i = 0; i < text.length; i++) {
      console.log(text[i]);
    }
    // " "
    // " "

    for (let i of text) {
      console.log(i);
    }
    // "𠮷"

normalize
**********

Handle European Characters.

newAPIs
********

.. code-block:: bash 

    includes()
    startsWith()
    endsWith()
    endsWith()
    padStart()
    padEnd()

String Template
*****************

.. code-block:: bash 

    let str = `There are <b>${basket.count}</b> items`

Regex
^^^^^^

Unicode support :code:`u`
***************************

.. code-block:: bash 

    var s = '𠮷';

    /^.$/.test(s) // false
    /^.$/u.test(s) // true

    /\u{61}/.test('a') // false
    /\u{61}/u.test('a') // true
    /\u{20BB7}/u.test('𠮷') // true

    /a{2}/.test('aa') // true
    /a{2}/u.test('aa') // true
    /𠮷{2}/.test('𠮷𠮷') // false
    /𠮷{2}/u.test('𠮷𠮷') // true

Stick :code:`y`
****************

:code:`y` begin after all match while :code:`g` begin at next character.

.. code-block:: bash 

    var s = 'aaa_aa_a';
    var r1 = /a+/g;
    var r2 = /a+/y;

    r1.exec(s) // ["aaa"]
    r2.exec(s) // ["aaa"]

    r1.exec(s) // ["aa"]
    r2.exec(s) // null

dotAll :code:`s` 
*****************

We can support all characters. dot only represents normal characters.

.. code-block:: bash 

    /foo.bar/.test('foo\nbar')
    // false
    /foo.bar/s.test('foo\nbar') // true

Number
^^^^^^^^^

APIS 
*****

- isFinite, isNaN

  .. code-block:: bash 

      Number.isFinite(15); // true
      Number.isFinite(0.8); // true
      Number.isFinite(NaN); // false
      Number.isFinite(Infinity); // false
      Number.isFinite(-Infinity); // false
      Number.isFinite('foo'); // false
      Number.isFinite('15'); // false
      Number.isFinite(true); // false

      Number.isNaN(NaN) // true
      Number.isNaN(15) // false
      Number.isNaN('15') // false
      Number.isNaN(true) // false
      Number.isNaN(9/NaN) // true
      Number.isNaN('true' / 0) // true
      Number.isNaN('true' / 'true') // true

- parseInt
- parseFloat
- isInteger
- isSafeInteger ( -2^53 ~ 2^53 )

Function 
^^^^^^^^^

Rest parameters
****************

:code:`...varaiable` to get all rest parameters. Array.

.. code-block:: bash 

    function add(...values) {
      let sum = 0;
      for (var val of values) {
        sum += val;
      }
      return sum;
    }
    add(2, 5, 3) // 10

strict mode 
************

Under strict mode, functions won't include :code:`func.arguments` and :code:`func.caller` .

If we want to use strict mode, then the function itself cannot include 
- default value 
- deconstructing 

Error: 

.. code-block:: bash 

    function doSomething(a, b = a) {
      'use strict';
      // code
    }

    const doSomething = function ({a, b}) {
      'use strict';
      // code
    };

    const doSomething = (...a) => {
      'use strict';
      // code
    };

    const obj = {
      doSomething({a, b}) {
        'use strict';
        // code
      }
    };

How we can avoid this: 

.. code-block:: bash 

    # 1
    'use strict';
    function doSomething(a, b = a) {
      // code
    }

    # 2 
    const doSomething = (function () {
      'use strict';
      return function(value = 42) {
        return value;
      };
    }());

Array Function
****************

Watch:
- there is no :code:`this` in function, :code:`this` is the outside :code:`this` .
- cannot use as a constructor 
- cannot use arguments object
- cannot use yield

Array 
^^^^^^

spread operator
****************

.. code-block:: bash 

    console.log(...[1, 2, 3])
    // 1 2 3

Usage: 

- clone 

  .. code-block:: bash 

      const a1 = [1, 2];
      const a2 = [...a1];

- combine

  .. code-block:: bash 

      const arr1 = ['a', 'b'];
      const arr2 = ['c'];
      [...arr1, ...arr2]

- String length

  .. code-block:: bash 

      'x\uD83D\uDE80y'.length // 4
      [...'x\uD83D\uDE80y'].length // 3

- generator

  .. code-block:: bash 

      const go = function*(){
        yield 1;
        yield 2;
        yield 3;
      };

      [...go()] // [1, 2, 3]

APIs 

- Array.from 

  .. code-block:: bash 

      let arrayLike = {
          '0': 'a',
          '1': 'b',
          '2': 'c',
          length: 3
      };
      let arr2 = Array.from(arrayLike); // ['a', 'b', 'c']

- Array.Of 

  Array constructor exists some misunderstanding.

  .. code-block:: bash 

      Array.of(3, 11, 8) // [3,11,8]
      Array.of(3) // [3]
      Array.of(3).length // 1

      Array() // []
      Array(3) // [, , ,]  
      Array(3, 11, 8) // [3, 11, 8]

- find, findIndex
- fill 
- entries()，keys() and values()

  .. code-block:: bash 

      for (let index of ['a', 'b'].keys()) {
        console.log(index);
      }
      // 0
      // 1

      for (let elem of ['a', 'b'].values()) {
        console.log(elem);
      }
      // 'a'
      // 'b'

      for (let [index, elem] of ['a', 'b'].entries()) {
        console.log(index, elem);
      }
      // 0 "a"
      // 1 "b"

      let letter = ['a', 'b', 'c'];
      let entries = letter.entries();
      console.log(entries.next().value); // [0, 'a']
      console.log(entries.next().value); // [1, 'b']
      console.log(entries.next().value); // [2, 'c']

- includes 
- flat, flatMap

  .. code-block:: bash 

      [1, 2, [3, 4]].flat()
      // [1, 2, 3, 4]


      [2, 3, 4].flatMap((x) => [x, x * 2])
      // [2, 4, 3, 6, 4, 8]


Object 
^^^^^^^

syntax
*******

.. code-block:: bash 

    const foo = 'bar';
    const baz = {foo};
    baz // {foo: "bar"}

    let lastWord = 'last word';
    const a = {
      'first word': 'hello',
      [lastWord]: 'world'
    };
    a['first word'] // "hello"
    a[lastWord] // "world"
    a['last word'] // "world"

    !!!! Don't use object as a key.
    const keyA = {a: 1};
    const keyB = {b: 2};
    const myObject = {
      [keyA]: 'valueA',
      [keyB]: 'valueB'
    };
    myObject // Object {[object Object]: "valueB"}

ATTR
*****

- :code:`name`

  .. code-block:: bash 

      const person = {
        sayName() {
          console.log('hello!');
        },
      };
      person.sayName.name   // "sayName"

- :code:`super` (Only in function of an object)

  Point to the prototype.

  .. code-block:: bash 

      const proto = {
        foo: 'hello'
      };

      const obj = {
        foo: 'world',
        find() {
          return super.foo;
        }
      };

      Object.setPrototypeOf(obj, proto);
      obj.find() // "hello"

Operator
**********

.. code-block:: bash 

    let z = { a: 3, b: 4 };
    let n = { ...z };
    n // { a: 3, b: 4 }

    let foo = { ...['a', 'b', 'c'] };
    foo
    // {0: "a", 1: "b", 2: "c"}

    let aClone = { ...a };
    // Same as 
    let aClone = Object.assign({}, a);

APIs 
*****

- :code:`Object.is`  same as :code:`===` .
- :code:`Object.assign` 
  - Shallow Copy
  - Array handle as object

    .. code-block:: bash 

        Object.assign([1, 2, 3], [4, 5])
        // [4, 5, 3]

  - get value and then overwrite

- :code:`Object.getOwnPropertyDescriptor`

  set, get special functions.

  .. code-block:: bash 

      const source = {
        set foo(value) {
          console.log(value);
        }
      };

      const target2 = {};
      Object.defineProperties(target2, Object.getOwnPropertyDescriptors(source));
      Object.getOwnPropertyDescriptor(target2, 'foo')
      // { get: undefined,
      //   set: [Function: set foo],
      //   enumerable: true,
      //   configurable: true }

- :code:`__proto__ ，Object.setPrototypeOf()，Object.getPrototypeOf()`
- :code:`Object.keys()，Object.values()，Object.entries()`
- :code:`Object.fromEntries()` adverse of :code:`entries` , from Map to Object.


Symbol
^^^^^^^

Usage
******

Object has various attributes which are defined in string. So it is very easy to overwrite them.
Symbol  is unique and is the 7th type of js.


.. code-block:: bash

    let s = Symbol();
    typeof s
    // "symbol"

    let s1 = Symbol('foo');
    let s2 = Symbol('bar');
    s1 // Symbol(foo)
    s2 // Symbol(bar)
    s1.toString() // "Symbol(foo)"
    s2.toString() // "Symbol(bar)"

    let s1 = Symbol();
    let s2 = Symbol();
    s1 === s2 // false
    let s1 = Symbol('foo');
    let s2 = Symbol('foo');
    s1 === s2 // false

Symbol can turn to strings only in explicit way. 

Iteration
**********
When we use Symbol as an attribute, then , it won't appear in iterations. 
- :code:`for...in`
- :code:`for...of`
- :code:`Object.keys()`
- :code:`Object.getOwnPropertyNames()`
- :code:`JSON.stringify()`

We can get these attributes with :code:`Object.getOwnPropertySymbols` .

APIs
********

- Symbol.for (create or get)

  .. code-block:: bash

      let s1 = Symbol.for('foo');
      let s2 = Symbol.for('foo');

      s1 === s2 // true

- Symbol.keyFor 

  .. code-block:: bash 

      let s1 = Symbol.for("foo");
      Symbol.keyFor(s1) // "foo"

      let s2 = Symbol("foo");
      Symbol.keyFor(s2) // undefined

Set and  Map
^^^^^^^^^^^^^

Set 
****

.. code-block:: bash 

    const s = new Set();

    [2, 3, 5, 4, 5, 2, 2].forEach(x => s.add(x));
    for (let i of s) {
      console.log(i);
    }
    // 2 3 5 4

    const set = new Set([1, 2, 3, 4, 4]);
    [...set]
    // [1, 2, 3, 4]

- size
- add()
- delete()
- has()
- clear()
- keys()
- values()
- entries()
- forEach()

Map
*****

Hash Key Value.
But, we can add everything as a key.

.. code-block:: bash 

    const map = new Map([
      ['name', '张三'],
      ['title', 'Author']
    ]);
    map.size // 2
    map.has('name') // true
    map.get('name') // "张三"
    map.has('title') // true
    map.get('title') // "Author"

    const items = [
      ['name', '张三'],
      ['title', 'Author']
    ];
    const map = new Map();
    items.forEach(
      ([key, value]) => map.set(key, value)
    );

- size
- add()
- delete()
- has()
- clear()
- keys()
- values()
- entries()
- forEach()

Proxy 
^^^^^^

meta programming, which can change language.

.. code-block:: bash 

    var obj = new Proxy({}, {
      get: function (target, key, receiver) {
        console.log(`getting ${key}!`);
        return Reflect.get(target, key, receiver);
      },
      set: function (target, key, value, receiver) {
        console.log(`setting ${key}!`);
        return Reflect.set(target, key, value, receiver);
      }
    });
    obj.count = 1
    //  setting count!
    ++obj.count
    //  getting count!
    //  setting count!
    //  2

Proxy Actions Supoorted
*************************


- get(target, propKey, receiver)
- set(target, propKey, value, receiver) 
- has(target, propKey)
- deleteProperty(target, propKey)
- ownKeys(target)
- getOwnPropertyDescriptor(target, propKey)
- defineProperty(target, propKey, propDesc)
- preventExtensions(target)
- getPrototypeOf(target)
- isExtensible(target)
- setPrototypeOf(target, proto)
- apply(target, object, args)
- construct(target, args)


Proxy.revocable
****************

Stop proxy.

.. code-block:: bash 

    let target = {};
    let handler = {};

    let {proxy, revoke} = Proxy.revocable(target, handler);

    proxy.foo = 123;
    proxy.foo // 123

    revoke();
    proxy.foo // TypeError: Revoked

This
*****

This will point to Proxy itself.

.. code-block:: bash

    const target = {
      m: function () {
        console.log(this === proxy);
      }
    };
    const handler = {};

    const proxy = new Proxy(target, handler);

    target.m() // false
    proxy.m()  // true

Reflect 
^^^^^^^^^

Why:
- Move some Object internal functions to Reflect 
- Refine some APIs that Object provides
- Make all actions become functions (name in object => has() )
- Reflect and Proxy Combination

  .. code-block:: bash 

      Proxy(target, {
        set: function(target, name, value, receiver) {
          var success = Reflect.set(target,name, value, receiver);
          if (success) {
            console.log('property ' + name + ' on ' + target + ' set to ' + value);
          }
          return success;
        }
      });

Methods:

- Reflect.apply(target, thisArg, args)
- Reflect.construct(target, args)
- Reflect.get(target, name, receiver)
- Reflect.set(target, name, value, receiver)
- Reflect.defineProperty(target, name, desc)
- Reflect.deleteProperty(target, name)
- Reflect.has(target, name)
- Reflect.ownKeys(target)
- Reflect.isExtensible(target)
- Reflect.preventExtensions(target)
- Reflect.getOwnPropertyDescriptor(target, name)
- Reflect.getPrototypeOf(target)
- Reflect.setPrototypeOf(target, prototype)


Promises
^^^^^^^^^

3 States:
- pending
- fulfilled (resolved)
- rejected 

.. code-block:: bash 

    const promise = new Promise(function(resolve, reject) {
      // ... some code

      if (success){
        resolve(value);
      } else {
        reject(error);
      }
    });

Once created, it will run.
Resolve and Reject cannot terminate Promise. So, always add return.

APIs 
******

- then 

  .. code-block:: bash 

      getJSON("/post/1.json").then(
        post => getJSON(post.commentURL)
      ).then(
        comments => console.log("resolved: ", comments),
        err => console.log("rejected: ", err)
      );

- catch 

  Alias of :code:`.then(null, rejection)` .

  then can append after catch as catch itself will return a promise.

- finally

  .. code-block:: bash 

      promise
      .then(result => {···})
      .catch(error => {···})
      .finally(() => {···});

- all 

  .. code-block:: bash 

      const promises = [2, 3, 5, 7, 11, 13].map(function (id) {
        return getJSON('/post/' + id + ".json");
      });

      Promise.all(promises).then(function (posts) {
        // ...
      }).catch(function(reason){
        // ...
      });

- race 

  Only one promise needs to be finished.

  .. code-block:: bash 

      const p = Promise.race([
        fetch('/resource-that-may-take-a-while'),
        new Promise(function (resolve, reject) {
          setTimeout(() => reject(new Error('request timeout')), 5000)
        })
      ]);

      p
      .then(console.log)
      .catch(console.error);

- resolve 

  Turn an object to a Promise object 

  .. code-block:: bash 

      const jsPromise = Promise.resolve($.ajax('/whatever.json'));

- reject 

  .. code-block:: bash 

      const p = Promise.reject('wrong');
      // same 
      const p = new Promise((resolve, reject) => reject('wrong'))

      p.then(null, function (s) {
        console.log(s)
      });

Iterator 
^^^^^^^^^

If a data structure has :code:`Symbol.iterator` attribute, then it is iterable. 
And we can use :code:`for...of` to iterate it.

.. code-block:: bash

    const obj = {
      [Symbol.iterator] : function () {
        return {
          next: function () {
            return {
              value: 1,
              done: true
            };
          }
        };
      }
    };


Native iterable objects:

- Array
- Map
- Set
- String
- TypedArray
- arguments object in function
- NodeList

Sample:

.. code-block:: bash

    let arr = ['a', 'b', 'c'];
    let iter = arr[Symbol.iterator]();

    iter.next() // { value: 'a', done: false }
    iter.next() // { value: 'b', done: false }
    iter.next() // { value: 'c', done: false }
    iter.next() // { value: undefined, done: true }


When we use it?
- destruct and assign

  .. code-block:: bash 

      let set = new Set().add('a').add('b').add('c');

      let [x,y] = set;
      // x='a'; y='b'

      let [first, ...rest] = set;
      // first='a'; rest=['b','c'];

- expand operator :code:`...`
- :code:`yield*`

  .. code-block:: bash 

      let generator = function* () {
        yield 1;
        yield* [2,3,4];
        yield 5;
      };

      var iterator = generator();

      iterator.next() // { value: 1, done: false }
      iterator.next() // { value: 2, done: false }
      iterator.next() // { value: 3, done: false }
      iterator.next() // { value: 4, done: false }
      iterator.next() // { value: 5, done: false }
      iterator.next() // { value: undefined, done: true }

Generator
^^^^^^^^^

State Machine.
- A :code:`*` between :code:`function` and name.
- use :code:`yeild` .

When we call generator, it doesn't run. Instead, it return  a pointer to internal content.

We should call :code:`next` to get next state.

.. code-block:: bash

    function* helloWorldGenerator() {
      yield 'hello';
      yield 'world';
      return 'ending';
    }
    var hw = helloWorldGenerator();
    
    hw.next()
    // { value: 'hello', done: false }
    hw.next()
    // { value: 'world', done: false }
    hw.next()
    // { value: 'ending', done: true }
    hw.next()
    // { value: undefined, done: true }

Legal syntax:

.. code-block:: bash

    function * foo(x, y) { ··· }
    function *foo(x, y) { ··· }
    function* foo(x, y) { ··· }
    function*foo(x, y) { ··· }


A parameter can be added to next function. And this value will be regarded as the previous yeild value.


.. code-block:: bash

    function* f() {
      for(var i = 0; true; i++) {
        var reset = yield i;
        if(reset) { i = -1; }
      }
    }
    var g = f();
    g.next() // { value: 0, done: false }
    g.next() // { value: 1, done: false }
    g.next(true) // { value: 0, done: false }


Complex:

.. code-block:: bash 

    function* foo(x) {
      var y = 2 * (yield (x + 1));
      var z = yield (y / 3);
      return (x + y + z);
    }

    var a = foo(5);
    a.next() // Object{value:6, done:false}
    a.next() // Object{value:NaN, done:false}
    a.next() // Object{value:NaN, done:true}

    var b = foo(5);
    b.next() // { value:6, done:false } x = 5
    b.next(12) // { value:8, done:false } y = 2*12, yield = 24/3 = 8
    b.next(13) // { value:42, done:true } z = 13, so 5+ 24 + 13 = 42


.. code-block:: bash 

    function* numbers () {
      yield 1
      yield 2
      return 3
      yield 4
    }

    [...numbers()] // [1, 2]

    Array.from(numbers()) // [1, 2]

    let [x, y] = numbers();
    x // 1
    y // 2

    for (let n of numbers()) {
      console.log(n)
    }
    // 1
    // 2

- throw

.. code-block:: bash 

    var g = function* () {
      try {
        yield;
      } catch (e) {
        console.log('Internal', e);
      }
    };

    var i = g();
    i.next();

    try {
      i.throw('a');
      i.throw('b');
    } catch (e) {
      console.log('External', e);
    }
    // Internal a
    // External b

- return

terminate iteration.

.. code-block:: bash 

    function* gen() {
      yield 1;
      yield 2;
      yield 3;
    }

    var g = gen();

    g.next()        // { value: 1, done: false }
    g.return('foo') // { value: "foo", done: true }
    g.next()        // { value: undefined, done: true }

- :code:`yield *` : call another generator

.. code-block:: bash

    function* bar() {
      yield 'x';
      yield* foo();
      yield 'y';
    }

- generator function as an object attribution

.. code-block:: bash

  let obj = {
    * myGeneratorMethod() {
      ···
    }
  };
  let obj = {
    myGeneratorMethod: function* () {
      // ···
    }
  };


Class 
^^^^^^

.. code-block:: bash 

    # Old
    function Point(x, y) {
      this.x = x;
      this.y = y;
    }
    Point.prototype.toString = function () {
      return '(' + this.x + ', ' + this.y + ')';
    };
    var p = new Point(1, 2);

    # New
    class Point {
      constructor(x, y) {
        this.x = x;
        this.y = y;
      }
      toString() {
        return '(' + this.x + ', ' + this.y + ')';
      }
    }

class specials
***************

- constructor 
- getter and setter 

  .. code-block:: bash 

      class MyClass {
        constructor() {
          // ...
        }
        get prop() {
          return 'getter';
        }
        set prop(value) {
          console.log('setter: '+value);
        }
      }
      let inst = new MyClass();
      inst.prop = 123;
      // setter: 123
      inst.prop
      // 'getter'

- Another form 

  .. code-block:: bash 

      const MyClass = class Me {
        getClassName() {
          return Me.name;
        }
      };
      let inst = new MyClass();
      inst.getClassName() // Me
      Me.name // ReferenceError: Me is not defined

Warnings 
*********

- default use strict 
- class will not hoist, move definition to the top. 

Static 
*******

.. code-block:: bash 

    class Foo {
      static classMethod() {
        return 'hello';
      }
    }
    Foo.classMethod() // 'hello'

    var foo = new Foo();
    foo.classMethod()
    // TypeError: foo.classMethod is not a function


    class Foo {
      static classMethod() {
        return 'hello';
      }
    }
    class Bar extends Foo {
    }
    Bar.classMethod() // 'hello'

    class Foo {
    }

    Foo.prop = 1;
    Foo.prop // 1

attrs 
******

.. code-block:: bash 

    class IncreasingCounter {
      constructor() {
        this._count = 0;
      }
      get value() {
        console.log('Getting the current value!');
        return this._count;
      }
      increment() {
        this._count++;
      }
    }

    // same 
    class IncreasingCounter {
      _count = 0;
      get value() {
        console.log('Getting the current value!');
        return this._count;
      }
      increment() {
        this._count++;
      }
    }

private variables and attrs 
****************************

.. code-block::  bash 

    class Widget {
      // public 
      foo (baz) {
        this._bar(baz);
      }
      // private 
      _bar(baz) {
        return this.snaf = baz;
      }
      // ...
    }

And we can use symbol. But it is a little strange.

.. code-block:: bash 

    const bar = Symbol('bar');
    const snaf = Symbol('snaf');

    export default class myClass{
      // public 
      foo(baz) {
        this[bar](baz);
      }
      // private 
      [bar](baz) {
        return this[snaf] = baz;
      }
      // ...
    };

new.target 
***********

Constructor or copy-constructor 

.. code-block:: bash 

    function Person(name) {
      if (new.target !== undefined) {
        this.name = name;
      } else {
        throw new Error('must use new ');
      }
    }
    // or 
    function Person(name) {
      if (new.target === Person) {
        this.name = name;
      } else {
        throw new Error('must use new ');
      }
    }

    var person = new Person('a'); // correct
    var notAPerson = Person.call(person, 'a');  // error

In a derived class, new.target will return derived class.

extends  
***********

super must be called to initialize parent instance.
And this can be used after super.

.. code-block:: bash 

    class Point {
    }
    class ColorPoint extends Point {
      constructor(x, y, color) {
        super(x, y); // 调用父类的constructor(x, y)
        this.color = color;
      }

      toString() {
        return this.color + ' ' + super.toString(); // 调用父类的toString()
      }
    }

if constructor is not defined, then:

.. code-block:: bash 

    class ColorPoint extends Point {
    }
    // same
    class ColorPoint extends Point {
      constructor(...args) {
        super(...args);
      }
    }

super 
******

when we use super as an object, that means we are using :code:`Parent.prototype` .

.. code-block:: bash

    class A {
      constructor() {
        this.p = 2;
      }
    }
    class B extends A {
      get m() {
        return super.p;
      }
    }
    let b = new B();
    b.m // undefined


- Child class calls parent class functions, :code:`this` represents Child class.

  .. code-block:: bash 

      class A {
        constructor() {
          this.x = 1;
        }
        print() {
          console.log(this.x);
        }
      }
      class B extends A {
        constructor() {
          super();
          this.x = 2;
        }
        m() {
          super.print();
        }
      }
      let b = new B();
      b.m() // 2


- In Child, if we assign super a value (:code:`super.x = 3;` ), then we are also using child itself. 

  .. code-block:: bash 

      class A {
        constructor() {
          this.x = 1;
        }
      }
      class B extends A {
        constructor() {
          super();
          this.x = 2;
          super.x = 3;
          console.log(super.x); // undefined
          console.log(this.x); // 3
        }
      }
      let b = new B();

- in static methods, super means parent.

  .. code-block:: bash 

      class Parent {
        static myMethod(msg) {
          console.log('static', msg);
        }

        myMethod(msg) {
          console.log('instance', msg);
        }
      }

      class Child extends Parent {
        static myMethod(msg) {
          super.myMethod(msg);
        }

        myMethod(msg) {
          super.myMethod(msg);
        }
      }

      Child.myMethod(1); // static 1

      var child = new Child();
      child.myMethod(2); // instance 2


prototype and __proto__
************************

.. code-block:: bash 

    class A {
    }
    class B extends A {
    }
    B.__proto__ === A // true
    B.prototype.__proto__ === A.prototype // true

Decorator 
^^^^^^^^^^^

- Class Decorator

  Python like.

  .. code-block:: bash 

      @testable
      class MyTestableClass {
        // ...
      }
      function testable(target) {
        target.isTestable = true;
      }
      MyTestableClass.isTestable // true

- Class Function Decorator

  .. code-block:: bash 

      class Person {
        @readonly
        name() { return `${this.first} ${this.last}` }
      }

- Can't apply to pure function
  Because function will hoist.

  .. code-block:: bash 

      var readOnly = require("some-decorator");
      @readOnly
      function foo() {
      }

      # same 

      var readOnly;
      @readOnly
      function foo() {
      }
      readOnly = require("some-decorator");

Module 
^^^^^^^^

:code:`CommonJS` : backend
:code:`AMD` : UI 

Both CommonJS and AMD are dynamic.
But ES6 :code:`import` and :code:`export` are static. 

export
*******

.. code-block:: bash 

    export var lastName = 'Jackson';
    export function multiply(x, y) {
      return x * y;
    };

    function v1() { ... }
    function v2() { ... }
    export {
      v1 as streamV1,
      v2 as streamV2,
      v2 as streamLatestVersion
    };

import 
********

Read only.

.. code-block:: bash 

    import {firstName, lastName, year} from './profile.js';
    import { lastName as surname } from './profile.js';

:code:`import` will be lifetd to the top of a file.

export default
****************

.. code-block:: bash 

    export default function crc32() { 
      // ...
    }
    import crc32 from 'crc32'; 

    export function crc32() { 
      // ...
    };

    import {crc32} from 'crc32'; 

    import _, { each, forEach } from 'lodash';


Using defualt will make the module in a single package.


Constants in different modules:

.. code-block:: bash 

    // constants.js 模块
    export const A = 1;
    export const B = 3;
    export const C = 4;

    // test1.js 模块
    import * as constants from './constants';
    console.log(constants.A); // 1
    console.log(constants.B); // 3

    // test2.js 模块
    import {A, B} from './constants';
    console.log(A); // 1
    console.log(B); // 3

Browser Load ES6 
******************

.. code-block:: bash 

    <script type="module" src="./foo.js"></script>    // Async
    <script type="module" src="./foo.js" async></script>    // Sync

ES6 VS CommonJS
*******************

- CommonJS export a copy of Value while ES6 export reference.
- CommonJS load dynamically while ES6 load statically.


Reference
^^^^^^^^^^^

- http://es6.ruanyifeng.com/


.. disqus::
    :disqus_identifier: _es6_reference_rst