TCP and TLS Handshaking
########################

:date: 2019-03-05
:tags: TCP, TLS, Handshaking
:category: Tools
:author: Brian Shen
:slug: TCP_and_TLS_Handshaking
:summary: TCP and TLS Handshaking

.. TCP_and_TLS_Handshaking:

.. contents::

Intro 
^^^^^^

I have a customer and they have a client which connects to our provided server. While others can connect to the server seamlessly, this client cannot connect in any way.

So I told them to make sure that their client can ping, telnet and openssl to the server.
Everything seems OK. So it is time for me to take responsibility. 

I collected the client debug logs and reviewed the sever side debug logs. I found that client's logs suggested that :code:`An existing connection was forcibly closed by the remote host` , and the error number is :code:`10054` . 
In the server side, the debug logs showed that a connection is broken.

I searched in the Internet and found that there are many reasons for this error: 

- You are sending malformed data to the application
- The network link between the client and server is going down for some reason
- You have triggered a bug in the third-party application that caused it to crash
- The third-party application has exhausted system resources

However, I don't think any of these cause my situation because all things seemed work OK.

In the end, I had to seek help from lower layer information. I used TCPDUMP to collection some information. 
Luckily, after comparing the broken connection and correct ones, I found something quite strange.

Usually, after three steps' handshaking, a client will send a client hello to the server, like this:

.. code-block:: bash 

    Client -> Server [SYN]
    Client <- Server [SYN, ACK]
    Client -> Server [ACK]
    Client -> Server [PSH, ACK] (sends SSL Client Hello)

But for the broken ones, client will send [RST ACK] after the basic three steps' handshaking.

.. code-block:: bash 

    Client -> Server [SYN]
    Client <- Server [SYN, ACK]
    Client -> Server [ACK]
    Client -> Server [RST, ACK]  (connection closes)
    
Quite strange. Most situations in the internet are like this: :code:`the connection is closed or reseted by the server` . So when a client chose to close the connection, it is quite abnormal.

I seek help from my network colleagues. And she suggested me that, from the :code:`pcap` file, it shows that the TCP connection is OK, but when it comes to application protocol, it gets wrong. There maybe some security policy in the client side, for example, URL blocking. So when the three steps' handshaking is been done, the connection will be closed immediately.  

I verified it by putting a URL blocking device in front or the client, and the connection is reseted after handshaking, that's wonderful! 

So next I will have some notes about what happens during TCP and TLS handshaking.

TCP handshaking 
^^^^^^^^^^^^^^^^

Quite simple:

.. code-block:: bash 

    Client -> Server [SYN X]
    Client <- Server [SYN Y, ACK X+1]
    Client -> Server [ACK Y+1]

1. The first host (Client) sends the second host (Server) a "synchronize" (SYN) message with its own sequence number x, which Server receives.
2. Server replies with a synchronize-acknowledgment (SYN-ACK) message with its own sequence number y and acknowledgement number x+1, which Client receives.
3. Client replies with an acknowledgment (ACK) message with acknowledgement number y+1, which Server receives and to which he doesn't need to reply.

.. figure:: /images/web/handshaking01.png


TLS handshaking 
^^^^^^^^^^^^^^^^

TLS is an application layer protocol, it is beyond TCP. So everything related to TLS are happened after basic TCP handshaking. 

Basic TLS handshake
********************

.. code-block:: bash 
    
    Client -> Server [Client Hello]
    Client <- Server [Server Hello]
    Client <- Server [Certificate]
    Client <- Server [ServerKeyExchange]
    Client <- Server [ServerHelloDone]
    Client -> Server [ClientKeyExchange]

    Client -> Server [ChangeCipherSpec]

    Client <- Server [ChangeCipherSpec]

    Client <-> Server [Application]

1. Negotiation phase:

  - A client sends a ClientHello message specifying **the highest TLS protocol version it supports, a random number, a list of suggested cipher suites and suggested compression methods** . If the client is attempting to perform a resumed handshake, it may send a session ID. If the client can use Application-Layer Protocol Negotiation, it may include a list of supported application protocols, such as HTTP/2.
  - The server responds with a ServerHello message, containing **the chosen protocol version, a random number, CipherSuite and compression method from the choices offered by the client** . To confirm or allow resumed handshakes the server may send a session ID. The chosen protocol version should be the highest that both the client and server support. For example, if the client supports TLS version 1.1 and the server supports version 1.2, version 1.1 should be selected; version 1.2 should not be selected.
  - The server sends its Certificate message (depending on the selected cipher suite, this may be omitted by the server).
  - The server sends its ServerKeyExchange message (depending on the selected cipher suite, this may be omitted by the server). This message is sent for all DHE and DH_anon ciphersuites.
  - The server sends a ServerHelloDone message, indicating it is done with handshake negotiation.
  - The client responds with a ClientKeyExchange message, which may contain a PreMasterSecret, public key, or nothing. (Again, this depends on the selected cipher.) This PreMasterSecret is encrypted using the public key of the server certificate.
  - The client and server then **use the random numbers and PreMasterSecret to compute a common secret** , called the "master secret". All other key data for this connection is derived from this master secret (and the client- and server-generated random values), which is passed through a carefully designed pseudorandom function.

