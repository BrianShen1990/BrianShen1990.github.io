Node Mocha Sinon
###################


:date: 2019-05-23
:tags: Node, Test, Mocha, Sinon
:category: Node
:slug: Node_Mocha_Sinon
:author: Brian Shen
:summary: Node Mocha Sinon

.. contents::

.. _Node_Mocha_Sinon:

Intro
^^^^^^

Mocha -> Test Framework 
*************************

Mocha is a feature-rich JavaScript test framework running on Node.js and in the browser, making asynchronous testing simple and fun. Mocha tests run serially, allowing for flexible and accurate reporting, while mapping uncaught exceptions to the correct test cases.

sinon -> Associated Mocks 
**************************

Standalone test spies, stubs and mocks for JavaScript. 
Works with any unit testing framework.

Quick Usage
^^^^^^^^^^^^

We will talk about 4 types of API test:

1. Function without calling functions from other modules
2. Calling sync function from other modules 
3. Calling promise from other modules
4. Calling callbacks from other modules 


Function without calling functions from other modules
*********************************************************

.. code-block:: javascript 

  // index.js 
  const ModuleB = require('./moduleB');
  module.exports.restEmpty = () => {
  }


Test Case: 

.. code-block:: javascript 

  const assert = require('assert');
  const sinon = require('sinon');
  const ModuleB = require('./moduleB');
  const index = require('./index');
  
  describe('#restEmpty() simple', function() {
    it('should run ok', function() {
      index.restEmpty();
    });
  });

Calling sync function from other modules 
******************************************

.. code-block:: javascript 

  // index.js 
  const ModuleB = require('./moduleB');
  module.exports.restGetDBInfo = () => {
    const res =  ModuleB.dbInfo();
    // send info
    // console.log(res);
  }
  
  // ModuleB.js 
  module.exports.dbInfo = () => {
    return {};
  }

Test Case:

.. code-block:: javascript 

  describe('#dbOp.restGetDBInfo() function', function() {
    let dbInfo;
    beforeEach( function() {
      dbInfo = sinon.stub(ModuleB, 'dbInfo');
    });
    afterEach( function() {
      dbInfo.restore();
    });

    it('should return value', function() {
      dbInfo.returns('test');
      index.restGetDBInfo();
      assert(dbInfo.calledOnce);
      const rReq = dbInfo.getCall(0).args[0];
      assert(!rReq);
    });
  });

Calling promise from other modules
************************************

.. code-block:: javascript 

  // index.js 
  const ModuleB = require('./moduleB');
  module.exports.restGetUsers = (name, response) => {
    return ModuleB.dbGetUser(name).then( (res) => {
      // send success
      // console.log(res);
      response && response.send(res);
    }).catch( (error) => {
      response && response.error(error);
    });
  }

  // ModuleB.js 
  module.exports.dbGetUser = (name) => {
    return new Promise( (resolve, reject) => {
      // do something
      resolve();
    }).catch( (err) => {
      reject(err);
    })
  }

Test Case: 

.. code-block:: javascript 

  describe('#dbOp.restGetUsers() promise', function() {
    const response = {
      send: () => {},
      error: () => {}
    };
    const RetValue = [{name:'test'}];
    let dbGetUser;
    let send;
    let error;
    beforeEach( function() {
      dbGetUser = sinon.stub(ModuleB, 'dbGetUser');
      send = sinon.stub(response, 'send');
      error = sinon.stub(response, 'error');
    });
    afterEach( function() {
      dbGetUser.restore();
      send.restore();
      error.restore();
    });

    it('should return value', function(done) {
      dbGetUser.resolves(RetValue);
      send.returns(null);
      index.restGetUsers('test', response).then( (res) => {
        assert(dbGetUser.calledOnce);
        assert(send.calledOnce);
        assert(!error.calledOnce);

        const dbArg = dbGetUser.getCall(0).args[0];
        assert(dbArg === 'test');
        const sendArg = send.getCall(0).args[0];
        assert.equal(sendArg, RetValue);
        
        done();
      }).catch( (err) => {
        done(err);
      });
    });
    it('should reject', function(done) {
      dbGetUser.rejects('error');
      error.returns(null);
      index.restGetUsers('test', response).then( (res) => {
        assert(dbGetUser.calledOnce);
        assert(!send.calledOnce);
        assert(error.calledOnce);
        
        const dbArg = dbGetUser.getCall(0).args[0];
        assert(dbArg === 'test');
        done();
      }).catch( (err) => {
        done(err);
      });
    });
  });

Calling callbacks from other modules 
*************************************

.. code-block:: javascript 

  // index.js
  const ModuleB = require('./moduleB');
  module.exports.restGetUsersCB = (name, response) => {
    return ModuleB.dbGetUserCB(name, (err, res) => {
      // send success
      // console.log(res);
      if(err) {
        response && response.error(err);
      } else {
        response && response.send(res);
      }
    });
  }

  // moduleB.js
  module.exports.dbGetUserCB = (name, cb) => {
    // do something
    cb({});
  }

Test Case:

.. code-block:: javascript 

  describe('#dbOp.restGetUsersCB() callback', function() {
    const response = {
      send: () => {},
      error: () => {}
    };
    const RetValue = [{name:'test'}];
    let dbGetUserCB;
    let send;
    let error;
    beforeEach( function() {
      dbGetUserCB = sinon.stub(ModuleB, 'dbGetUserCB');
      send = sinon.stub(response, 'send');
      error = sinon.stub(response, 'error');
    });
    afterEach( function() {
      dbGetUserCB.restore();
      send.restore();
      error.restore();
    });

    it('should call error', function() {
      dbGetUserCB.callsArgWith(1, 'error', null);
      error.returns(null);
      index.restGetUsersCB('test', response);
      assert(dbGetUserCB.calledOnce);
      assert(error.calledOnce);
      assert(!send.called);

      const dbArg = dbGetUserCB.getCall(0).args[0];
      assert(dbArg === 'test');
      const errorArg = error.getCall(0).args[0];
      assert(errorArg === 'error');

    });
    it('should call send', function() {
      dbGetUserCB.callsArgWith(1, null, 'test');
      send.returns(null);
      index.restGetUsersCB('test', response);
      assert(dbGetUserCB.calledOnce);
      assert(!error.calledOnce);
      assert(send.called);

      const dbArg = dbGetUserCB.getCall(0).args[0];
      assert(dbArg === 'test');
      const sendArg = send.getCall(0).args[0];
      assert(sendArg === 'test');

    });

  });

Run Test Cases
^^^^^^^^^^^^^^^

.. code-block:: bash

  mocha test_moduleB.js 

    index
      #restEmpty() simple
        ✓ should run ok
      #dbOp.restGetDBInfo() function
        ✓ should return value
      #dbOp.restGetUsers() promise
        ✓ should return value
        ✓ should reject
      #dbOp.restGetUsersCB() callback
        ✓ should call error
        ✓ should call send

    6 passing (30ms)


Report Enhancements
^^^^^^^^^^^^^^^^^^^^^

Typically, Mocha only support one kind of report which can be conjuncted with :code:`console.log` . To generate better reports, a better report extension should be added.

We use :code:`mochawesome` , a Gorgeous HTML/CSS Reporter for Mocha.js.

Quite simple usage:

:code:`mocha testfile.js --reporter mochawesome` .

Reference 
^^^^^^^^^^

- https://mochajs.org/
- https://sinonjs.org/
- https://github.com/adamgruber/mochawesome