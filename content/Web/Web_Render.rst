Browser Render Process
#######################

:date: 2019-03-01
:tags: UI, Render Process 
:category: Web
:slug: Render Process
:author: Brian Shen
:summary: Browser Render Process

.. contents::

.. _Browser_Render_Process:

Render Process 
**************

The normal render process in a browser goes through this periods.

:code:`JavaScript => Style => Layout => Paint => Compositing`

- **JavaScript.** Typically JavaScript is used to handle work that will result in visual changes, whether it’s jQuery’s animate function, sorting a data set, or adding DOM elements to the page. It doesn’t have to be JavaScript that triggers a visual change, though: CSS Animations, Transitions, and the Web Animations API are also commonly used.
- **Style calculations.** This is the process of figuring out which CSS rules apply to which elements based on matching selectors, for example, :code:`.headline` or :code:`.nav > .nav__item` . From there, once rules are known, they are applied and the final styles for each element are calculated.
- **Layout.** Once the browser knows which rules apply to an element it can begin to calculate how much space it takes up and where it is on screen. The web’s layout model means that one element can affect others, for example the width of the <body> element typically affects its children’s widths and so on all the way up and down the tree, so the process can be quite involved for the browser.
- **Paint.** Painting is the process of filling in pixels. It involves drawing out text, colors, images, borders, and shadows, essentially every visual part of the elements. The drawing is typically done onto multiple surfaces, often called layers.
- **Compositing.** Since the parts of the page were drawn into potentially multiple layers they need to be drawn to the screen in the correct order so that the page renders correctly. This is especially important for elements that overlap another, since a mistake could result in one element appearing over the top of another incorrectly.

Visual Change Process 
***********************

You won’t always necessarily touch every part of the pipeline on every frame. In fact, there are three ways the pipeline normally plays out for a given frame when you make a visual change, either with JavaScript, CSS, or Web Animations:


- JS > Style > Layout > Paint > Composite ( :code:`Re-Layout` or :code:`re-flow` )

:code:`JavaScript => Style => Layout => Paint => Compositing`

If you change a “layout” property, so that’s one that changes an element’s geometry, like its width, height, or its position with left or top, the browser will have to check all the other elements and “reflow” the page. Any affected areas will need to be repainted, and the final painted elements will need to be composited back together.

- JS > Style > Paint > Composite  ( :code:`Re-Paint` )

:code:`JavaScript => Style => Paint => Compositing`

If you changed a “paint only” property, like a background image, text color, or shadows, in other words one that does not affect the layout of the page, then the browser skips layout, but it will still do paint.

- JS > Style > Composite 

:code:`JavaScript => Style => Compositing`

If you change a property that requires neither layout nor paint, and the browser jumps to just do compositing.

This final version is the cheapest and most desirable for high pressure points in an app's lifecycle, like animations or scrolling.

Sample
*******

OK Let's have a quick sample.

:code:`test.html` :

.. code-block:: html

    <html>
    <head>
      <style>
        .paintOnly {
          color: red;
        }
      </style>
      <script type="text/javascript" src="jquery-3.3.1.min.js"></script>
      <script>
        const reLayout = function () {
          $('#divTest').html(Math.random());
        };
        const rePaint = function () {
          $('#divTest').addClass('paintOnly');
        };
      </script>
    </head>
    <body>
      <div>
        <h5>Test</h5>
        <div id="divTest"></div>
        <input type="button" onclick="reLayout()" value="Test Re-Layout" />
        <input type="button" onclick="rePaint()" value="Test Re-Paint" />
      </div>
    </body>
    </html>

Open in chrome:

.. figure:: /images/web/webRender03.png 

And when I record the performance in Chrome and analyze it:

.. figure:: /images/web/webRender02.png 

.. figure:: /images/web/webRender01.png 

As we can see, :code:`html()` method will lead the div to change width and heigh, so it will trigger re-Layout.

But when we use :code:`addClass()` and the added class only changes the text color, no Layout needs to be changed, and there is no Layout process. 

Optimizing - JS 
*****************

- Avoid :code:`setTimeout` or :code:`setInterval` for visual updates; always use :code:`requestAnimationFrame` instead.

  The only way to guarantee that your JavaScript will run at the start of a frame is to use :code:`requestAnimationFrame` .

  Frameworks or samples may use :code:`setTimeout` or :code:`setInterval` to do visual changes like animations, but the problem with this is that the callback will run at some point in the frame, possibly right at the end, and that can often have the effect of causing us to miss a frame, resulting in jank.

