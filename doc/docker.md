# Instructions for running inside docker

This is still experimental, so there might be some problems with it.

### 1. Install Postgresql

  ```bash
  $ sudo apt-get update --fix-missing
  $ sudo apt-get install postgresql postgresql-server-dev-all
  ```

### 2. Clone the repo.

  ```bash
  $ git clone git://github.com/freedomsponsors/www.freedomsponsors.org.git
  $ cd www.freedomsponsors.org
  ```

### 3. Create the database/default user.

  ```bash
  $ sudo su postgres #run the next command as postgres
  $ createuser -d -SRP frespo # this will prompt you to create a password (just use frespo for now)
  $ createdb -O frespo frespo
  $ exit # go back to your normal user
  ```

### 4. Install docker

https://www.docker.com/

### 5. Create the docker image for the repo

```bash
$ cd www.freedomsponsors.org
$ docker build -t freedomsponsors .
```

### 6. Find out your host ip (visible to docker containers)

```bash
$ ip addr
```

Look for your "docker ip":

```
...
inet6 fe80::271:ccff:fe89:71e9/64 scope link
   valid_lft forever preferred_lft forever
4: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default
link/ether 02:42:55:58:f7:70 brd ff:ff:ff:ff:ff:ff
inet 172.17.0.1/16 scope global docker0
   valid_lft forever preferred_lft forever
inet6 fe80::42:55ff:fe58:f770/64 scope link
   valid_lft forever preferred_lft forever
...
```

In the example output above it's 172.17.0.1

### 7. Make sure your DB can be accessed by somewhere other than localhost.

You need to edit pg_hba.conf and postgresql.conf

http://www.cyberciti.biz/tips/postgres-allow-remote-access-tcp-connection.html

### 8. Run the docker image:

```bash
docker run -it -e DATABASE_HOST=172.17.0.1 freedomsponsors
```

TODO:
* How to live-update the running application without having to restart the docker container
* How to debug on pycharm
* Publish image on dockerhub
* Deploy to production using docker
