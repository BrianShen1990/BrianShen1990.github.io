Ratio Window Solutions
#########################


:date: 2019-10-10
:tags: CSS, Web
:category: Web
:slug: Ratio Window Solutions
:author: Brian Shen
:summary: Ratio Window Solutions


Intro
^^^^^^

About keeping UI elements in a fixed ratio, there are many solutions. Most of them are related to how to keep height in a fixed ratio with width.

Well, that's is not that hard. What's really hard is that how to keep width in fixed ratio with height.

Why this requirement occurs? Nowadays, more companies need to display a page on their large screen in order to show off  before their monitors. If we want our UI presentations to show their best, we need to take the full screen. But screen size varies. That means the best way is to take all the available height, and then scale the width as modern screens' width-to-height ratio is increasing.

OK, let's simplify the question, keep the page in a ratio of 4:3.

4:3 According to width
^^^^^^^^^^^^^^^^^^^^^^^

Magic :code:`padding-top`
**************************

.. code-block:: bash 

  <!DOCTYPE html>
  <html>
  <head>
    <style>
      body {
        width: 100%;
        height: 100%;
      }
      .rectangle {
        width: 50%;
        height: 100%;
      }
      .per43 {
        padding-top: 75%;
        background-color: orange;
      }
    </style>
  </head>
  <body>
    <div class="rectangle">
      <div class="per43">
        some VW text 
      </div>
    </div>
  </body>
  </html>

.. figure:: /images/Web/Web_RatioWindow_01.png

Everything seems perfect, but if we look careful, we would notice that the real height, is higher than 75%, it includes a extra text height.

OK, problems happen. If we need to keep perfectly accurate ratio, we should put all things in absolute position. 

Let's change our code:

.. code-block:: bash 

  .text {
    position: absolute;
    top: 10%;
    left: 10%; 
  }
  <div class="per43">
    <div class="text">some VW text </div>
  </div>

.. figure:: /images/Web/Web_RatioWindow_02.png

VM 
***

Visual Width. That's is the width compared with browser's width. 

.. code-block:: bash 

  <!DOCTYPE html>
  <html>
  <head>
    <style>
      body {
        width: 100%;
        height: 100%;
      }
      .per43 {
        width: 50vw;
        height: 37.5vw;
        background-color: orange;
      }
    </style>
  </head>
  <body>
    <div class="per43">
      <div class="text">some VW text </div>
    </div>
  </body>
  </html>

.. figure:: /images/Web/Web_RatioWindow_03.png

Perfect! But this scenario has limitations:

Width can only be referenced to browser's width.


4:3 According to height
^^^^^^^^^^^^^^^^^^^^^^^^

The previous two samples are both to keep a ratio according to width. But what about height?

Using an image. 

.. figure:: /images/Web/Web_RatioWindow_05.png

.. code-block:: bash 

  <!DOCTYPE html>
  <html>
  <head>
    <style>
      html, body {
        width: 100%;
        height: 100%;
        margin: 0px;
        min-height: 300px;
      }
      .per43 {
        height: 100%;
        background-color: green;
        text-align: center;
      }
      .per43 > img {
        height: 100%;
      }
    </style>
  </head>
  <body>
    <div class="per43">
      <img src="./K43.png" />
    </div>
  </body>
  </html>

.. figure:: /images/Web/Web_RatioWindow_04.gif

OK, that's amazing, right?

However, it would be very painful if we want to add some content.

.. code-block:: bash

  <!DOCTYPE html>
  <html>
  <head>
    <style>
      html, body, .outer{
        width: 100%;
        height: 100%;
        margin: 0px;
        min-height: 300px;
        text-align: center;
      }
      .outer {
        background-color: red;
      }
      .per43 {
        height: 100%;
        background-color: green;
        text-align: center;
        margin: 0 auto;
        display: inline-block;
      }
      .per43 > img {
        height: 100%;
      }
      .innerContent {
        position: absolute;
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
      }
    </style>
  </head>
  <body>
    <div class="outer">
      <div class="per43">
        <img src="./K43.png" />
        <div class="innerContent">
          <div>
            hhhh
          </div>
          <div>
            hhhh2
          </div>
        </div>
      </div>
    </div>
  </body>
  </html>

.. figure:: /images/Web/Web_RatioWindow_06.gif

Now we can fill whatever we want with relative position.