- Move long-running JavaScript off the main thread to Web Workers.
- Use micro-tasks to make DOM changes over several frames.
- Use Chrome DevTools’ Timeline and JavaScript Profiler to assess the impact of JavaScript.

Optimizing - Style 
********************

Reduce the Scope and Complexity of Style Calculations:

- Reduce the complexity of your selectors; use a class-centric methodology like BEM.
- Reduce the number of elements on which style calculation must be calculated.


BEM (Block, Element, Modifier):

  It recommends that everything has a single class, and, where you need hierarchy, that gets baked into the name of the class as well:


.. code-block:: css 

  .list { }
  .list__list-item { }
  .list__list-item--last-child {}

Optimizing - Layout  
********************

Avoid Large, Complex Layouts and Layout Thrashing

- Layout is normally scoped to the whole document.
- The number of DOM elements will affect performance; you should avoid triggering layout wherever possible.

  Layout is almost always scoped to the entire document

- Assess layout model performance; new Flexbox is typically faster than older Flexbox or float-based layout - models.
- Avoid forced synchronous layouts and layout thrashing; read style values then make style changes.

  First the JavaScript runs, then style calculations, then layout. It is, however, possible to force a browser to perform layout earlier with JavaScript. It is called a **forced synchronous layout**.

  We may want to write out the height of an element (let’s call it “box”) at the start of the frame you may write some code like this:

  .. code-block:: javascript

    requestAnimationFrame(logBoxHeight);

    function logBoxHeight() {
      // Gets the height of the box in pixels and logs it out.
      console.log(box.offsetHeight);
    }

  Things get problematic if we changed the styles of the box before we ask for its height:

  .. code-block:: javascript

    function logBoxHeight() {

      box.classList.add('super-big');

      // Gets the height of the box in pixels
      // and logs it out.
      console.log(box.offsetHeight);
    }

  Now, in order to answer the height question, the browser must first apply the style change (because of adding the super-big class), and then run layout. Only then will it be able to return the correct height. This is unnecessary and potentially expensive work.

  Correct:

  .. code-block:: javascript

    function logBoxHeight() {
      // Gets the height of the box in pixels
      // and logs it out.
      console.log(box.offsetHeight);

      box.classList.add('super-big');
    }

  There’s a way to make forced synchronous layouts even worse: **do lots of them in quick succession** . Take a look at this code:

  .. code-block:: javascript

    function resizeAllParagraphsToMatchBlockWidth() {
      // Puts the browser into a read-write-read-write cycle.
      for (var i = 0; i < paragraphs.length; i++) {
        paragraphs[i].style.width = box.offsetWidth + 'px';
      }
    }

  Fix :

  .. code-block:: javascript

    // Read.
    var width = box.offsetWidth;

    function resizeAllParagraphsToMatchBlockWidth() {
      for (var i = 0; i < paragraphs.length; i++) {
        // Now write.
        paragraphs[i].style.width = width + 'px';
      }
    }

Optimizing - Painting   
***********************

- Changing any property apart from transforms or opacity always triggers paint.
- Paint is often the most expensive part of the pixel pipeline; avoid it where you can.
- Reduce paint areas through layer promotion and orchestration of animations.

  .. code-block:: css 

    .moving-element {
      will-change: transform;
    }

    .moving-element {
      transform: translateZ(0);
    }

- Use the Chrome DevTools paint profiler to assess paint complexity and cost; reduce where you can.

Optimizing - Compositing  
*************************

There are two key factors in this area that affect page performance: 

  - the number of compositor layers that need to be managed
  - the properties that you use for animations.


- Stick to transform and opacity changes for your animations.

  Do not need Layout and Paint:

  Today there are only two properties for which that is true - :code:`transforms` and :code:`opacity` :

- Promote moving elements with :code:`will-change` or :code:`translateZ` .
- Avoid overusing promotion rules; layers require memory and management.

  Manage layers and avoid layer explosions

Debounce Your Input Handlers
*****************************

- Avoid long-running input handlers; they can block scrolling.
- Do not make style changes in input handlers.
- Debounce your handlers; store event values and deal with style changes in the next requestAnimationFrame callback.

  .. code-block:: bash 

    function onScroll (evt) {

      // Store the scroll value for laterz.
      lastScrollY = window.scrollY;

      // Prevent multiple rAF callbacks.
      if (scheduledAnimationFrame)
        return;

      scheduledAnimationFrame = true;
      requestAnimationFrame(readAndUpdatePage);
    }

    window.addEventListener('scroll', onScroll);

Reference
**********

https://developers.google.com/web/fundamentals/performance/rendering/