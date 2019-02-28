Web Security 08 - Sniff
#########################################

:date: 2019-02-28
:tags: Security, Web, MIME Sniff, Web Security
:category: Security
:slug: Web_Security_07_MIME_Sniff
:author: Brian Shen
:summary: Web Security 08 - MIME Sniff

.. _Web_Security_07_MIME_Sniff:

.. contents::

All the sample code is in https://github.com/brianshen1990/WebSecurity .


What is MIME Type
********************

A Multipurpose Internet Mail Extensions (MIME) type is a standard that indicates the nature and format of a document, file, or assortment of bytes.


Browsers use the MIME type, not the file extension, to determine how to process a URL, so it's important that web servers send the correct MIME type in the response's Content-Type header. If this is not correctly configured, browsers are likely to misinterpret the contents of files and sites will not work correctly, and downloaded files may be mishandled.

General Types:

- applicationList (application/octet-stream, application/pdf, application/pkcs8, and application/zip)
- audio (audio/mpeg, audio/vorbis)
- font (font/woff, font/ttf, and font/otf)
- image (image/jpeg, image/png, image/gif, and image/svg+xml)
- model (model/3mf and model/vml)
- text (text/html, text/plain, text/html, text/javascript, text/css)
- video (video/mp4)


What's MIME sniffing
*********************

In the absence of a MIME type, or in certain cases where browsers believe they are incorrect, browsers may perform MIME sniffing — guessing the correct MIME type by looking at the bytes of the resource.

Each browser performs MIME sniffing differently and under different circumstances. (For example, Safari will look at the file extension in the URL if the sent MIME type is unsuitable.) There are security concerns as some MIME types represent executable content. Servers can prevent MIME sniffing by sending the X-Content-Type-Options header.

Sample
*******

Let's see what happened in our blog system:

.. figure:: /images/security/WebSecurity23.png

.. warning::

    If a file is cached in our browser, then we cannot see the content type in DevTools.

Let's modifying our system ( :code:`index.html` ): 

.. code-block:: html 

    <script src="./userImage.txt" ></script>

:code:`userImage.txt` :

.. code-block:: javascript 
  
    alert('I take over the browser!');

And run our system:

.. code-block:: bash 

    node index.js 

It seems that the :code:`txt` plain file is being executed! 

.. figure:: /images/security/WebSecurity24.png

What if our system allows users to upload txt file types, and some bad guys upload a txt file full of scripts, and in the blog content, they somehow import this scripts, then XSS attack can be happened. 

How to fix 
***********

1. Stop browser performing MIME sniffing
2. Send the correct MIME Type 

Now let's build a safe website :code:`indexSafe.js` :

.. code-block:: javascript 

    // ...
    app.use(helmet.noSniff());
    // ...

And run our system:

.. code-block:: bash 

    node indexSafe.js 

.. figure:: /images/security/WebSecurity25.png

The plain txt file won't be executed any more.

https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types