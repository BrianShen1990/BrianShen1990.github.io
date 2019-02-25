Web Security 03 - X Powered By / Server 
#########################################

:date: 2019-02-14
:tags: Security, Web, XPoweredBy, Web Security
:category: Security
:slug: Web_Security_03_X_Powered_By
:author: Brian Shen
:summary: Web Security 03 - X Powered By 

.. _Web_Security_03_X_Powered_By:

.. contents::

All the sample code is in https://github.com/brianshen1990/WebSecurity .

What is X-Powered-By / Server 
********************************

Many of us may not notice this http header until we use a security scan tool to scan our website. And we notice that those tools often suggest us to remove this kind of header, for 2 reasons:

1. Make http header more slight
2. Avoid potential vulnerability. 

So let's have a look at this header.

.. code-block:: bash 

    node index.js 


.. figure:: /images/security/WebSecurity07.png

This header suggests that our backend is supported by Express. 

Other sample: 

.. figure:: /images/security/WebSecurity08.png

.. figure:: /images/security/WebSecurity09.png

Those can leak the backend server information. As we know, for Apache, IIS, there are some special security bugs. If a hacker knows which server a website is using and potential bugs of this kind of server, some attacks may be taken. 

How to fix 
************

How can we remove this kind of http header then?

Different backends have different configurations. Here we only cover our sample: Express. 

In Express, we also use Helmet. 

In :code:`indexSafe.js` :

.. code-block:: javascript 

    ... 
    app.use(bodyParser.urlencoded({
      extended: true
    }));
    app.use(bodyParser.json());
    app.use(helmet.referrerPolicy({ policy: 'same-origin' }));
    app.disable('x-powered-by');
    ...

Now start again: 

.. code-block:: bash 

    node indexSafe.js 

.. figure:: /images/security/WebSecurity10.png

There will be no server information any more. 

