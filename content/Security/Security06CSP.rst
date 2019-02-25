Web Security 06 CSP
#########################################

:date: 2019-02-21
:tags: Security, Web, CSP, Web Security
:category: Security
:slug: Web_Security_06_CSP
:author: Brian Shen
:summary: Web Security 06 - CSP

.. _Web_Security_06_CSP:

.. contents::

All the sample code is in https://github.com/brianshen1990/WebSecurity .

What is Content Security Policy
********************************

The HTTP Content-Security-Policy response header allows web site administrators to control resources the user agent is allowed to load for a given page. With a few exceptions, policies mostly involve specifying server origins and script endpoints. This helps guard against cross-site scripting attacks (XSS).


For example, if I open my github blog, it will load resources from Google. I trust google, so It's OK that some google scripts are in my site.

.. figure:: /images/security/WebSecurity16.png

But what if my site load some resource from other site that I don't trust? So CSP is very important in this situation.

The syntax of CSP is simple, but we can define complex situations.

:code:`Content-Security-Policy: <policy-directive>; <policy-directive>`

For example: 

.. code-block:: bash 

    Content-Security-Policy: default-src 'self' http://example.com;
                             script-src http://example.com/

This definition means all resources can be only loaded from the current site and http://example.com, but scripts can be only loaded from http://example.com/.

There are many kinds of source:

- child-src
- connect-src
- font-src
- frame-src
- img-src
- manifest-src
- media-src
- object-src
- prefetch-src
- script-src
- style-src
- worker-src

Sample
*********

Let's assume one  bad user in our blog system post a blog. The content includes some malicious scripts. 

And when other users read his article, the page will load like this :code:`staticFile/blogView.html` :

.. code-block:: html 

    <html>
    <head>
      <script type="text/javascript" src="jquery-3.3.1.min.js"></script>
    </head>
    <body>
      <div>
        <h5>Blog Title: Sample CSP</h5>
      </div>

      <div id="blogContent">
        
        <p>This is the content of my blog.</p>
        <script type="text/javascript" src="http://localhost:8889/hackCSP.js"></script>
        <p>And I will show you how dangerous if we do not use CSP.</p>

      </div>
    </body>
    </html>

To make the demo more simple, let assume that we do not set httpOnly to our cookies :code:`index.js` :

.. code-block:: javascript

    app.use(session({
      secret: 'our apps little secret',
      resave: false,
      saveUninitialized: true,
      cookie: { maxAge: 60000, httpOnly: false }
    }))

Since we load scripts from 8889, so let's add a malicious script :code:`staticHack/hackCSP.js` :

.. code-block:: javascript

    $(document).ready(function () {
        var xxx = document.cookie;
        alert('I got cookie:' + xxx);
    })

now let's begin:

.. code-block:: bash 

    node index.js
    node indexHack.js 


Open http://localhost:8888 to login, and then open http://localhost:8888/blogView.html :

.. figure:: /images/security/WebSecurity17.png

Now we get the cookie, and we can use it to do anything.


How to fix
************

Actually, there are many ways to fix this problem:

- Cookie httpOnly
- User Content Filter
- Content Security Policy 

We will use Content Security Policy to solve this problem. So let's do a little modification to our safe site :code:`indexSafe.js` :


.. code-block:: javascript

    app.use(helmet.contentSecurityPolicy({
      directives: {
        defaultSrc: ["'self'"]
      }
    }));

and run again:

.. code-block:: bash 

    node indexSafe.js
    node indexHack.js 

.. figure:: /images/security/WebSecurity18.png

We can see from the console that the resources from 8889 are refused to load.

Reference
***********

https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy

