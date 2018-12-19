Sphinx And RST 
###############


:date: 2017-11-08
:tags: Sphinx, RST
:category: Tools
:slug: Sphinx_And_RST
:author: Brian Shen
:summary: Sphinx And RST 

.. contents::

.. _sphinx_AND_RST_:

What is :code:`Sphinx` / 什么是 :code:`Sphinx`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Reference : `Official Page <http://www.sphinx-doc.org/en/stable/>`_

Sphinx is a tool that makes it easy to create intelligent and beautiful documentation.

Sphinx 可以让你轻松地创建只能而漂亮的文档。

How to install :code:`Sphinx` / 怎么安装
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Prerequisite / 前提:

- Python
- Pip

Open cmd and execute:  / 打开命令行执行： 
    :code:`pip install sphinx`
Usually, most people use a theme named :code:`rtd` , so install this theme: / 我们通常看到的主题的名字叫 :code:`rtd` ，可以这样安装：
    :code:`pip install sphinx_rtd_theme`

Create a folder, then run command: / 新建文件夹 并且运行命令：
    :code:`sphinx-quickstart` 。

After input some essential information, :code:`sphinx` has created some files.

再输入一些必要的信息之后， :code:`sphinx` 以及自动的为你创建了一些文件。

.. figure::  /images/tools/sphinx_02.png

.. code-block:: bash

    Sphinx
    ├── _build          # output
    ├── _static         # resource, like pictures and files
    ├── _templates      # ignore
    ├── conf.py         # Sphinx configuration file
    ├── index.rst       # entry
    ├── make.bat        # Window make file
    ├── Makefile        # Linux make file

:code:`index.rst` is the entry file, :code:`sphinx` will use this file and include other files mentioned in it.

:code:`index.rst` 是主入口文件，:code:`sphinx` 创建的 文档会包含其中的所有的其他链接文件。

Modify the configuration file :code:`conf.py` / 修改配置文件：

.. code-block:: bash

    # sys.path.insert(0, os.path.abspath('.'))
    import sphinx_rtd_theme

    # html_theme = 'alabaster'
    html_theme = 'sphinx_rtd_theme'

Now run :code:`.\make.bat html` , it will automatically turn :code:`rst` into :code:`html` .

现在，可以运行 :code:`.\make.bat html` ，这将会自动的将 :code:`rst` 转换为 :code:`html` 文件。

.. code-block:: bash

    Sphinx
    ├── _build
    │   ├── html
    │   │    ├── index.html (Open this)
    ├── _static
    ├── _templates
    ├── conf.py
    ├── index.rst
    ├── make.bat
    ├── Makefile

.. figure::  /images/tools/sphinx_03.png

Best Practice / 最佳实践
^^^^^^^^^^^^^^^^^^^^^^^^^^

No matter we use :code:`Sphinx` for personal documents or for team projects documents, there will be a lot of documents. So, how to organize them?

无论是用 :code:`Sphinx` 来记录个人文档 还是 团队文档，毫无疑问都会慢慢积累大量的文档，所以，如何去组织他们呢？

- Create a folder named :code:`_content` for original documents, and include them in the main entry file :code:`index.rst` .

创建一个文件夹，叫 :code:`_content` 来存放原始的 rst 文件，并且 将需要的文档包括进 :code:`index.rst` 。

The content of :code:`index.rst` .

.. code-block:: bash

    Welcome to my documentation!
    ==============================

    .. toctree::
    :maxdepth: 2
           :caption: Contents:

           ./_content/content_one.rst
           ./_content/content_two.rst

The content of :code:`content_one.rst` / :code:`content_one.rst` 的内容：

.. code-block:: bash

    Sphinx Content one
    ##################

    RST Language one
    ^^^^^^^^^^^^^^^^

    Header Sample One
    *****************

Compile and open in chrome: / 编译并且在 浏览器中打开：

.. figure::  /images/tools/sphinx_04.png

If we need numbers, add :code:`:numbered:` in :code:`index.rst` .
如果我们需要序号的话，可以加上 :code:`:numbered:`  标志。

.. code-block:: bash

    .. toctree::
       :maxdepth: 2
       :numbered:
       :caption: Contents:

Compile and open in chrome。 / 编译再次在浏览器中打开即可。

- Multi Projects / 多个工程

If we have two or projects, then how to organize?

如果我们有多个工程的话，那么怎么组织文件结构呢？

.. code-block:: bash

    index.rst
    content/
    ├── Node
    │   ├── NodeIndex.rst
    │   └── Node_Scheduler.rst
    ├── Tools
    │   ├── ToolIndex.rst
    │   ├── Tools_DiskMount.rst
    │   ├── Tools_LocalYumRepo.rst
    │   └── Tools_PDFToWord.rst
    └── images
        └── tools
            ├── local_repo_01.png
            ├── local_repo_02.png
            ├── mount_disk_01.png
            └── pdf_to_word_01.png


The content of :code:`index.rst` .

