Web Security 11 - CORS
#########################################

:date: 2019-04-08
:tags: Security, Web, Https, Web Security, CORS 
:category: Security
:slug: Web_Security_11_CORS
:author: Brian Shen
:summary: Web Security 11 - CORS

.. _Web_Security_11_CORS:

.. contents::

All the sample code is in https://github.com/brianshen1990/WebSecurity .

Intro
*******

Cross-Origin Resource Sharing (CORS) is a mechanism that uses additional HTTP headers to tell a browser to let a web application running at one origin (domain) have permission to access selected resources from a server at a different origin. A web application executes a cross-origin HTTP request when it requests a resource that has a different origin (domain, protocol, and port) than its own origin.

Headers
*********

- Access-Control-Allow-Origin

  specifies either a single origin, which tells browsers to allow that origin to access the resource; or else — for requests without credentials — the "*" wildcard, to tell browsers to allow any origin to access the resource.
  
- Access-Control-Expose-Headers

  The Access-Control-Expose-Headers header lets a server whitelist headers that browsers are allowed to access.

- Access-Control-Max-Age

  The Access-Control-Max-Age header indicates how long the results of a preflight request can be cached. 

- Access-Control-Allow-Credentials

  The Access-Control-Allow-Credentials header Indicates whether or not the response to the request can be exposed when the credentials flag is true. When used as part of a response to a preflight request, this indicates whether or not the actual request can be made using credentials. 

- Access-Control-Allow-Methods

  The Access-Control-Allow-Methods header specifies the method or methods allowed when accessing the resource. This is used in response to a preflight request.

- Access-Control-Allow-Headers

  The Access-Control-Allow-Headers header is used in response to a preflight request to indicate which HTTP headers can be used when making the actual request.

Sample: Not sharing data 
*************************

Let's look at our blog system :code:`index.js` , there is an API that will send Hello World.

.. code-block:: javascript 

  app.get('/api/', (req, res) => res.send('Hello World!'))

If we try to get the resource from a different site 8889: 

:code:`staticFileHack/index.html` :

.. code-block:: html 

  <html>
    <head>
      <script type="text/javascript" src="jquery-3.3.1.min.js"></script>
      <script>
        const test = function(){
          $.ajax({
            method: "GET",
            url: "http://localhost:8888/api/",
          }).done( function( msg ) {
            alert(msg);
          });
        }
      </script>
    </head>
  <body>
    <div>
      <h5>Hack Dev</h5>
      <button onclick="test()">Load Resource From 8888.</button>
    </div>
  </body>

  </html>

And run: 

.. code-block:: bash 

  node index.js
  node indexHack.js 

When we click the button, the resource won't be allowed to be loaded.

.. figure:: /images/security/WebSecurity31.png 

By default, if we do not set :code:`Access-Control-Allow-Origin` in response header, other site cannot access those resources.

Sample: Sharing data 
*********************

Then how to share And why to share. There are many reasons actually, but the main one is that we need to share our resources, especially when we are in developing stage.

Suppose we have a site run in one node :code:`ip1:80` . We use angular or react to develop. We don;t want to start a backend server locally. Since we have :code:`ip1:80` , we can use this server. That is we can use our local UI while access the remote backend. That would be quite convenient. 

So let's share our backend resources! :code:`indexShare.js` 

.. code-block:: javascript

  // ...
  const cors = require('cors');
  // ...
  app.get('/api/',  cors(),  (req, res) => res.send('Hello World!'))
  // ...

.. code-block:: bash 

  node indexShare.js
  node indexHack.js 

When we get this resource, there won't be any problem.

.. figure:: /images/security/WebSecurity32.png 

As we can see, an special header had been added to the response.

Reference
**********

https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS