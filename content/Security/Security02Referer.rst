Web Security 02 - Referrer
###########################

:date: 2019-02-13
:tags: Security, Web, Referrer, Web Security
:category: Security
:slug: Web_Security_02_Referrer
:author: Brian Shen
:summary: Web Security 02 - Referrer

.. _Web_Security_02_Referrer.rst:

.. contents::

All the sample code is in https://github.com/brianshen1990/WebSecurity .

Definition of Referrer
^^^^^^^^^^^^^^^^^^^^^^

The Referrer request header contains the address of the previous web page from which a link to the currently requested page was followed. The Referrer header allows servers to identify where people are visiting them from and may use that data for analytics, logging, or optimized caching, for example.

A Referrer header is not sent by browsers if:

  - The referring resource is a local "file" or "data" URI.
  - An unsecured HTTP request is used and the referring page was received with a secure protocol (HTTPS).

https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referer
https://developer.mozilla.org/en-US/docs/Web/Security/Referer_header:_privacy_and_security_concerns


Security - Check Referrer 
^^^^^^^^^^^^^^^^^^^^^^^^^^

If we do not check Referrer, API can be called from anyplace, which may cause security problems. 

Sample
*******

Let's use the Website in the prepare session, and then, we will fake another website, which contains a malicious link to attract user to click. This malicious link is the transfer points link.


Backend code:`indexHack.js` :

.. code-block:: javascript

    const express = require('express');
    const session = require('express-session');
    const app = express();
    app.use(express.static('staticHack'))

    app.listen(8889, () => console.log('Example app listening on port 8889!'))

HTML :code:`staticHack/index.html` : 

.. code-block:: html

    <html>

    <head>
      <script type="text/javascript" src="jquery-3.3.1.min.js"></script>
      <script type="text/javascript" src="test.js"></script>
    </head>

    <body>
      <div>
        <h5>Hack</h5>
        <a href='http://localhost:8888/api/transferPoints?dstUser=user02'>Click and you can get some discount in Amazon!</a>
      </div>
    </body>

    </html>


Now start the two websites:

.. code-block:: bash 

    node index.js
    node indexHack.js 


This is the Malicious website:

.. figure:: /images/security/WebSecurity03.png

When we click the URL, the authentication will fail. A message like this will appear :code:`{"messgae":"auth broken!"}` .

This is because we haven't login yet. But what if we've opened our Blog System and already login?

.. figure:: /images/security/WebSecurity04.png

Now, we jump to the malicious website, and click the link, successful message will appear :code:`{"message":"success!"}` . and user01 will transfer his points to user02, unconsciously. 

How to fix
************

As we can see, this is totally something we are not expecting: how can a user from another site, calls API in this site?

This is something what Referrer does: APIs should be only called from the same site. Calls from other sites should be rejected.

Now, let's add some Referrer check functions (in :code:`indexSafe.js` , same content with security implementation):

.. code-block:: javascript

    const REFERES = [
      'http://localhost:8888',
    ];
    const refererCheck = function(req, res, next) {
      const refer = req.header('referer');
      console.log(refer);
      if (!refer) {
        res.status(404).send({messgae: 'referer check failure!'})
        return;
      } else {
        let found = false;
        REFERES.forEach( (item) => {
          if (refer.startsWith(item)) {
            found = true;
            return false;
          }
        });
        if (found) {
          next();
        } else {
          res.status(404).send({messgae: 'referer check failure!'})
          return;
        }
      }
    }

    app.post('/api/addUser', refererCheck, (req, res) ...
    app.post('/api/login', refererCheck, (req, res) ...
    app.get('/api/getPoints', refererCheck, auth, (req, res) ...
    app.get('/api/transferPoints', refererCheck, auth, (req, res) ...


When we start this website again, 

.. code-block:: bash 

    node indexSafe.js

A Referrer check failure message will appear: :code:`{"messgae":"referer check failure!"}` .

Security - Referrer Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^

While Referrer check is very important, some users don't want to expose their Referrer at all.

For example, if we are surfing :code:`http://localhost:8888/` , then, we type :code:`http://localhost:8889/` in the browser address column, it will go to 8889 website. But, we don't want 8889 to know where do I come from. I want to hide my Referrer when I go to another website. 

That is the Referrer Policy.

There are many types of Referrer policy (https://www.w3.org/TR/referrer-policy/#referrer-policies).

- "no-referrer": 
  no referrer information is to be sent along with requests made from a particular request client to any origin. The header will be omitted entirely.
- "no-referrer-when-downgrade" : 
  The "no-referrer-when-downgrade" policy sends a full URL along with requests from a TLS-protected environment settings object to a potentially trustworthy URL, and requests from clients which are not TLS-protected to any origin.
- "same-origin" : 
  a full URL, stripped for use as a referrer, is sent as referrer information when making same-origin requests from a particular client.
- "origin" : 
  only the ASCII serialization of the origin of the request client is sent as referrer information when making both same-origin requests and cross-origin requests from a particular client.
- "strict-origin" :
  The "strict-origin" policy sends the ASCII serialization of the origin of the request client when making requests:

  - from a TLS-protected environment settings object to a potentially trustworthy URL, and
  - from non-TLS-protected environment settings objects to any origin.

- "origin-when-cross-origin" : 
  a full URL, stripped for use as a referrer, is sent as referrer information when making same-origin requests from a particular request client, and only the ASCII serialization of the origin of the request client is sent as referrer information when making cross-origin requests from a particular client.
- "strict-origin-when-cross-origin" :
  a full URL, stripped for use as a referrer, is sent as referrer information when making same-origin requests from a particular request client, and only the ASCII serialization of the origin of the request client when making cross-origin requests:

  - from a TLS-protected environment settings object to a potentially trustworthy URL, and
  - from non-TLS-protected environment settings objects to any origin.
- "unsafe-url" : 
  a full URL, stripped for use as a referrer, is sent along with both cross-origin requests and same-origin requests made from a particular client.


So many definitions, but mainly we will use :code:`same-origin` .

Sample
*******


Let's make a little change to our code. Add a link in html page :code:`staticFile/index.html` :

.. code-block:: html

    <br>
    <a href='http://localhost:8889'>Go To 8889</a>

Start our application:

.. code-block:: bash 

    node index.js


When we click the link, it will get 8889's index.html with referrer 8888: 

.. figure:: /images/security/WebSecurity05.png

Sometimes, it can leak our information.

How to fix it
**************

Let's add some referrer policy:

.. code-block:: bash 

    const helmet = require('helmet')
    ...
    app.use(helmet.referrerPolicy({ policy: 'same-origin' }));

Now, let check our websites again:

.. code-block:: bash 

    node indexSafe.js 

.. figure:: /images/security/WebSecurity06.png

There will be no referrer at all. 

