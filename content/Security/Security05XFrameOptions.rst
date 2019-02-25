Web Security 05 - X-Frame-Options
#########################################

:date: 2019-02-20
:tags: Security, Web, X-Frame-Options, Web Security
:category: Security
:slug: Web_Security_05_X_Frame_Options
:author: Brian Shen
:summary: Web Security 05 - X-Frame-Options

.. _Web_Security_05_X_Frame_Options:

.. contents::

All the sample code is in https://github.com/brianshen1990/WebSecurity .

What is X-Frame-Options
************************

The X-Frame-Options HTTP response header can be used to indicate whether or not a browser should be allowed to render a page in a :code:`<frame>` , :code:`<iframe>` , :code:`<embed>` or :code:`<object>` . Sites can use this to avoid clickjacking attacks, by ensuring that their content is not embedded into other sites.

There are mainly three types of options:

.. code-block:: bash 

    X-Frame-Options: deny
    X-Frame-Options: sameorigin
    X-Frame-Options: allow-from https://example.com/

So what will happen is I don't set any value? 

Let's have a test:

Modify the :code:`staticHack/index.html` to add a iframe load our blog site:

.. code-block:: html 

    <html>
    <head>
    </head>
    <body>
      <div>
        <h5>Hack</h5>
        <a href='http://localhost:8888/api/transferPoints?dstUser=user02'>Click and you can get some discount in Amazon!</a>

        <hr />
        <iframe src="http://localhost:8888" ></iframe>
      </div>
    </body>
    </html>

Now start:

.. code-block:: bash 

    node index.js
    node indexHack.js

.. figure:: /images/security/WebSecurity11.png

Wow, our 8889 site can load 8888 site's content. That's not what we are expecting. 

How to fix
***********

Quite easy, all we need to do is to set the options to :code:`deny` so that our blog site won't be embed in any other site.

In :code:`indexSafe.js` :

.. code-block:: javascript 

    ...
    app.disable('x-powered-by');
    app.use(helmet.frameguard({ action: 'deny' }));

Now start again:

.. code-block:: bash 

    node indexSafe.js
    node indexHack.js

.. figure:: /images/security/WebSecurity12.png

We can see that our blog system won't be loaded in another site anymore.

Sample clickjacking
*********************

Let's talk something more about clickjacking.

Let's add another static page :code:`staticFile/hijack.html` in our blog system.

.. code-block:: html

    <html>
    <head>
      <script type="text/javascript">
        function hiJack(){
          alert('Secrets 12345678 from 8888 blog system');
        }  
      </script>
    </head>

    <body>
      <div id='logon'>
        <input type="button" onclick="hiJack()" value="Secret From 8888" />
      </div>
    </body>
    </html>

And in the hack site, we also add an static page :code:`staticHack/hijack.html` :

.. code-block:: html 

    <html>
    <head>
    </head>
    <body>
      <div>
        <iframe src="http://localhost:8888/hijack.html" ></iframe>
      </div>
    </body>
    </html>

And run sample:

.. code-block:: bash 

    node index.js
    node indexHack.js

.. figure:: /images/security/WebSecurity13.png

OK, if we are a user from blog system, then we know this will popup our secret, so we won't click the button at all.

But if we hide the iframe and put something interesting content above it to attract user to click the exactly position, then, we can luckily popup the secret. 

So let's have a small change to our hack static page :code:`staticHack/hijack.html` :

.. code-block:: html 

    <html>
    <head>
    </head>
    <body>
      <div>
        <image style="width: 180px; height: 60px; position: absolute;" src="./hijack.png"></image>
        <iframe src="http://localhost:8888/hijack.html" 
          style="width: 300px; height: 150px; border: 0; border: none; position: absolute; opacity: 0.1;"></iframe>
      </div>
    </body>
    </html>

The picture we use: 

.. figure:: /images/security/WebSecurity14.png

Now run the demo:

.. code-block:: bash 

    node index.js
    node indexHack.js

and the results: 

.. figure:: /images/security/WebSecurity15.png

As we can see, when we want to click :code:`Movies` button faked by a picture, we actually click the iframe's button from 8888. 

And the event in 8888 is triggered.

Actually, in reality, we would set :code:`opacity` to 0 so that the iframe won't display at all. 


Reference
**********

https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options
