
HTML To PDF Solutions / HTML 转换 PDF 解决方案
##############################################

:date: 2019-01-10
:tags: phantomjs, wkhtmltopdf, PDF, HTML
:category: Tools
:slug: HTML_To_PDF_Solutions
:author: Brian Shen
:summary: HTML To PDF Solutions

.. _HTML_To_PDF_Solutions:

.. contents::

Intro / 简介
^^^^^^^^^^^^^

There are many situations that we need to generate reports in PDF. And there are many solutions.

- Use libraries to manipulate pdf content. That suffers. 
- Use html and then render it to PDF. That's wonderful.

I think everyone like the last solution since you can always have a preview.

And to render html to PDF, there are many solutions.
But the most popular ones are :code:`phantomjs` and :code:`wkhtmltopdf` .

I thought :code:`phantomjs` would be more popular if it's still under maintenance.
Unfortunately, it doesn't. So the lack of some necessary features makes :code:`wkhtmltopdf` an appearing alternative.

In my project, I used to generate PDF using :code:`phantomjs` . One day a customer asked for a menu.
And I found it unable to fulfill.
And then I began to use :code:`wkhtmltopdf` .

However, there are some problems both. And I'll explain.

很多情况下， 我们需要产生PDF的报告。 因此也有很多现存的解决方案：

- 可以使用 PDF 库 去操作PDF 的内容， 那会非常的痛苦
- 使用HTML 然后 渲染为PDF， 那会很好

我想每个人都改会喜欢后一种解决方案， 因为你永远可以有一个预览。

至于 将 HTML 转换为 PDF， 现在也有很多的解决方案。 最流行的就是 :code:`phantomjs` 和 :code:`wkhtmltopdf` 。

我想 :code:`phantomjs` 会更加的流行 如果 它还在被维护的话。 可惜的是，他被停止维护了。 一些基础必要功能的缺少使得 :code:`wkhtmltopdf` 称为很好的选择。

我曾使用 :code:`phantomjs` 产生 PDF，但是后来客户需要 一个 目录，:code:`phantomjs` 不具备这样的功能。因为我转向了 :code:`wkhtmltopdf` 。

Sample Files / 示例文件
^^^^^^^^^^^^^^^^^^^^^^^

To compare the render results of the two Scriptable Headless Browser. We will use the following samples.

为了对比渲染结果，我们使用以下的示例。

.. code-block:: bash 

    ./resources/
    ├── DailyReport.js
    ├── DailyReport1x.html
    ├── DailyReport3x.html
    ├── Report.css
    ├── echarts.common.min.js
    ├── jquery-1.12.4.min.js
    └── jquery-3.3.1.min.js

:code:`DailyReport1x.html` (We render a link and a chart / 我们渲染一个 连接 和 图表):

.. code-block:: bash 

    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <title>Daily Report</title>
    <link rel="stylesheet" href="Report.css">
    <script src="jquery-1.12.4.min.js"></script>
    <script src="echarts.common.min.js"></script>
    <script src="DailyReport.js"></script>
    </head>
    <body>
    <div class="page">
        <div>
        <h2>Menu</h2>
        <div class="chartDiv">
            <a href="#chartDiv">● Test Internal Link</a>
            <br />
        </div>
        </div>
    </div>
    <div class="page">
        <div style="height:100mm; width:180mm;" id="chartDiv">
        </div>
    </div>
    </body>
    </html>

:code:`DailyReport.js` :

.. code-block:: bash 

    function drawPie() {
      var chartOptions = {
        animation: false,
        xAxis: {
          type: 'category',
          data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        },
        yAxis: {
          type: 'value'
        },
        series: [{
          data: [820, 932, 901, 934, 1290, 1330, 1320],
          type: 'line'
        }]
      };
      var myChart = echarts.init(document.getElementById('chartDiv'));
      myChart.setOption(chartOptions);
    };
    $(document).ready(function() {
      drawPie();
    });


