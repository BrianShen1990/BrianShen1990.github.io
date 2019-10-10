Sed and Find
#############


:date: 2019-10-08
:tags: Linux, CentOS6, CentOS7
:category: Tools
:slug: Tools_Sed_Find
:author: Brian Shen
:summary: Tools Sed and Find

.. _Tools_Sed_Find.rst:


Sed and Find are both tiny but wonderful tools.


Sed 
^^^^^

Give sample using this file :code:`sample.txt` .

content:

.. code-block:: bash 

  Line1 hello
  Line2 
  Line3
  Line4

:code:`sed -i` means taking modification back to the file.

Find and Append 
****************

:code:`sed 'N;/Line2/a\Line2.1' sample.txt`

.. code-block:: bash 

  Line1 hello
  Line2 
  Line2.1
  Line3
  Line4

Append at the end 
******************

:code:`sed '$a\LastLine' sample.txt`

.. code-block:: bash 

  Line1 hello
  Line2 
  Line3
  Line4
  LastLine

Search and Delete
******************

:code:`sed '/Line2/'d sample.txt`

.. code-block:: bash

  Line1 hello
  Line3
  Line4

Delete line
*************

:code:`sed '3d' sample.txt`  

delete line 3

.. code-block:: bash

  Line1 hello
  Line2 
  Line4

Replace
********

:code:`sed 's/Line/line/g' sample.txt`

.. code-block:: bash

  line1 hello
  line2 
  line3
  line4

Insert
*******

:code:`sed '2iLine2.1' sample.txt`

Inserts at line 2 :code:`Line2.1` .

.. code-block:: bash

  Line1 hello
  Line2.1
  Line2 
  Line3
  Line4

Find
^^^^

.. code-block:: bash 

  ls -al
  total 1860416
  dr-xr-x---.  5 root    root         4096 Oct 10 20:33 .
  dr-xr-xr-x. 18 root    root         4096 Aug  2 07:48 ..
  -rw-------.  1 root    root         1549 Jul 21  2018 anaconda-ks.cfg
  -rw-r--r--.  1 root    root        69856 Aug 19 15:35 kkk.txt
  -rw-r--r--.  1 root    root           31 Oct 10 20:33 sample.txt
  -rw-r--r--.  1 root    root         1120 Sep 19 12:05 tda.sh
  -rw-r--r--.  1 tcpdump tcpdump     18997 Sep 19 12:31 test5.pcap
  -rw-r--r--.  1 tcpdump tcpdump     18222 Sep 19 12:33 test6.pcap
  -rw-r--r--.  1 tcpdump tcpdump    969225 Sep 19 12:50 test7.pcap
  -rw-r--r--.  1 tcpdump tcpdump     29300 Sep 19 12:55 test8.pcap
  -rw-r--r--.  1 tcpdump tcpdump     21058 Sep 19 13:31 test9.pcap
  -rw-r--r--.  1 root    root           48 Aug 20 19:51 tst.sh


File 
*****

.. code-block:: bash

  .
  |-- nest
  |   |-- ss.txt
  |-- sample.txt

:code:`find ./ -name ss.txt`

.. code-block:: bash

  ./nest/ss.txt


:code:`find ./ -type f -size +1M`


Content
*******

:code:`grep -R "Line" ./`

.. code-block:: bash 

  ./nest/ss.txt:Line1 hello
  ./nest/ss.txt:Line2 
  ./nest/ss.txt:Line3
  ./nest/ss.txt:Line4
  ./sample.txt:Line1 hello
  ./sample.txt:Line2 
  ./sample.txt:Line3
  ./sample.txt:Line4

OR: 


:code:`find ./ -type f -exec cat {} + | grep Line2`

.. code-block:: bash

  Line2 
  Line2 
