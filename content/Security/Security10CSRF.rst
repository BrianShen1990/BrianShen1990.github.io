Web Security 10 - CSRF
#########################################

:date: 2019-03-26
:tags: Security, Web, Https, Web Security, CSRF 
:category: Security
:slug: Web_Security_10_CSRF
:author: Brian Shen
:summary: Web Security 10 - CSRF

.. _Web_Security_10_CSRF:

.. contents::

All the sample code is in https://github.com/brianshen1990/WebSecurity .


Intro
*******

CSRF, Cross Site Request Forgery, is an attack that forces an end user to execute unwanted actions on a web application in which they're currently authenticated. CSRF attacks specifically target state-changing requests, not theft of data, since the attacker has no way to see the response to the forged request. 

In  https://brianshen1990.github.io/Web_Security_02_Referrer.html, we have given a simple example of How referrer can avoid basic attack. Actually, that sample is some kind of CSRF attack.

Sample
*******

Let's have a short review: 

Let's use the Website in the prepare session, and then, we will fake another website, which contains a malicious link to attract user to click. This malicious link is the transfer points link.

Backend :code:`indexHack.js` :

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


How to avoid CSRF attack?
***************************

- Use only JSON APIs

  AJAX calls use JavaScript and are CORS-restricted.
  There is no way for a simple :code:`<form>` to send :code:`JSON`,
  so by accepting only JSON,
  you eliminate the possibility of the above form.

- Disable CORS

  The first way to mitigate CSRF attacks is to disable cross-origin requests.
  If you're going to allow CORS,
  only allow it on :code:`OPTIONS, HEAD, GET` as they are not supposed to have side-effects.

  Unfortunately, this does not block the above request as it does not use JavaScript (so CORS is not applicable).

- Check the referrer header

  Unfortunately, checking the referrer header is a pain in the ass,
  but you could always block requests whose referrer headers are not from your site.
  This really isn't worth the trouble.

  For example, you could not load sessions if the referrer header is not your server.

- GET should not have side effects

  Make sure that none of your :code:`GET` requests change any relevant data in your database.
  This is a very novice mistake to make and makes your app susceptible to more than just CSRF attacks.

- Avoid using POST

  Because :code:`<form>` s can only :code:`GET` and :code:`POST`,
  by using other methods like :code:`PUT`, :code:`PATCH`, and :code:`DELETE`,
  an attacker has fewer methods to attack your site.

