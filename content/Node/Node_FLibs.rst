Basic Useful Node Libraries 
############################

:date: 2019-08-13
:tags: Node, Lodash, Bluebird, Superagent
:category: Node
:slug: Basic_Useful_Node_Libraries 
:author: Brian Shen
:summary: Basic Useful Node Libraries 

.. _Basic_Useful_Node_Libraries:

.. contents::

Lodash
^^^^^^^

A modern JavaScript utility library delivering modularity, performance & extras.

Many features can be replaced with native ES6 now.

Samples:

- Loop for N times

  .. code-block:: javascript

    _.times(5, (n)=>{console.log(n)});
    // 0
    // 1
    // 2
    // 3
    // 4

- Loop through a collection and return a deeply-nested property from each item 

  The point is it will handle empty attributes automatically.

  .. code-block:: javascript
    
    const ownerArr = [{
      "owner": "Colin",
      "pets": [{"name":"dog1"}, {"name": "dog2"}]
    }, {
      "owner": "John",
      "pets": [{"name":"dog3"}, {"name": "dog4"}]
    }, {
      "owner": "John",
    }];
    console.log( _.map(ownerArr, 'pets[0].name') );
    //  [ 'dog1', 'dog3', undefined ]


- Create an array of N size and populate them with unique values of the same prefix

  .. code-block:: javascript

    console.log( _.times(6, _.uniqueId.bind(null, 'ball_')) );
    // [ 'ball_1', 'ball_2', 'ball_3', 'ball_4', 'ball_5', 'ball_6' ]

- Deep Cloning

  .. code-block:: javascript

    let objA = {
      "name": "colin",
      "obj" : {
        "name": "haha"
      }
    };

    let objB = _.cloneDeep(objA);
    objB.obj.name = "ahaha";
    console.log(objB, objA);
    // { name: 'colin', obj: { name: 'ahaha' } } { name: 'colin', obj: { name: 'haha' } }

- Get Random Number between a range

  .. code-block:: javascript
      
    console.log( _.random(15, 20) );
    console.log( _.random(15, 20, true) );
    // 17
    // 17.24617688571962

- delete and pick array attributes 

  .. code-block:: javascript

    let obj7A = {"name": "colin", "car": "suzuki"};
    console.log( _.omit(obj7A, ['car', 'age']) ); // {"name": "colin"}

    let obj8A = {"name": "colin", "car": "suzuki", "age": 17};
    let obj8B = _.pick(obj8A, ['car', 'age']);
    console.log(obj8B);

    // { name: 'colin' }
    // { car: 'suzuki', age: 17 }

- Random pick elements

  .. code-block:: javascript

    const luckyDraw = ["Colin", "John", "James", "Lily", "Mary"];
    console.log( _.sample(luckyDraw) );

- Array Minus 

  .. code-block:: javascript

    const obj10A = ["Colin", "John", "James", "Lily", "Mary"];
    const obj10B = ["Lily", "Mary", "Brian"];
    console.log( _.difference(obj10A, obj10B) );
    // [ 'Colin', 'John', 'James' ]


https://colintoh.com/blog/lodash-10-javascript-utility-functions-stop-rewriting
https://lodash.com/


Bluebird 
^^^^^^^^^

As it says in github page: Bluebird is a full featured promise library with unmatched performance.

Although since ES6 we can use promises without any further thinking, but when it comes to browsers, it is still difficult, especially when we need to support legacy browsers.

So mainly I use it in frontend. However, there are some attractive features, like cancellable promises.

.. code-block:: bash

  const BPromise = require("bluebird");
  BPromise.config({
    // Enable cancellation
    cancellation: true,
  });
  const proA = new BPromise( (res, rej) => {
    setTimeout( () => {
      res("From Bluebird Promise");
    }, 1000);
  });

  proA.then( (res) => {
    console.log(res);
  })
  console.log("normal seq");

  const proB = new BPromise( (res, rej) => {
    setTimeout( () => {
      res("never will enter here Bluebird Promise");
    }, 1000);
  });

  proB.then( (res) => {
    console.log(res);
  });
  proB.cancel();
  console.log("after canceled");

  // normal seq
  // after canceled
  // From Bluebird Promise

http://bluebirdjs.com/docs/why-bluebird.html

superagent
^^^^^^^^^^^

- whatwg-fetch (fetch polyfill)
- superagent (IE9+ and Node)
- axios (IE 11+ and Node)
- request (Node)

All these are famous HTTP Client. All is very developer friendly 

.. code-block:: bash

  const superagent = require('superagent');

  // callback
  superagent
    .get('https://github.com/visionmedia/superagent')
    .then( (res) => {
      console.log(res);
    });


https://medium.com/@kartikag01/fetch-vs-axios-vs-request-promise-vs-superagent-8e78fa358d17