.. code-block:: bash

    Welcome to my documentation!
    ==============================

    .. toctree::
    :maxdepth: 2
           :caption: Contents:

           ./_content/Tools/ToolsIndex.rst
           ./_content/Node/NodeIndex.rst


The content of :code:`ToolsIndex.rst` :

.. code-block:: bash

    Project Tools
    ==============

    .. toctree::
    :maxdepth: 2
           :caption: Contents:

           ./Tools_DiskMount.rst
           ./Tools_LocalYumRepo.rst
           ./Tools_PDFToWord.rst

In this way, every folder can become a project and the main entry :code:`index.rst` doesn't need to care about the structure of sub directory.. 

这样的结构， 每一个文件夹就是一个工程，并且 顶层 不需要关心 子目录的结构。

RST Language / RST 语言简介
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Reference : `RST reference <http://www.sphinx-doc.org/en/stable/rest.html#internal-links>`_

Section / 章节
***************

.. code-block:: bash

    # Header
    Sphinx Introduction
    ###################

    # Sub Header
    RST Language
    ^^^^^^^^^^^^

    # Small Header
    Header Sample
    *************

Although official suggestion is the following, but use the previous one, it is compatible with many platforms.

虽然官方推荐是以下的标志，但是还是推荐上面的格式，因为兼容性更好。

.. code-block:: bash

    # with overline, for parts
    * with overline, for chapters
    =, for sections
    -, for subsections
    ^, for subsubsections
    ", for paragraphs


Words Style / 样式
**********************

- emphasis – alternate spelling for *emphasis*
- strong – alternate spelling for **strong**
- literal – alternate spelling for ``literal``
- subscript – subscript text
- superscript – superscript text
- title-reference – for titles of books, periodicals, and other materials

.. code-block:: bash

    *emphasis* , **strong**,  ``literal``

Sample / 示例 :

    *emphasis* , **strong**,  ``literal``

List / 清单
************

    .. code-block:: bash

        * This is a bulleted list.
        * It has two items, the second
          item uses two lines.

        1. This is a numbered list.
        2. It has two items too.

        #. This is a numbered list.
        #. It has two items too.


Sample / 示例:

    * This is a bulleted list.
    * It has two items, the second
      item uses two lines.

    1. This is a numbered list.
    2. It has two items too.

    #. This is a numbered list.
    #. It has two items too.


Reference Link / 参考链接 
*****************************

.. _sphinx-external:

- External Link / 外部链接

    .. code-block:: bash

        `Official Page <http://www.sphinx-doc.org/en/stable/>`_

    Sample / 样例:

        `Official Page <http://www.sphinx-doc.org/en/stable/>`_


- Internal Link / 内部链接

    Add a link flag in document. / 在文档中添加一个连接标志

    .. code-block:: bash

        .. _sphinx-external:

        - External Link

    To use this link: / 使用它： 

    .. code-block:: bash

        :ref:`Go to External <sphinx-external>`

    Sample / 示例(Fail in pelican)


Codes / 代码段
****************

- Simple Code / 示例代码

    .. code-block:: bash

        This is an introduction to :code:`Sphinx`

    Sample / 示例:
        This is an introduction to :code:`Sphinx`

- Doc tree / 文档树

    .. code-block:: bash

        .. code-block:: bash

            storage_env
            ├── config
            ├── storage
            │   ├── provision  (provision core codes)
            │   │    ├── salesforce_provision.py
            │   │    ├── salesforce_sandbox_provision.py
            │   │    ├── salesforce_production_provision.py
            │   │    └── salesforce_utils

    Sample / 示例:

    .. code-block:: bash

        storage_env
        ├── config
        ├── storage
        │   ├── provision  (provision core codes)
        │   │    ├── salesforce_provision.py
        │   │    ├── salesforce_sandbox_provision.py
        │   │    ├── salesforce_production_provision.py
        │   │    └── salesforce_utils

- Javascript / JS 代码

    .. code-block:: bash

        .. code-block:: javascript

            console.log("Sphinx");

    Sample / 示例:

    .. code-block:: javascript

        console.log("Sphinx");


Pictures / 图片
****************


.. code-block:: bash

    .. figure::  /images/tools/sphinx_01.png

Sample / 示例:

     .. figure::  /images/tools/sphinx_01.png

Tables / 表格
**************

.. code-block:: bash

    .. list-table::
        :widths: 25 25 50
        :header-rows: 1

        * - Heading row 1, column 1
          - Heading row 1, column 2
          - Heading row 1, column 3
        * - Row 1, column 1
          -
          - Row 1, column 3
        * - Row 2, column 1
          - Row 2, column 2
          - Row 2, column 3
 
- Sample / 示例 

.. list-table::
    :widths: 25 25 50
    :header-rows: 1

    * - Heading row 1, column 1
      - Heading row 1, column 2
      - Heading row 1, column 3
    * - Row 1, column 1
      -
      - Row 1, column 3
    * - Row 2, column 1
      - Row 2, column 2
      - Row 2, column 3


Enjoy!