2. The client now sends a ChangeCipherSpec record, essentially telling the server, "Everything I tell you from now on will be authenticated (and encrypted if encryption parameters were present in the server certificate)." The ChangeCipherSpec is itself a record-level protocol with content type of 20.

  - Finally, the client sends an authenticated and encrypted Finished message, containing a hash and MAC over the previous handshake messages.
  - The server will attempt to decrypt the client's Finished message and verify the hash and MAC. If the decryption or verification fails, the handshake is considered to have failed and the connection should be torn down.

3. Finally, the server sends a ChangeCipherSpec, telling the client, "Everything I tell you from now on will be authenticated (and encrypted, if encryption was negotiated)."

  - The server sends its authenticated and encrypted Finished message.
  - The client performs the same decryption and verification procedure as the server did in the previous step.

4. Application phase: 

  at this point, the "handshake" is complete and the application protocol is enabled, with content type of 23. Application messages exchanged between client and server will also be authenticated and optionally encrypted exactly like in their Finished message. Otherwise, the content type will return 25 and the client will not authenticate.


Resumed TLS handshake
***********************

Public key operations (e.g., RSA) are relatively expensive in terms of computational power. TLS provides a secure shortcut in the handshake mechanism to avoid these operations: resumed sessions. Resumed sessions are implemented using session IDs or session tickets.

Apart from the performance benefit, resumed sessions can also be used for single sign-on, as it guarantees that both the original session and any resumed session originate from the same client. This is of particular importance for the FTP over TLS/SSL protocol, which would otherwise suffer from a man-in-the-middle attack in which an attacker could intercept the contents of the secondary data connections.

**Session IDs**

In an ordinary full handshake, the server sends a session id as part of the ServerHello message. The client associates this session id with the server's IP address and TCP port, so that when the client connects again to that server, it can use the session id to shortcut the handshake. In the server, the session id maps to the cryptographic parameters previously negotiated, specifically the "master secret". Both sides must have the same "master secret" or the resumed handshake will fail (this prevents an eavesdropper from using a session id). The random data in the ClientHello and ServerHello messages virtually guarantee that the generated connection keys will be different from in the previous connection. In the RFCs, this type of handshake is called an abbreviated handshake. It is also described in the literature as a restart handshake.

.. code-block:: bash 

    Client -> Server [Client Hello With Session ID]
    Client <- Server [Server Hello With Session ID]

    Client <- Server [ChangeCipherSpec]

    Client -> Server [ChangeCipherSpec]

    Client <-> Server [Application]

1. Negotiation phase:
    
  - A client sends a ClientHello message specifying the highest TLS protocol version it supports, a random number, a list of suggested cipher suites and compression methods. Included in the message is the **session id** from the previous TLS connection.
  - The server responds with a ServerHello message, containing the chosen protocol version, a random number, cipher suite and compression method from the choices offered by the client. If the server recognizes the session id sent by the client, it responds with the same session id. The client uses this to recognize that a resumed handshake is being performed. If the server does not recognize the session id sent by the client, it sends a different value for its session id. This tells the client that a resumed handshake will not be performed. At this point, both the client and server have the "master secret" and random data to generate the key data to be used for this connection.

2. The server now sends a ChangeCipherSpec record, essentially telling the client, "Everything I tell you from now on will be encrypted." The ChangeCipherSpec is itself a record-level protocol and has type 20 and not 22.

  - Finally, the server sends an encrypted Finished message, containing a hash and MAC over the previous handshake messages.
  - The client will attempt to decrypt the server's Finished message and verify the hash and MAC. If the decryption or verification fails, the handshake is considered to have failed and the connection should be torn down.
    
3. Finally, the client sends a ChangeCipherSpec, telling the server, "Everything I tell you from now on will be encrypted. "

  - The client sends its own encrypted Finished message.
  - The server performs the same decryption and verification procedure as the client did in the previous step.

4. Application phase: at this point, the "handshake" is complete and the application protocol is enabled, with content type of 23. Application messages exchanged between client and server will also be encrypted exactly like in their Finished message.


.. figure:: /images/web/handshaking02.png

In this Pcap recorded from visiting Github, it demos this steps.

Reference
************

https://stackoverflow.com/questions/34185716/tcp-client-sends-rst-ack-immediately-after-sending-ack-to-server

https://stackoverflow.com/questions/2582036/an-existing-connection-was-forcibly-closed-by-the-remote-host

https://en.wikipedia.org/wiki/Handshaking

https://en.wikipedia.org/wiki/Transport_Layer_Security#TLS_handshake
