Web Worker
#############

:date: 2019-04-10
:tags: Web Worker
:category: Web
:slug: Web_Worker
:author: Brian Shen
:summary: Web, Web Worker

.. _Web_Worker:

.. contents::

Intro
******

Web Workers is a simple means for web content to run scripts in background threads. The worker thread can perform tasks without interfering with the user interface. Once created, a worker can send messages to the JavaScript code that created it by posting messages to an event handler specified by that code (and vice versa). 

The worker context is represented by a :code:`DedicatedWorkerGlobalScope` object in the case of dedicated workers (standard workers that are utilized by a single script; shared workers use :code:`SharedWorkerGlobalScope` ). A dedicated worker is only accessible from the script that first spawned it, whereas shared workers can be accessed from multiple scripts.

You can run whatever code you like inside the worker thread, with some exceptions. For example, you can't directly manipulate the DOM from inside a worker, or use some default methods and properties of the window object.

- APIs for dedicated workers

  - constructor: :code:`Worker()` 
  - sendMessage: :code:`postMessage()` and :code:`onmessage`
  - terminate: :code:`terminate()`
  - error handling: :code:`onerror`
  - import Scripts: :code:`importScripts`

- APIs for shared workers

  - constructor: :code:`SharedWorker`
  - sendMessage: :code:`myWorker.port.postMessage()` and :code:`myWorker.port.onmessage`

    .. code-block:: javascript

      onconnect = function(e) {
        var port = e.ports[0];

        port.onmessage = function(e) {
          var workerResult = 'Result: ' + (e.data[0] * e.data[1]);
          port.postMessage(workerResult);
        }
      }

Warnings
*********

- Workers are not governed by the content security policy of the document (or parent worker) that created them.
- Data passed between the main page and workers is copied, not shared.
- Transferable Objects can be introduced. This is effective when transferring huge data. But data transferred no longer exists in the previous environment.
- Embedded workers can be loaded form scripts tags.

  .. code-block:: javascript

    // This script WILL be parsed by JS engines because its MIME type is text/javascript.

    // In the past...:
    // blob builder existed
    // ...but now we use Blob...:
    var blob = new Blob(Array.prototype.map.call(document.querySelectorAll('script[type=\'text\/js-worker\']'), function (oScript) { return oScript.textContent; }),{type: 'text/javascript'});

    // Creating a new document.worker property containing all our "text/js-worker" scripts.
    document.worker = new Worker(window.URL.createObjectURL(blob));

    document.worker.onmessage = function(oEvent) {
      pageLog('Received: ' + oEvent.data);
    };

    // Start the worker.
    window.onload = function() { document.worker.postMessage(''); };

- Embedded workers can be loaded form functions!

  .. code-block:: javascript

    function fn2workerURL(fn) {
      var blob = new Blob(['('+fn.toString()+')()'], {type: 'application/javascript'})
      return URL.createObjectURL(blob)
    }

Sample
********

:code:`index.html` :

.. code-block:: html 

  <!DOCTYPE html>
  <html>
    <head>
      <title>Web Worker</title>
      <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
      <script src="jquery.min.js"></script>
      <script src="index.js"></script>
    </head>
    <body>
      <button onclick="testWorker()">Test Workder</button>
      <p id="res"></p>
    </body>
  </html>

:code:`index.js` :

.. code-block:: javascript 

  const myWorker = new Worker('./worker.js');
  myWorker.onmessage =  (e) => {
    $('#res').text(e.data);
  };
  const testWorker = () => {
    myWorker.postMessage([3,4]);
  };

:code:`worker.js` :

.. code-block:: javascript 

  onmessage = function(e) {
    console.log('Message received from main script');
    const workerResult = 'Result: ' + (e.data[0] * e.data[1]);
    console.log('Posting message back to main script');
    postMessage(workerResult);
  }

Now start our website :code:` http-server ./` :

.. figure:: /images/web/webworker01.png 

Reference
**********

https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers



