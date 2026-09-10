---
title: "Create a Redis database on Google Kubernetes Engine"
linkTitle: "Create a Redis database on Google Kubernetes Engine"
url: "/tutorials/operate/orchestration/kubernetes/kubernetes-gke/"
description: "Deploy a Redis Enterprise database on Google Kubernetes Engine (GKE) using the Redis Enterprise Operator. This tutorial walks you through GKE cluster creation, operator deployment, and database..."
group: "For operators"
aliases:
- "/tutorials/operate-orchestration-kubernetes-kubernetes-gke/"
date: 2026-02-25
lastmod: 2026-02-25
hidden: true
mirrored: true
---

*Published 25 February 2026*

Deploy a Redis Enterprise database on Google Kubernetes Engine (GKE) using the Redis Enterprise Operator. This tutorial walks you through GKE cluster creation, operator deployment, and database provisioning so you can run a production-grade Redis cluster on GCP Kubernetes.

## What you'll learn

- How to create a GKE cluster sized for Redis Enterprise
- How to deploy the Redis Enterprise Operator for Kubernetes
- How to provision a Redis Enterprise Cluster (REC) on GKE
- How to retrieve cluster credentials and create a database

## What do you need before deploying Redis on GKE?

Before you begin, make sure you have the following:

- A Google Cloud account with the **Kubernetes Engine Admin** role
- A Linux, macOS, or WSL environment
- [Google Cloud SDK (`gcloud` CLI)](https://cloud.google.com/sdk/docs/install) installed and initialized with `gcloud init`
- `kubectl` installed (included with `gcloud components install kubectl`)
- `curl` and `git` installed

> Familiarity with Kubernetes concepts such as namespaces, pods, and deployments is helpful. See the [Kubernetes Operator tutorial](/tutorials/operate/orchestration/kubernetes-operator/) for background on how operators manage Redis clusters.

## How do you verify the Google Cloud SDK installation?

Confirm that `gcloud` is installed and available on your system:

```bash
gcloud version
```

You should see output similar to:

```bash
Google Cloud SDK 320.0.0
alpha 2020.12.04
app-engine-go 1.9.71
```

## How do you create a GKE cluster for Redis?

Create a five-node GKE cluster with enough resources to run Redis Enterprise. The `e2-standard-8` machine type provides 8 vCPUs and 32 GB of memory per node:

```bash
gcloud container clusters create redis-cluster \
  --subnetwork default \
  --num-nodes 5 \
  --machine-type e2-standard-8 \
  --region us-east1
```

After the cluster is ready, `gcloud` automatically configures `kubectl` to connect to it.

## How do you create a namespace for Redis?

Create a dedicated namespace to isolate your Redis deployment:

```bash
kubectl create namespace demo
```

Switch your `kubectl` context to use the new namespace by default:

```bash
kubectl config set-context --current --namespace=demo
```

## How do you deploy the Redis Enterprise Operator?

The Redis Enterprise Operator automates the deployment and management of Redis Enterprise clusters on Kubernetes. Deploy it by applying the operator bundle:

```bash
kubectl apply -f https://raw.githubusercontent.com/RedisLabs/redis-enterprise-k8s-docs/master/bundle.yaml
```

This creates the required roles, service accounts, custom resource definitions (CRDs), and the operator deployment itself.

Verify the operator is running:

```bash
kubectl get deployment redis-enterprise-operator
```

Expected output:

```bash
NAME                               READY   UP-TO-DATE   AVAILABLE   AGE
redis-enterprise-operator          1/1     1            1           2m
```

## How do you create a Redis Enterprise Cluster on GKE?

Apply the default Redis Enterprise Cluster (REC) custom resource. This configuration works well for development and testing:

```bash
kubectl apply -f crds/app_v1_redisenterprisecluster_cr.yaml
```

The cluster takes 5–10 minutes to initialize. Check its status using the `rec` shorthand:

```bash
kubectl get rec
```

Expected output:

```bash
NAME               AGE
redis-enterprise   14s
```

## How do you verify the Redis deployment on GKE?

List all the pods, services, and deployments to confirm everything is running:

```bash
kubectl get po,svc,deploy
```

Expected output:

```bash
NAME                                                    READY   STATUS    RESTARTS   AGE
pod/redis-enterprise-0                                  2/2     Running   0          6m42s
pod/redis-enterprise-1                                  2/2     Running   0          4m34s
pod/redis-enterprise-2                                  2/2     Running   0          2m18s
pod/redis-enterprise-operator-58f8566fd7-5kcvz          1/1     Running   0          69m
pod/redis-enterprise-services-rigger-5849b86c65-lwql9   1/1     Running   0          6m42s
NAME                          TYPE           CLUSTER-IP     EXTERNAL-IP     PORT(S)                      AGE
service/kubernetes            ClusterIP      10.3.240.1     <none>          443/TCP                      71m
service/redis-enterprise      ClusterIP      None           <none>          9443/TCP,8001/TCP,8070/TCP   6m42s
service/redis-enterprise-ui   LoadBalancer   10.3.246.252   35.196.117.24   8443:31473/TCP               6m42s
NAME                                               READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/redis-enterprise-operator          1/1     1            1           69m
deployment.apps/redis-enterprise-services-rigger   1/1     1            1           6m44s
```

You can also verify the pods and services in the Google Cloud Console:

![Google Cloud Console showing Redis Enterprise pods and services running on GKE, including the operator, cluster nodes, and services rigger](/images/site-mirror/2434aab8c940340edfba0c1f2d912f8c5aac3e81-1332x854.webp)

## How do you retrieve the Redis cluster admin password?

Extract the admin password from the Kubernetes secret:

```bash
kubectl get secrets redis-enterprise -o jsonpath='{.data.password}' | base64 --decode
```

## How do you create a Redis database?

Open the Redis Enterprise web console at `https://<EXTERNAL-IP>:8443` (use the `redis-enterprise-ui` service external IP from the output above). Log in with the admin credentials, then:

1. Click **Setup** and configure your cluster DNS and admin account.
2. Navigate to **Databases** and create your first Redis database.

## Next steps

- Learn how Kubernetes operators manage Redis: [Kubernetes Operator tutorial](/tutorials/operate/orchestration/kubernetes-operator/)
- Understand the underlying design: [Redis Kubernetes Architecture](https://redis.io/docs/latest/operate/kubernetes/architecture/)
- Plan for production workloads: [Sizing and Scaling Redis on Kubernetes](https://redis.io/docs/latest/operate/kubernetes/recommendations/sizing-on-kubernetes/)

![Diagram showing Redis Enterprise Kubernetes architecture with operator, StatefulSet, and Redis Enterprise Cluster pods distributed across Kubernetes nodes](/images/site-mirror/a0e97d6d114339c086d82ad3bbeaf992ee501a94-1518x562.webp)
