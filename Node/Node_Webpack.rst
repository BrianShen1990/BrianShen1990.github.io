Node Webpack
###############


:date: 2018-12-18
:tags: Node
:category: Node
:slug: Node_Webpack
:author: Brian Shen
:summary: Node Webpack

.. _node_webpack_rst:

.. contents::

Basic Usage of Webpack.  / Webpack 的简单使用。

Asset Management 资产管理
^^^^^^^^^^^^^^^^^^^^^^^^^^

Mainly how to manipulate rules to support them.

主要是如何通过配置规则 来 支持各种文件资产类型。

.. code-block:: bash 

    module: {
      rules: [
        {
          test: /\.css$/,
          use: [
            'style-loader',
            'css-loader',
          ]
        }, 
        {
          test: /\.(png|svg|jpg|gif)$/,
          use: [
            'file-loader',
          ],
        },
      ],


Output Management / 输出管理
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Mainly :code:`Entry` and :code:`Output` .

主要是 入口点 和 输出。

.. code-block:: bash 

    entry: {
      index: './src/index.js',
    },
    output: {
      filename: '[name].[hash].js',
      chunkFilename: '[name].[hash].js',
      path: path.resolve(__dirname, 'dist')
    },

And clear dist by :code:`CleanWebpackPlugin` :
如果想要清除目标文件夹中的文件，使用插件 :code:`CleanWebpackPlugin` 。

.. code-block:: bash
    
    const CleanWebpackPlugin = require('clean-webpack-plugin');

    plugins: [
      new CleanWebpackPlugin(['dist']),

And generate html :code:`index.html` automatically。 

如果想要自动的产生 :code:`index.html` 。

.. code-block:: bash

    const CleanWebpackPlugin = require('clean-webpack-plugin');

    new HtmlWebpackPlugin({
      title: 'Output01'
    }),

Development / 友好开发
^^^^^^^^^^^^^^^^^^^^^^^

Add source map to debug in UI:
在 UI 中加入 source map 以便调试。

.. code-block:: bash

    devtool: 'inline-source-map',

And :code:`webpack-dev-server` :
开发是也可以使用 :code:`webpack-dev-server` 来启动本地服务器。

.. code-block:: bash

    devServer: {
      contentBase: './dist',
      hot: true,
    },

Hot Module Replacement / 热模块加载
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Advanced Feature.
Haven't used it yet.

Tree Shaking
^^^^^^^^^^^^^^^

- Remove unnecessary modules of code for ES2015

Add :code:`sideEffects` to indicate which files are pure ES2015 MODULES.

主要是用来移除不必要的模块。
将那些单纯的ES2015的代码，整理到 :code:`sideEffects` tag 下。


- Minify the Output (Uglify)

  最小化代码。

.. code-block:: bash
    
    mode: 'production'

Production / 生产环境
^^^^^^^^^^^^^^^^^^^^^

Use :code:`webpack-merge` and 

使用   :code:`webpack-merge` 模块，

.. code-block:: bash

    webpack.common.js
    webpack.dev.js
    webpack.prod.js

so that we can have different configurations in different environment.
Also meed to update npm scripts as well. 

这样的话，开发 和 部署环境会有不同的配置。 当然我们也需要在 npm 代码中进行相应的修改。

source mapping in production: :code:`devtool: 'source-map'` .

source mapping 永远是被推荐的，即使是在生产环境中。

Code Splitting / 代码分割
^^^^^^^^^^^^^^^^^^^^^^^^^^

- Multi Entries / 多入口点

  Multi Entries will split code but will also cause Duplication.

  即使定义了多个入口点，编译出来的单独的文件 是互相隔离的，会导致重复代码。

- Prevent Duplication / 避免重复代码。

  .. code-block:: bash 

      optimization: {
        splitChunks: {
          chunks: 'all'
        }
      }

- Dynamic Imports / 动态加载

  Instead of using optimization, we use 
  
  与 优化不同，这边会将所有的依赖打包成单个文件。

  .. code-block:: bash 

      output: {
        filename: '[name].bundle.js',
        chunkFilename: '[name].bundle.js',
        path: path.resolve(__dirname, 'dist')
      },

  and use dynamic imports. A little unfriendly for developers.

  并且动态的加载。 对开发还是有些不利的。

  .. code-block:: bash

      const { default: _ } = await import(/* webpackChunkName: "lodash" */ 'lodash');
      element.innerHTML = _.join(['Hello', 'webpack'], ' ');  

- Prefetching/Preloading modules 

  预先加载代码的话，直接使用 import 就可以了。

  Using import.

Lazy Loading / 懒加载
^^^^^^^^^^^^^^^^^^^^^^^

More complex and is very unfriend to developers.

更加的复杂， 对开发也不是很友好。

Dynamic load during events like click.

懒加载 就是， 直到某个事件发生了， 要去使用一个资源，我们再去动态的加载。

However, there are some frameworks: / 针对不同前端库，其实有自己的一些框架。

  https://reacttraining.com/react-router/web/guides/code-splitting


Caching / 缓存
^^^^^^^^^^^^^^^^^^

Add hash to name so that whenever a file updates, the name will change as well.

在文件名中加上 hash 值，这样的话 文件只要有变动，名字也会跟着改变。

.. code-block:: bash

    output: {
      filename: '[name].[hash].js',
      chunkFilename: '[name].[hash].js',
      path: path.resolve(__dirname, 'dist')
    },

Combine vendors in node_modules.
可以将 node_modules 文件夹中不变的内容 都让在一个 文件里面， 因为他们是不变动的。

.. code-block:: bash 

    optimization: {
      usedExports: true,
      runtimeChunk: 'single',
      splitChunks: {
        cacheGroups: {
          vendor: {
            test: /[\\/]node_modules[\\/]/,
            name: 'vendors',
            chunks: 'all',
          },
        },
      },
    },

However, we need to use plugins as each :code:`module.id`  is incremented based on resolving order by default.

当然，我们需要记住 一个插件，否则 每一次  :code:`module.id` 都会改变。

.. code-block:: bash 

    plugins: [
      new webpack.HashedModuleIdsPlugin(),


Authoring Libraries
^^^^^^^^^^^^^^^^^^^^

创建一个 库。

use library and library and externals. 

需要借助 library 和 externals 标签。

TODO

Shimming
^^^^^^^^^

Not recommended!  / 不推荐

- Shimming Globals / 全局变量

.. code-block:: bash 

    plugins: [
      new webpack.ProvidePlugin({
      _: 'lodash'
      }),

- Global Exports / 全局导出

Very useful for dated libs.

当我们使用 一个过时的库时，会很实用。

.. code-block:: bash 

    src/globals.js

    var file = 'blah.txt';
    var helpers = {
      test: function() { console.log('test something'); },
      parse: function() { console.log('parse something'); }
    };

What can we do about that?

我们如何去使用这个库？

.. code-block:: bash 

    module: {
      rules: [
        {
          test: require.resolve('index.js'),
          use: 'imports-loader?this=>window'
        }
        },
        {
          test: require.resolve('globals.js'),
          use: 'exports-loader?file,parse=helpers.parse'
        }
      ]
    }

And now we can use :code:`import { file, parse } from './globals.js';` .

现在我们可以使用  :code:`import { file, parse } from './globals.js';`  。


Progressive Web Application / 渐进式Web应用
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A Service Worker ran at background, quite amazing.

Type Script
^^^^^^^^^^^^^

Need a :code:`tsconfig.json` .

需要额外的 配置文件 :code:`tsconfig.json` 。

.. code-block:: bash

    {
      "compilerOptions": {
        "outDir": "./dist/",
        "sourceMap": true,
        "noImplicitAny": true,
        "module": "es6",
        "target": "es5",
        "jsx": "react",
        "allowJs": true
      }
    }

And add this / 并且添加上 规则:

.. code-block:: bash 

    module: {
      rules: [
        {
          test: /\.tsx?$/,
          use: 'ts-loader',
          exclude: /node_modules/
        }
      ]
    },
    resolve: {
      extensions: [ '.tsx', '.ts', '.js' ]
    },


Sample / 示例
^^^^^^^^^^^^^^^

webpack.common.js 
********************

.. code-block:: bash 

    const path = require('path');
    const HtmlWebpackPlugin = require('html-webpack-plugin');
    const CleanWebpackPlugin = require('clean-webpack-plugin');
    const webpack = require('webpack');

    module.exports = {
      entry: {
        index: './src/index.js',
      },
      plugins: [
        new CleanWebpackPlugin(['dist']),
        new HtmlWebpackPlugin({
          title: 'Output01'
        }),
        new webpack.HashedModuleIdsPlugin(),
        new webpack.HotModuleReplacementPlugin(),
        new webpack.ProvidePlugin({
          _: 'lodash'
        }),
      ],
      output: {
        filename: '[name].[hash].js',
        chunkFilename: '[name].[hash].js',
        path: path.resolve(__dirname, 'dist')
      },
      module: {
        rules: [
          {
            test: /\.tsx?$/,
            use: 'ts-loader',
            exclude: /node_modules/
          },
          {
            test: /\.css$/,
            use: [
              'style-loader',
              'css-loader',
            ]
          }, 
          {
            test: /\.(png|svg|jpg|gif)$/,
            use: [
              'file-loader',
            ],
          },
          {
            test: /\.(woff|woff2|eot|ttf|otf)$/,
            use: [
              'file-loader'
            ],
          },
        ],
      },
      resolve: {
        extensions: [ '.tsx', '.ts', '.js' ]
      },
    };


webpack.dev.js 
********************

.. code-block:: bash 

    const merge = require('webpack-merge');
    const common = require('./webpack.common.js');

    module.exports = merge(common, {
      // mode: 'production',
      mode: 'development',
      devtool: 'inline-source-map',
      devServer: {
        contentBase: './dist',
        hot: true,
      },
    });

webpack.prod.js 
********************

.. code-block:: bash 

    const merge = require('webpack-merge');
    const common = require('./webpack.common.js');

    module.exports = merge(common, {
      mode: 'production',
      devtool: 'source-map',
      optimization: {
        usedExports: true,
        runtimeChunk: 'single',
        splitChunks: {
          cacheGroups: {
            vendor: {
              test: /[\\/]node_modules[\\/]/,
              name: 'vendors',
              chunks: 'all',
            },
          },
        },
      },
    });


package.json
********************

.. code-block:: bash 

    {
      "name": "webpack-demo",
      "version": "1.0.0",
      "description": "",
      "private": true,
      "scripts": {
        "test": "echo \"Error: no test specified\" && exit 1",
        "build": "webpack --config webpack.prod.js",
        "watch": "webpack --watch",
        "startHttp": "http-server dist",
        "start": "webpack-dev-server --open --config webpack.dev.js"
      },
      "keywords": [],
      "author": "",
      "license": "ISC",
      "devDependencies": {
        "clean-webpack-plugin": "^1.0.0",
        "css-loader": "^2.0.1",
        "express": "^4.16.4",
        "file-loader": "^2.0.0",
        "html-webpack-plugin": "^3.2.0",
        "http-server": "^0.11.1",
        "style-loader": "^0.23.1",
        "ts-loader": "^5.3.1",
        "typescript": "^3.2.2",
        "webpack": "^4.27.1",
        "webpack-cli": "^3.1.2",
        "webpack-dev-middleware": "^3.4.0",
        "webpack-dev-server": "^3.1.10",
        "webpack-merge": "^4.1.5",
        "workbox-webpack-plugin": "^3.6.3"
      },
      "dependencies": {
        "lodash": "^4.17.11"
      },
      "sideEffects": false
    }

tsconfig.json 
****************

.. code-block:: bash 

    {
      "compilerOptions": {
        "outDir": "./dist/",
        "sourceMap": true,
        "noImplicitAny": true,
        "module": "es6",
        "target": "es5",
        "jsx": "react",
        "allowJs": true
      }
    }

