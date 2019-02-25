Web Security 01 - Prepare
##########################

:date: 2019-02-12
:tags: Security, Web, Web Security
:category: Security
:slug: Web_Security_01_Prepare
:author: Brian Shen
:summary: Web Security 01 - Prepare

.. _Web_Security_01_Prepare.rst:

.. contents::

All the sample code is in https://github.com/brianshen1990/WebSecurity .

Intro 
******

In this series, I will talk about the web security problems and how to prevent them.
Security is becoming more and more important, especially in a world where all users are surfing the internet, and a world any programmer can expose a service. It seems that many websites we visit, many services we use, are not that secure enough. But since we enjoy the free services, sometimes we think a little privacy and insecure is acceptable. A quite strange era.

However, whether those services are safe or not, when we ourselves provide a service to our customer, free or charge, I think we should always try to protect a user's information, and try to guarantee a safe digital world to them. Maybe it will costs many time, but, it worths. 

All those problems are summarized from my experience. It will cover the following topics: 

- Referer


Only for my reference, so if there is any problem, you can kindly point out.

Assume a situation
********************

In order to provide some examples, I will assume that I provide some services to my customer.
Here is the situation, we will create a blog system, and there is a point sub system in it. Every registered user will have 200 points. And if he or she publishes blogs and makes comments, additional points will be rewarded. 

And those points can be transferred to other users. 

So let's use Express to hold such a website. 

Four services are provided: 

- register 
- login
- get points
- transfer points (through get method)

To make the example simple enough, we won't use any database here. All we need to do is to store user information in a JSON file.

So this is our express backend, providing 4 APIs:

- :code:`/api/addUser` 
- :code:`/api/login`
- :code:`/api/getPoints`
- :code:`/api/transferPoints`

Code detail:

.. code-block:: javascript

    const express = require('express');
    const session = require('express-session');
    const bodyParser = require('body-parser')
    const fs = require('fs');
    const crypto = require('crypto');
    const app = express();
    const UserInfoFile = './data/userInfo.json';
    const UserInfo = require(UserInfoFile);

    const saveUser = function() {
      return new Promise( (resolve, reject) => {
        fs.writeFile(UserInfoFile, JSON.stringify(UserInfo), (err) => {
          if (err) {
            reject(err);
          } else {
            resolve();
          }
        });
      });
    }

    app.use(session({
      secret: 'our apps little secret',
      resave: false,
      saveUninitialized: true,
      cookie: { maxAge: 60000 }
    }))

    app.use(bodyParser.urlencoded({
      extended: true
    }));
    app.use(bodyParser.json());


    app.post('/api/addUser', (req, res) => {
      if (req.body.name && req.body.passwd) {
        if (UserInfo[req.body.name]) {
          res.status(402).send({messgae: 'name exists!'})
          return;
        } else {
          const derivedKey = crypto.createHash('md5').update(req.body.passwd).digest("hex");
          UserInfo[req.body.name] = {
            passwd: derivedKey,
            points: 200,
          };
          saveUser().then( () => {
            res.status(200).send({messgae: 'success!'})
            return;
          }).catch( (err) => {
            res.status(500).send({messgae: 'Internal server error!'})
            return;
          });
        }
      } else {
        res.status(402).send({messgae: 'body broken!'})
        return;
      }
    });

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
            res.status(200).send({messgae: 'success!'})
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

    const auth = function(req, res, next) {
      if (req.session.login) {
        if (!UserInfo[req.session.name]) {
          res.status(401).send({messgae: 'user not exists!'})
          return;
        } else {
          next();
        }
      } else {
        res.status(402).send({messgae: 'auth broken!'})
        return;
      }
    }

    app.get('/api/getPoints', auth, (req, res) => {
      res.status(200).send({points: UserInfo[req.session.name].points})
      return;
    });

    app.get('/api/transferPoints', auth, (req, res) => {
      if (UserInfo[req.query.dstUser]) {
        UserInfo[req.session.name].points = UserInfo[req.session.name].points - 5;
        UserInfo[req.query.dstUser].points = UserInfo[req.query.dstUser].points + 5;
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

    app.get('/api/', (req, res) => res.send('Hello World!'))

    app.use(express.static('staticFile'))

    app.listen(8888, () => console.log('Example app listening on port 8888!'))



And this is our UI code:

HTML (Simplest jQuery):

.. code-block:: html 

    <html>

    <head>
      <script type="text/javascript" src="jquery-3.3.1.min.js"></script>
      <script type="text/javascript" src="test.js"></script>
    </head>

    <body>
      <div id='logon'>
        <h5>Logon</h5>
        <input type="text" id="name" />&nbsp;
        <input type="text" id="passwd" />&nbsp;
        <input type="button" onclick="logon()" value="Logon" />
      </div>

      <div id='main'>
        <h5>Points</h5>
        <span id="points"></span>&nbsp;
        <input type="button" onclick="getPoints()" value="getpoints" />
        <br />
        <input type="text" id="dstUser" />&nbsp;
        <input type="button" onclick="transfer()" value="Transfer" />
      </div>
    </body>

    </html>

JS:

.. code-block:: javascript

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
      }).done( function( msg ) {
        $('#logon').hide();
        $('#main').show();
      });
    }

    const getPoints = function(){
      $.ajax({
        method: "GET",
        url: "./api/getPoints",
      }).done( function( msg ) {
        $('#points').text(msg.points);
      });
    }

    const transfer = function () {
      const name = $('#dstUser').val();
      $.ajax({
        method: "GET",
        url: "./api/transferPoints?dstUser=" + name,
      }).done( function( msg ) {
        getPoints();
      });
    }

    $(document).ready(function () {
      $('#logon').show();
      $('#main').hide();
    })

And the results: 

.. figure:: /images/security/WebSecurity01.png

.. figure:: /images/security/WebSecurity02.png

OK, our prepare work has been done!