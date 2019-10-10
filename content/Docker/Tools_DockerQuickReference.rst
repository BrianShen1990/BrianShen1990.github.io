Docker Quick Reference
#######################

:date: 2019-09-10
:tags: Linux, CentOS7, Docker
:category: Docker
:author: Brian Shen
:slug: Docker_Quick_Reference
:summary: Docker Quick Reference

.. _Docker_Quick_Reference:

.. contents::

Docker concepts
^^^^^^^^^^^^^^^^

Docker is a platform for developers and sysadmins to **develop**, **deploy**, and **run** applications with containers. The use of Linux containers to deploy applications is called **containerization**. 


Containers and virtual machines
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A container runs natively on Linux and shares the kernel of the host machine with other containers. It runs a discrete process, taking no more memory than any other executable, making it lightweight.

By contrast, a virtual machine (VM) runs a full-blown “guest” operating system with virtual access to host resources through a hypervisor. In general, VMs provide an environment with more resources than most applications need.


Commands - Run and Debug
^^^^^^^^^^^^^^^^^^^^^^^^^

- :code:`docker run -d -v redis-vol:/data redis:alpine -p` run containers
- :code:`docker run -d -v redis-vol:/data redis`
- :code:`docker run --entrypoint /bin/bash -it nodeais:2.4.4`
- :code:`docker run -it -v /root:/root nodeais:2.4.3 bash`

- :code:`docker exec -i 92a1 curl 127.0.0.1:9200` **debug** go into shell without interrupt the main container, recommendation
- :code:`docker exec -it 92a1 bash`
- :code:`docker attach 69d1` attach will stop main process and return control here

- :code:`docker logs --tail=100 -f mongodb` to get debug logs 


Commands - Image
^^^^^^^^^^^^^^^^^^^^^^

- :code:`docker pull library/elasticsearch:5.6` to pull es 
- :code:`docker pull java:openjdk-8-jdk` to pull java

- :code:`docker images` list images
- :code:`docker image ls` 
- :code:`docker image ls mongo --format "{{.ID}}"`
- :code:`docker image rm *id*`

- :code:`docker build -t plugins-scripts:v23 .` build image 

Commands - Container
^^^^^^^^^^^^^^^^^^^^^^

- :code:`docker container ls`
- :code:`docker container ls -a` to include stooped ones
- :code:`docker container rm *id*`
- :code:`docker container prune` remove all stopped containers
- :code:`docker ps` is a short cut for :code:`docker container ls`

Commands - Volumes
^^^^^^^^^^^^^^^^^^^^^^

- :code:`docker volume ls`
- :code:`docker volume create redis-vol`
- :code:`docker run -d --name devtest --mount source=myvol2,target=/app nginx:latest`
- :code:`docker run -d --name devtest -v myvol2:/app nginx:latest` 
- :code:`docker volume inspect my-vol`
- :code:`docker volume rm my-vol`
- :code:`docker run -d --name=nginxtest --mount source=nginx-vol,destination=/usr/share/nginx/html,readonly nginx:latest` for read only
- :code:`docker run -d --name=nginxtest -v nginx-vol:/usr/share/nginx/html:ro nginx:latest` for read only
- :code:`docker volume prune`  delete all unused 

Commands - Network 
^^^^^^^^^^^^^^^^^^^

- :code:`docker network create my-net` bridge 
- :code:`docker network create --driver=bridge --subnet=172.28.0.0/16 --ip-range=172.28.5.0/24 --gateway=172.28.5.254 br0`
- :code:`docker network create -d macvlan --subnet=172.16.86.0/24 --gateway=172.16.86.1 -o parent=eth0 pub_net` macvlan
- :code:`docker network rm my-net` Remove network
- :code:`docker create --name my-nginx --network my-net --publish 8080:80 nginx:latest` Connect by starting 
- :code:`docker network connect my-net my-nginx` Connect while started 
- :code:`docker network disconnect my-net my-nginx` Disconnect 
- :code:`docker create --name my-nginx --network host --publish 8080:80 nginx:latest`
- :code:`docker network prune` all unused networks are removed

Commands - Format
^^^^^^^^^^^^^^^^^^

- :code:`println` print each line :code:`docker inspect --format='{{range .NetworkSettings.Networks}}{{println .IPAddress}}{{end}}' container`  
- :code:`docker inspect -f '{{range .NetworkSettings.Networks}}{{println .IPAddress}}{{end}}'` get IP

  - :code:`upper` : :code:`docker inspect --format "{{upper .Name}}" container` 
  - :code:`title` : :code:`docker inspect --format "{{title .Name}}" container`
  - :code:`split` : :code:`docker inspect --format '{{split .Image ":"}}'`
  - :code:`lower` : :code:`docker inspect --format "{{lower .Name}}" container`
  - :code:`json` : :code:`docker inspect --format '{{json .Mounts}}' container`
  - :code:`join` : :code:`docker inspect --format '{{join .Args " , "}}' container`

- Sample:

  .. code-block:: bash 

    docker inspect 7cb9995533cb | grep "IPAddress"
    
    .Service.ID	Service ID
    .Service.Name	Service name
    .Service.Labels	Service labels
    .Node.ID	Node ID
    .Node.Hostname	Node Hostname
    .Task.ID	Task ID
    .Task.Name	Task name
    .Task.Slot	Task slot

Commands Tags, Save and Export
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(Seems modern docker can remember the tag)

- :code:`docker image save b5435fede523 -o ./plugins-scrcips.2.3.0.180428.tar`
- :code:`docker image load -i ./plugins-scrcips.2.3.0.180428.tar`
- :code:`docker image tag b5435fede523 plugins-scripts:2.3.0`
- :code:`docker image rmi plugins-scripts:2.3.0`

Commands Others 
^^^^^^^^^^^^^^^^^^

- :code:`docker system prune` remove all images, containers, and networks.
- :code:`docker run --rm -it --security-opt apparmor=docker-default hello-world` security policy
- :code:`docker run  -v /root:/root -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix  -it node:6.14.0 /bin/bash`  Display (For LibreOffice/Chrome/FF)
- :code:`LABEL "com.example.vendor"="ACME Incorporated"` to add labels
- :code:`bin/registry garbage-collect [--dry-run] /path/to/config.yml` garbage collection 

Reference
^^^^^^^^^^

- https://docs.docker.com/get-started/