:code:`Report.css` :

.. code-block:: bash 

    @page {
      size: A4;
      margin: 0;
    }
    @media print {
      body {
        background: white;
      }
      .page {
        width: 210mm;
        page-break-after: always;
      }
    }
    html, body {
      background: rgb(241,241,241);
    }
    .page {
      page-break-after: always;
      width: 210mm;
      background: white;
    }


And preview in Chrome / 在Chrome 中预览:

.. figure::  /images/tools/htmltopdf01.png

Print Preview / Chrome 打印预览:

.. figure::  /images/tools/htmltopdf02.png


:code:`phantomjs`
^^^^^^^^^^^^^^^^^^^

Installation / 安装
*******************

Download from its `Phantomjs Official Site <http://phantomjs.org/download.html>`_ and move it to :code:`/usr/bin/` .

The latest and end version is :code:`2.1.1` .

从官网去下载，移动到 :code:`/usr/bin/`  . 最新也是最后的版本是 :code:`2.1.1`  .

Usage in JS / JS  调用
************************

We use :code:`html-pdf` because it is simple.

使用 :code:`html-pdf` ， 因为这样很简单。

:code:`npm install html-pdf`

.. code-block:: bash

    const fs = require('fs');
    const phantomjs = require('html-pdf');

    const SrcPath1x = 
      '/Users/BrianShen/Code/Asia/tset/Node/testPDF/resources/DailyReport1x.html';
    const BasePath = 
      'file:///Users/BrianShen/Code/Asia/tset/Node/testPDF/resources/';
    const OutPath = 'test.pdf';

    const genPDFPahntomJS = function(srcPath, basePath, outPath) {
      return new Promise( (resolve, reject) => {
        fs.readFile(srcPath, 'UTF8', function(errfs, html) {
          if (errfs) {
            reject(errfs);
            return;
          }
          const genOptions = {
            height: '297mm',
            width: '210mm',
            base: basePath,
            type: 'pdf',
            border: {
              top: '12mm', // default is 0, units: mm, cm, in, px
              right: '0',
              bottom: '0',
              left: '0',
            },
            paginationOffset: 1, // Override the initial pagination number
            footer: {
              height: '20mm',
              contents: {
                first: ' ',
                default:'{{page}}/{{pages}}',
              },
            },
          };
          phantomjs.create(html, genOptions).toFile(outPath, (err, res) => {
            if (err) {
              reject(err);
              return;
            }
            resolve(res);
          });
        });
      });
    }

    genPDFPahntomJS(SrcPath1x, BasePath, OutPath).then( () => {
      console.log('Success');
    }).catch( (err) => {
      console.log(err);
    })

let's see the result / 看看结果:

.. figure::  /images/tools/htmltopdf03.png

Very strange, isn't it?

:code:`phantomjs 2.1.1` has a very strange bug, that the size of printed page is only 75% as big as the standard page. For example, for A4 with 29.7*21. When we design our html, we can only use (29.7 * 0.75) * (21 * 0.75) .

And the fatal fault is that the internal hyperlink in the PDF cannot be clicked!

非常的奇怪。 :code:`phantomjs 2.1.1` 有一个非常奇怪的bug，大的A4 是平常 A4 的 75% 。 这就意味着你在设计html 的时候要按照75%的比例进行设计.

:code:`wkhtmltopdf`
^^^^^^^^^^^^^^^^^^^

Installation / 安装
********************

OK, still download from `wkhtmltopdf Official Site <https://wkhtmltopdf.org/downloads.html>`_  and install.

仍然从 官网下载并且安装 .

Usage in Command Line / 命令行使用
***********************************

Quite simple. I just like it because it is simple and easy to begin and test.

非常简单，能让你快速的开始。

.. code-block:: bash

  # wkhtmltopdf --debug-javascript --print-media-type --page-size A4 ./resources/DailyReport1x.html test.pdf
  Loading pages (1/6)
  Counting pages (2/6)                                               
  Resolving links (4/6)                                                       
  Loading headers and footers (5/6)                                           
  Printing pages (6/6)
  Done 

