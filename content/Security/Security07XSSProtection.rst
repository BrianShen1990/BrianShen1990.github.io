Web Security 07 - XSS Protection
#########################################

:date: 2019-02-26
:tags: Security, Web, XSS Protection, Web Security
:category: Security
:slug: Web_Security_07_XSS_Protection
:author: Brian Shen
:summary: Web Security 07 - XSS Protection

.. _Web_Security_07_XSS_Protection:

.. contents::

All the sample code is in https://github.com/brianshen1990/WebSecurity .

What is XSS 
*************


Cross-site scripting, abbreviated to “XSS”, is a way attackers can take over webpages. 
One may wonder the abbreviation should be "CSS", but CSS is actually Cascaded Style Sheet.

The goal of an XSS attack is to gain control of JavaScript in the victim’s browser. Once a hacker has done that, there’s a lot of nasty stuff they can do: log your actions, impersonate you, steal your authentication cookies, and much more.


XSS attacks can generally be categorized into two categories: stored and reflected.

- Stored XSS Attacks

  Stored attacks are those where the injected script is permanently stored on the target servers, such as in a database, in a message forum, visitor log, comment field, etc. The victim then retrieves the malicious script from the server when it requests the stored information. Stored XSS is also sometimes referred to as Persistent or Type-I XSS.

- Reflected XSS Attacks

  Reflected attacks are those where the injected script is reflected off the web server, such as in an error message, search result, or any other response that includes some or all of the input sent to the server as part of the request. Reflected attacks are delivered to victims via another route, such as in an e-mail message, or on some other website. When a user is tricked into clicking on a malicious link, submitting a specially crafted form, or even just browsing to a malicious site, the injected code travels to the vulnerable web site, which reflects the attack back to the user’s browser. The browser then executes the code because it came from a "trusted" server. Reflected XSS is also sometimes referred to as Non-Persistent or Type-II XSS.


Sample
*******

This section, we will give a sample of reflected XSS Attacks. Since we have a blog system, sometimes a user has to search for some blogs. But suppose that we allow users to input anything without filtering.

This is the search page :code:`__viewPage.html` :

.. code-block:: html 

    <html>
    <head>
      <script type="text/javascript" src="jquery-3.3.1.min.js"></script>
      <script type="text/javascript">
        const testXss = function(){
          window.location = "?search=" + $("#xssId").val();
        }
      </script>
    </head>
    <body>
    <br>
    XSS Tested:
    <input type="text" id="xssId" > &nbsp; <input type="button" onclick="testXss()" value="Search" />
    <div>
      You searched: <span id="xssReflected"></span>
    </div>
    </body>
    </html>

To demo the :code:`X-XSS-Protection` flag, we will send client the raw content, instead of a file :code:`index.js` :


.. code-block:: javascript 

    app.get('/viewPage.html', (req, res) => { 
      const tempVal = req.param('search');
      console.log(tempVal);
      let html = `<html>
      <head>
        <script type="text/javascript" src="jquery-3.3.1.min.js"></script>
        <script type="text/javascript">
          const testXss = function(){
            window.location = "?search=" + $("#xssId").val();
          }
        </script>
      </head>
      <body>
      <br>
      XSS Tested:
      <input type="text" id="xssId" > &nbsp; <input type="button" onclick="testXss()" value="Search" />
      <div>
        You searched: <span id="xssReflected">${tempVal}</span>
      </div>
      </body>
      </html>` ;

      res.send(html); 
    });


Now let's start our website:

.. code-block:: bash 

    node index.js 

In our browser, input :code:`localhost:8888/viewPage.html` . If we search :code:`node` , then our website will return a page with the search keywords.

.. figure:: /images/security/WebSecurity19.png

However, if we input something malicious like :code:`<script>alert("I take over the browser now!")</script>` :

.. figure:: /images/security/WebSecurity20.png

Look, chrome just blocks the scripts and refuses to load the page. But actually, there is no XSS header at all.

Because for Chrome, XSS Auditor blocks by default. (https://www.chromestatus.com/feature/5748927282282496) .

However, if we force chrome to disable XSS Auditor :code:`index.js` :

.. code-block:: javascript

      </html>` ;
      res.set('X-XSS-Protection', 0);
      res.send(html); 
    });

and start again:

.. code-block:: bash 

    node index.js 

.. figure:: /images/security/WebSecurity21.png

Scripts can be executed.

How Chrome XSS Auditor works?
******************************

https://www.chromium.org/developers/design-documents/xss-auditor

The XSS Auditor works by matching request data to data in a response page.

So by comparing our URL and the page content, if there are some scripts and the content is same, then there is a possibility that the page may contains XSS attack.

How to fix 
*************

The HTTP X-XSS-Protection response header is a feature of Internet Explorer, Chrome and Safari that stops pages from loading when they detect reflected cross-site scripting (XSS) attacks. Although these protections are largely unnecessary in modern browsers when sites implement a strong Content-Security-Policy that disables the use of inline JavaScript ('unsafe-inline'), they can still provide protections for users of older web browsers that don't yet support CSP.

Let's do a little modification to our :code:`indexSafe.js` :

.. code-block:: bash 

    app.use(helmet.xssFilter());

and run :

.. code-block:: bash 

    node indexSafe.js 

Then, it won't be loaded again:

.. figure:: /images/security/WebSecurity22.png

(If any step fails, please use incognito window to open it.)

https://www.owasp.org/index.php/Cross-site_Scripting_(XSS)
https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-XSS-Protection
