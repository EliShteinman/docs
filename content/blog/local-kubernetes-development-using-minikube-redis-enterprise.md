---
title: "Local Kubernetes Development Using Minikube and Redis Enterprise"
linkTitle: "Local Kubernetes Development Using Minikube and Redis Enterprise"
url: "/blog/local-kubernetes-development-using-minikube-redis-enterprise/"
description: "Kubernetes is an open-source container orchestration system used to deploy, scale and manage containerized applications. Kubernetes is a project hosted by the Cloud Native Computing Foundation..."
date: 2018-01-05
blogCategories:
- "Company"
- "Tech"
authors:
- "Vick Kelkar"
lastmod: 2025-03-04
hidden: true
mirrored: true
---

*By Vick Kelkar, Principal Product Manager · Published 5 January 2018 · updated 4 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

Kubernetes is an open-source container orchestration system used to deploy, scale and manage containerized applications. Kubernetes is a project hosted by the Cloud Native Computing Foundation ([CNCF](https://www.cncf.io/)). At a very high level, it contains two types of resources: a master node (which is the cluster coordinator) and nodes, which are the workers that run containerized applications.

Minikube is a tool used to run a Kubernetes cluster on a local machine. Minikube is a single-node Kubernetes cluster inside a VM on your laptop. Minikube can be used to try out Kubernetes and or develop with it day-to-day.

The [Redis Enterprise](/) offering extends Redis, the most popular database used with Docker containers. Redis Enterprise delivers high performance, low latency and high availability to organizations. This blog post will show you the basics steps needed to setup Minikube and run a 3-node Redis Enterprise cluster on your local laptop.

## Installation

We are going to use the [homebrew](https://brew.sh/) package manager to install minikube and kubernetes command line tool on your local laptop.

```javascript
$ brew cask install minikube
$ brew install kubernetes-cli

```

## Starting Minikube

Minikube offers the ability to change the Virtual Machine (VM) driver. For this blog post, we used the vmwarefusion driver.

```javascript
$ minikube start --memory 12288 --disk-size 30g --vm-driver vmwarefusion

```

The output of the command should look like:

![Minikube startup output](/images/site-mirror/cfb11634b1155ac2fc63d164e9b618f061cdee97-600x209.webp)

*Minikube startup output*

## Verify Minikube installation

We will use the Kubernetes command-line tool, kubectl, to verify the Minikube installation. You can verify the Minikube install using:

```javascript
$ kubectl cluster-info

```

The output should look like:

```javascript
Kubernetes master is running at https://192.168.21.147:8443

```

## Redis Enterprise on Minikube

### Installation

Minikube is now running on your laptop and kubectl cli was able to successfully query the master node to get the status of the cluster. We will now deploy the Redis Enterprise service in Minikube with three replica sets. The yaml configuration for the Redis Enterprise deployment and service can be found [here.](https://gist.github.com/v-kelkar/6dd938ec8aa9e26cb39edcb7420683e9)

We will use the yaml to create the deployment and service in the Kubernetes cluster.

```javascript
$ kubectl apply -f redis-enterprise5.yaml
deployment "redis5" created
service "redis5" created
```

We can verify that three pods were created by issuing the command

```javascript
Kubectl get pods -o wide
```

![Output of kubectl get pods](/images/site-mirror/5b6f68d8d73f255ee297fa7a9b8f14513568438e-717x95.webp)

*Output: kubectl get pods -o wide*

### Prerequisite for Cluster Configuration

We need to change the binding of the CCS from local loopback address 127.0.0.1 to 0.0.0.0.

```javascript
$ kubectl exec -it <name-of-your-pod> bash
$ sed 's/bind 127.0.0.1/bind 0.0.0.0/g' -i /opt/redis/config/ccs-redis.conf
$ /opt/redis/bin/supervisorctl restart ccs

```

### Configuration of Cluster

We need to setup the Redis Enterprise cluster as a master node by logging into the pod and issuing a `create cluster` command.

```javascript
$ kubectl exec -it <name-of-your-pod> bash

```

We will use the rladmin utility to create the new cluster:

```javascript
root@redis5-7749c97f4d-vk6rn:~# /opt/redis/bin/rladmin cluster create name cluster.local username <your_email_addr> password <your_passwd>

```

We will use the rladmin utility to join the 2 nodes to cluster

```javascript
root@redis5-7749c97f4d-hcggk:~#/opt/redis/bin/rladmin cluster join username <your_email_addr> password <master_password> nodes <master_IP_addr>

```

and

```javascript
root@redis5-7749c97f4d-p74nx:~#/opt/redis/bin/rladmin cluster join username <your_email_addr> password <master_password> nodes <master_IP_addr>

```

### Database creation on cluster

We will use the Rest API of Redis Enterprise to create a database on the master node:

```javascript
curl -k -u "vick@redis.com:<password>" --request POST --url "https://localhost:9443/v1/bdbs" --header 'content-type: application/json' --data '{"name":"demo-db","type":"redis","memory_size":536870912,"port":11000,"data_persistence":"aof","replication":true,"shards_placement":"sparse","proxy_policy":"all-master-shards"}'

```

We can look at the status of the cluster and database using the rladmin utility included in Redis Enterprise download:

![rladmin cluster status](/images/site-mirror/1d2749b5949ce2f465880dc07049489094613c13-1012x362.webp)

*rladmin cluster status*

- You can read more about Redis Enterprise’s shard placement policy and proxy policy on our [documentation page](https://docs.redis.com/latest/rs/administering/designing-production/networking/multiple-active-proxy/).
- Redis Enterprise includes replication and persistence by default. You can read about persistence on our Redis Enterprise [database documentation page](https://docs.redis.com/latest/rs/concepts/data-access/persistence/).

### Redis Enterprise Dashboard access

You can access the Redis Enterprise dashboard, which is running on port 8443, by setting up a secure tunnel between local port and the pod port. Once the tunnel is established, you can reach the Redis Enterprise dashboard at https://127.0.0.1:8443:

kubectl port-forward <my-pod-name> <localport>:<pod-port>

Example: kubectl port-forward redis5-58dc568c56-7qk22 8443:8443

![Redis Enterprise Dashboard](/images/site-mirror/e63ae1db04eac9e6ca61203f5c060ec18e19638a-1019x429.webp)

*Redis Enterprise Dashboard – Nodes*

![Redis Enterprise Dashboard - Database](/images/site-mirror/70046263cbde70656c327117fda8c54dc0f9cb90-1006x498.webp)

*Redis Enterprise Dashboard – Database*

### Local access to Redis Enterprise

You can connect to your database using the IP of the node and the port specified during database creation:

```javascript
$ redis-cli -h <ip_addr_of master_node> -p <11000>

```

### What’s next

We are working on a Kubernetes native Redis Enterprise container that will take advantage of the new primitives introduced in Kubernetes 1.8 and above. We are working on releasing a new version of the Redis Enterprise container image that will leverage both the new Persistent Sets and the Storage class primitives while providing a better cluster bootstrapping experience. In the meantime, [learn more about the Redis Enterprise](/redis-enterprise/advantages/) offering.