And let's see the result: / 看一看结果。

.. figure::  /images/tools/htmltopdf04.png

Everything works fine!

符合预期。

Usage in JS / JS 使用
**********************

I use :code:`wkhtmltopdf` as it is very popular.

我使用的是 :code:`wkhtmltopdf` 。

:code:`npm install wkhtmltopdf` 

.. code-block:: bash 

    const wkhtmltopdf = require('wkhtmltopdf');

    const SrcPath1x = 
      'file:///Users/BrianShen/Code/Asia/tset/Node/testPDF/resources/DailyReport1x.html';
    const OutPath = 
      './test1.pdf';

    const genPDFWkHtmlToPdf = function(srcPath, outPath) {
      return new Promise( (resolve, reject) => {
        wkhtmltopdf(srcPath, {
          output: outPath,
          printMediaType: true,
          footerLeft: '[page] / [toPage]',
        }, (err) => {
          if (err) {
            reject(err);
            return;
          }
          resolve();
        });
      });
    }

    genPDFWkHtmlToPdf(SrcPath1x, OutPath).then( () => {
      console.log('Success');
    }).catch( (err) => {
      console.log(err);
    }) 

The result / 结果:

.. figure::  /images/tools/htmltopdf05.png

It's as same as we rendered with command line!

Besides, the internal hyperlink works!

与 命令行中 渲染的结果是一样的。此外，内部的连接是可以使用的。

Other Tips / 其他
^^^^^^^^^^^^^^^^^

Charts can be partial / 图表显示不全
************************************

ECharts will use animation by default, so disable it.

ECharts 会自动的开启 动画效果。会导致延时。关闭即可。

:code:`animation: false,`

jQuery 3.3.1 is not fully compatible with wkhtmltopdf 
******************************************************

jQuery 3.3.1 与 wkhtmltopdf 不兼容。

Let's see a sample:

看个例子。

.. code-block:: bash 

    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>Daily Report</title>
      <link rel="stylesheet" href="Report.css">
      <script src="jquery-3.3.1.min.js"></script>
    </head>
    <body>
      <div class="page">
        <div>
          <h2>Menu</h2>
          <div class="chartDiv">
            <a href="#chartDiv">● Test Internal Link</a>
            <br />
          </div>
        </div>
        <div>
          <table id="tableDiv">
            <tr><td>Test</td><td>Title</td></tr>
          </table>
        </div>
      </div>
    </body>
    <script>
      $(document).ready(function(){
        $('#tableDiv').append('<tr><td>Row1</td><td>Row1</td></tr>');
      })
    </script>
    </html>

When we open it in Chrome:

从Chrome 中打开。

.. figure::  /images/tools/htmltopdf06.png

And render it with :code:`wkhtmltopdf` :

使用 :code:`wkhtmltopdf` 去渲染。

.. code-block:: bash 

    #wkhtmltopdf --debug-javascript --print-media-type --page-size A4 --footer-left "Page [page] of [toPage]" ./resources/DailyReport3x.html test.pdf
    Loading pages (1/6)
    Warning: file:///Users/BrianShen/Code/Asia/tset/Node/testPDF/resources/jquery-3.3.1.min.js:2 jQuery.Deferred exception: 'undefined' is not a function
    Warning: undefined:0 TypeError: 'undefined' is not a function
    Counting pages (2/6)
    Resolving links (4/6)                                                       
    Loading headers and footers (5/6)                                           
    Printing pages (6/6)
    Done

It can't work.

But when we switch to 1.12.4 and render it, everything works fine.

发生了错误。但是我们切换到 1.12.4 的 jQuery， 一切工作正常。

.. figure::  /images/tools/htmltopdf05.png

Sad thing is that jQuery 1.12.4 is not under maintenance anymore.

遗憾的是，jQuery 1.12.4 不在维护了。