- Don't use method override!

  Many applications use (https://github.com/expressjs/method-override) to use
  :code:`PUT`, :code:`PATCH`, and :code:`DELETE` requests over a regular form.
  This, however, converts requests that were previously invulnerable vulnerable!

  Don't use :code:`method-override` in your apps - just use AJAX!

- Don't support old browsers

  Old browsers do not support CORS or security policies.
  By disabling support for older browsers
  (which more technologically-illiterate people use, who are more (easily) attacked),
  you minimize CSRF attack vectors.

- CSRF Tokens

  Alas, the final solution is using CSRF tokens.
  How do CSRF tokens work?

  1. Server sends the client a token.
  2. Client submits a form with the token.
  3. The server rejects the request if the token is invalid.

  An attacker would have to somehow get the CSRF token from your site,
  and they would have to use JavaScript to do so.
  Thus, if your site does not support CORS,
  then there's no way for the attacker to get the CSRF token,
  eliminating the threat.

  *Make sure CSRF tokens can not be accessed with AJAX!*
  Don't create a :code:`/csrf` route just to grab a token,
  and especially don't support CORS on that route!

  The token just needs to be "unguessable",
  making it difficult for an attacker to successfully guess within a couple of tries.
  It does not have to be cryptographically secure.
  An attack is one or two clicks by an unbeknownst user,
  not a brute force attack by a server.


Sample
*******

So there are many fix solutions:

1. Check change referrer https://brianshen1990.github.io/Web_Security_02_Referrer.html
2. Disable CORS (We will talk about it in https://brianshen1990.github.io/Web_Security_11_CORS.html)
3. Change this API to post instead of using get as this API will cause backend changes
4. CSRF Tokens

Now we will fix this problem in solution 3 and 4.

First let's update our API from get to post.

In backend :code:`indexSafe.js` , we change API from get to post :

.. code-block:: javascript

  app.post('/api/transferPoints', auth, (req, res) => {
    if (UserInfo[req.body.dstUser]) {
      UserInfo[req.session.name].points = UserInfo[req.session.name].points - 5;
      UserInfo[req.body.dstUser].points = UserInfo[req.body.dstUser].points + 5;
      saveUser().then( () => {
        res.status(200).send({message: 'success!' });
      }).catch( (err) => {
        res.status(500).send({message: 'Internal Server error!' });
      });
    return;
    } else {
      res.status(401).send({messgae: 'user not exists!'})
      return;
    }
  });

And in our UI :code:`staticFileSafe/test.js` :

.. code-block:: bash 

  const transfer = function () {
    const name = $('#dstUser').val();
    $.ajax({
      method: "POST",
      url: "./api/transferPoints",
      data: {
        dstUser: name
      }
    }).done( function( msg ) {
      getPoints();
    });
  }

Let's start our application again:

.. code-block:: bash 

  node indexSafe.js
  node indexHack.js 

As we can see, the malicious url cannot transfer any points now.

However, hackers can also update their methods. Let's also have an example:

:code:`staticHackPost/index.html` :

.. code-block:: bash 

  <html>
  <head>
  </head>
  <body>
    <div>
      <h5>Hack</h5>
      <form method="POST" action="http://localhost:8888/api/transferPoints">
        <input type="text" name="dstUser" id="dstUser" value="user02"/>&nbsp;
        <button type="submit">Click and you can get some discount in Amazon!</button>
      </form>
    </div>
  </body>
  </html>

and :code:`indexHackPost.js`

.. code-block:: bash

  const express = require('express');
  const session = require('express-session');
  const app = express();
  app.use(express.static('staticHackPost'))

  app.listen(8889, () => console.log('Example app listening on port 8889!'))

Now start our application again:

.. code-block:: bash 

  node indexSafe.js
  node indexHackPost.js 


.. figure:: /images/security/WebSecurity28.png 

And when we click the button, we can see our post from hack site 8889 is handled by our blog site 8888.

.. figure:: /images/security/WebSecurity29.png 

As we have said before, there are many methods to fix this problem, referrer is still an easy and simple way. However, next we will talk about the method of CSRF token.

The point of CSRF token is that, we will use another token to verify the user's identity. And for each post request, which could do modification to our backend, we will check this CSRF token and refresh it.

Many people think it is not necessary to refresh them every time. But we won't talk about that here. We will only give a simple example.

Now every time, if a user logged, we will put a CSRF token in the session, and we will stored it. When we use post method in UI, backend will verify the token in session and from post body, if verified OK,we will refresh this token. And if not , we will redirect user to login page.


Now in our :code:`indexCSRF.js` , we add CRF related functions:

.. code-block:: bash 

  const setCSRF  = function(req, res) {
    const tempCsrf = `${Math.random()}`;
    req.session.csrf = tempCsrf;
    res.setHeader("csrf", tempCsrf);
  }

  const clearCSRF  = function(req, res) {
    req.session.csrf = '';
  }

  const checkCSRF = function(req, res, next) {
    console.log(req.headers.csrf);
    console.log(req.session.csrf);
    if ( req.headers.csrf && req.session.csrf && req.session.csrf === req.headers.csrf ){
      setCSRF(req, res);
      next();
    } else {
      clearCSRF(req, res);
      res.status(403).send({messgae: 'CSRF Failure!'})
    }
  }

When we first logon, if everything is OK, we will setCSRF:

.. code-block:: bash 

  app.post('/api/login', (req, res) => {
    if (req.body.name && req.body.passwd) {
      if (!UserInfo[req.body.name]) {
        res.status(401).send({messgae: 'name or password error!'})
        return;
      } else {
        const derivedKey = crypto.createHash('md5').update(req.body.passwd).digest("hex");
        if ( UserInfo[req.body.name].passwd === derivedKey ) {
          req.session.login = true;
          req.session.name = req.body.name;
          setCSRF(req, res);
          res.status(200).send({
            messgae: 'success!'
          });
          return;
        } else {
          req.session.login = false;
          res.status(401).send({messgae: 'name or password error!'})
          return;
        };
      }
    } else {
      res.status(402).send({messgae: 'body broken!'})
      return;
    }
  });

and in the following post requests:

.. code-block:: bash 

  app.post('/api/transferPoints', auth, checkCSRF, (req, res) => {

What about UI? :code:`staticFileSafeCSRF/index.html`

.. code-block:: bash

  <body>
    <meta name="csrf-token" id="csrf-token">

And when we do post, we should do more things :code:`staticFileSafeCSRF/post.js` :

.. code-block:: bash 

  const setCSRF = function(req){
    $("#csrf-token").attr("content", req.getResponseHeader("CSRF"));
  }

  const getCSRF = function(){
    return $("#csrf-token").attr("content");
  }

  const logon = function () {
    const name = $('#name').val();
    const passwd = $('#passwd').val();
    $.ajax({
      method: "POST",
      url: "./api/login",
      data: { 
        name: name, 
        passwd: passwd 
      },
    }).done( function( msg,textStatus, request ) {
      $('#logon').hide();
      setCSRF(request);
      $('#main').show();
    });
  }
  // ...

  const transfer = function () {
    const name = $('#dstUser').val();
    $.ajax({
      method: "POST",
      url: "./api/transferPoints",
      headers: {
        'csrf': getCSRF(),
      },
      data: {
        dstUser: name
      }
    }).done( function( msg, textStatus, request ) {
      setCSRF(request);
      getPoints();
    });
  }

  ...

And now, begin application again:

.. code-block:: bash 

  node indexCSRF.js
  node indexHack.js 

Without valid CSRF, these API's cannot be accessed any more.

  .. figure:: /images/security/WebSecurity30.png 

https://www.ibm.com/developerworks/cn/web/1102_niugang_csrf/index.html

https://github.com/pillarjs/understanding-csrf
