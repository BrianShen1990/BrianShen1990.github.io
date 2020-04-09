Webpack Optimization
##########################


:date: 2020-04-09
:tags: Node
:category: Node
:slug: Node_Webpack_Optimization
:author: Brian Shen
:summary: Node_Webpack_Optimization

.. _Node_Webpack_Optimization_rst:

.. contents::

We always want to split our code, makes it light ans stable enough for Browser to load and cache.

With default webpack configuration, all js code will be bundled into 1 single file, which usually will be >=4 MB.

How could we change adn optimized it then?


Use :code:`splitChunks`
^^^^^^^^^^^^^^^^^^^^^^^^

If you know your depending modules:

.. code-block:: javascript 

  {
    mode: 'production',
    /** optimization for chunks */
    optimization: {
      splitChunks: {
        chunks: 'all',
        cacheGroups: {
          react: {
            test: /[\\/]node_modules[\\/](react|react-dom|react-router-dom)[\\/]/,
            name: 'react',
            chunks: 'all',
          },
          react_assist: {
            test: /[\\/]node_modules[\\/](react-toastify|react-paginate|react-dropzone)[\\/]/,
            name: 'react_assist',
            chunks: 'all',
          },
          css_bootstrap: {
            test: /[\\/]node_modules[\\/](bootstrap|reactstrap|@fortawesome\/fontawesome-free)[\\/]/,
            name: 'css_bootstrap',
            chunks: 'all',
          },
          tools: {
            test: /[\\/]node_modules[\\/](axios|moment)[\\/]/,
            name: 'tools',
            chunks: 'all',
          },
        }
      }
    }
  }

Let's compare the file size and how browser can handle this.


Before optimization:

.. figure:: /images/node/webpack_opt_02.png

After optimization: 

.. figure:: /images/node/webpack_opt_01.png

.. list-table:: 
   :widths: 30 35 35
   :header-rows: 1

   * - Period
     - Before
     - After
   * - Resource
     - 9.5M 
     - 2.4M
   * - Finish
     - 1.22s
     - 662ms


Use React Lazy and Suspense
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Only for example.

.. figure:: /images/node/webpack_opt_03.png

