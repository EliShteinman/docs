---
title: "Argo CD: What it is and why it should be part of your Redis CI-CD"
linkTitle: "Argo CD: What it is and why it should be part of your Redis CI-CD"
url: "/tutorials/operate/ci-cd/argo-cd/"
description: "Argo CD is an open-source, declarative, GitOps continuous delivery tool built for Kubernetes. The name combines Argo—a CNCF-hosted container-native workflow engine—with CD (continuous delivery),..."
aliases:
- "/tutorials/operate-ci-cd-argo-cd/"
date: 2026-02-25
lastmod: 2026-02-26
hidden: true
---

*Published 25 February 2026 · updated 26 February 2026*

> **TL;DR:**
>
> Argo CD is a declarative, GitOps-based continuous delivery tool for Kubernetes. It monitors a Git repository for changes to Kubernetes manifests and automatically syncs them to your cluster. In this tutorial you will install Argo CD, connect it to a Git repo containing Redis manifests, and deploy Redis to a local Kubernetes cluster—all without manually running `kubectl apply`.

![Argo CD logo on a dark background](/images/site-mirror/68bfb5c3e6238875e3816c68d821e08697c5c245-512x496.webp)

## What you'll learn

- What Argo CD is and how it implements GitOps for Kubernetes
- How to install and configure Argo CD on a local Kubernetes cluster
- How to deploy a Redis application through Argo CD
- How to deploy a multi-service voting app that uses Redis as a queue
- How Argo CD keeps your cluster in sync with your Git repository

## What is Argo CD?

Argo CD is an open-source, declarative, GitOps continuous delivery tool built for Kubernetes. The name combines [Argo](https://argoproj.github.io/)—a [CNCF-hosted](https://www.cncf.io/blog/2020/04/07/toc-welcomes-argo-into-the-cncf-incubator/) container-native workflow engine—with CD ([continuous delivery](https://en.wikipedia.org/wiki/Continuous_delivery)), the practice of automatically deploying every code change to a testing or production environment after the build stage.

Argo CD follows the [GitOps methodology](https://about.gitlab.com/topics/gitops/), which uses [Git as the single source of truth](https://git-scm.com/) for declarative infrastructure and application configuration. It watches a remote Git repository for new or updated manifest files and synchronizes those changes with the cluster. By managing manifests in Git and syncing them with the cluster, you get all the advantages of a Git-based workflow—version control, pull-request reviews, collaboration transparency—and a one-to-one mapping between what is in the Git repo and what is deployed in the cluster.

> Argo CD empowers organizations to declaratively build and run cloud-native applications and workflows on Kubernetes using GitOps.

![Argo CD user interface header bar showing navigation and status](/images/site-mirror/8897da125db8b1e7467c516d8c7f8b0aa152ad7c-512x107.webp)

Argo CD is a pull-based, declarative, GitOps continuous delivery tool for Kubernetes with a [fully loaded UI](https://github.com/argoproj/argo-cd/tree/master/ui). The tool reads your environment configuration from your Git repository and applies it to your Kubernetes namespaces. App definitions, environment, and configurations should be declarative and version-controlled. App deployment and life cycle management should be automated, auditable, and easy to understand.

Built specifically to make continuous deployment to Kubernetes simpler and more efficient, Argo CD addresses several common challenges: the need to set up additional tools outside of Jenkins for a complete CI/CD pipeline to Kubernetes, the need to configure access control to Kubernetes across cloud platforms, and the need for visibility into deployment status once a new app is pushed to a cluster.

Argo CD is not just deployed inside Kubernetes—it should be considered an extension of Kubernetes, as it uses existing Kubernetes resources and functionalities like etcd and controllers to store data and monitor real-time updates of application state. If you are already using Kubernetes to run Redis workloads (for example, via the [Redis Kubernetes Operator](/tutorials/operate/orchestration/kubernetes-operator/)), Argo CD is a natural next step for automating deployments.

## How does Argo CD work?

![GitOps workflow diagram showing Argo CD pulling manifest changes from a Git repository into a Kubernetes cluster](/images/site-mirror/eb1e3ec4049ad952ad4459435b037162f93625f1-992x543.webp)

Instead of pushing changes to the Kubernetes cluster, Argo CD pulls Kubernetes manifest changes and applies them. Once Argo CD is running inside your cluster, you configure it to connect and track a Git repository.

If any changes are detected, Argo CD applies those changes automatically to the cluster. Developers can commit code (for example, through Jenkins), which will automatically build a new image, push it to a container registry, and then update the Kubernetes manifest file. Argo CD pulls the updated manifest and deploys it—saving manual work, reducing the initial setup configuration, and eliminating security risks. Whatever manifest files are connected to the Git repo will be tracked and synced by Argo CD, providing a single flexible deployment tool for developers and DevOps teams.

Argo CD also watches the cluster for changes. If someone updates the cluster manually, Argo CD detects the divergence between the desired state in Git and the actual state in the cluster, then syncs the Git-defined state back to the cluster—guaranteeing that the Git repo remains the single source of truth. Argo CD can also be configured to send an alert instead of automatically overriding manual updates, if a quick direct change to the cluster is needed.

## What are Argo CD's capabilities?

Argo CD provides declarative, version-controlled application deployments with automatic monitoring and pulling of manifest changes from Git. Key capabilities include:

- **Easy rollback:** Revert to a previous state without manually undoing every update in the cluster.
- **Web UI:** A visual dashboard for monitoring and managing Kubernetes resources.
- **Multiple manifest formats:** Supports Kubernetes YAML files, Helm Charts, Kustomize, and other templating tools that generate Kubernetes manifests.
- **CLI and metrics:** A command-line interface, Grafana metrics dashboard, and audit trails for application events and API calls.
- **Disaster recovery:** Point a new cluster to the Git repo and Argo CD will automatically recreate the same exact state—no manual intervention required.
- **Access control via Git:** Configure who can commit merge requests and who can approve them, managing cluster access indirectly through Git. No need to give external tools like Jenkins direct access to cluster credentials.

## Prerequisites

Before you begin, make sure you have the following installed and configured:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) with Kubernetes enabled (Settings > Kubernetes > Enable Kubernetes)
- [kubectl](https://kubernetes.io/docs/tasks/tools/) configured to use the Docker Desktop context
- [Homebrew](https://brew.sh/) (macOS) for installing the Argo CD CLI

## Getting started

## Step 1. Install the Argo CD CLI

```bash
brew install argocd
```

## Step 2. Create a new namespace

Create a namespace called `argocd` where all Argo CD resources will be installed.

```bash
kubectl create namespace argocd
```

## Step 3. Install Argo CD resources

```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

kubectl get po -n argocd
NAME                                  READY   STATUS              RESTARTS   AGE
argocd-application-controller-0       0/1     ContainerCreating   0          3m9s
argocd-dex-server-65bf5f4fc7-5kjg6    0/1     Init:0/1            0          3m13s
argocd-redis-d486999b7-929q9          0/1     ContainerCreating   0          3m13s
argocd-repo-server-8465d84869-rpr9n   0/1     Init:0/1            0          3m12s
argocd-server-87b47d787-gxwlb         0/1     ContainerCreating   0          3m11s
```

## Step 4. Ensure that all pods are up and running

```bash
kubectl get po -n argocd
NAME                                  READY   STATUS    RESTARTS   AGE
argocd-application-controller-0       1/1     Running   0          5m25s
argocd-dex-server-65bf5f4fc7-5kjg6    1/1     Running   0          5m29s
argocd-redis-d486999b7-929q9          1/1     Running   0          5m29s
argocd-repo-server-8465d84869-rpr9n   1/1     Running   0          5m28s
argocd-server-87b47d787-gxwlb         1/1     Running   0          5m27s
```

## Step 5. Configure port forwarding for dashboard access

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
Forwarding from 127.0.0.1:8080 -> 8080
Forwarding from [::1]:8080 -> 8080
```

![Argo CD login screen with username and password fields](/images/site-mirror/9ac25adf2f58a235e5d80771bf85812c819282e2-512x281.webp)

## Step 6. Log in

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo

HcD1I0XXXXXQVrq-
```

![Argo CD dashboard showing an empty application list after first login](/images/site-mirror/11016615002461fc7cec3ebd525f613d4488e963-512x165.webp)

## Step 7. Install Argo CD CLI on Mac using Homebrew

```bash
brew install argocd
```

## Step 8. Access the Argo CD API server

By default, the Argo CD API server is not exposed with an external IP. To access the API server, choose one of the following techniques to expose the Argo CD API server:

```bash
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'
service/argocd-server patched
```

## Step 9. Log in to Argo CD

```bash
argocd login localhost
WARNING: server certificate had error: x509: certificate signed by unknown authority. Proceed insecurely (y/n)? y
Username: admin
Password:
'admin:login' logged in successfully
Context 'localhost' updated
```

## Step 10. Update the password

```bash
argocd account update-password
*** Enter password of currently logged in user (admin):
*** Enter new password for user admin:
*** Confirm new password for user admin:
Password updated
Context 'localhost' updated
```

## Step 11. Register a cluster to deploy apps to

As we are running it on Docker Desktop, we will add it accordingly.

```bash
argocd cluster add docker-desktop
WARNING: This will create a service account `argocd-manager` on the cluster referenced by context `docker-desktop` with full cluster level admin privileges. Do you want to continue [y/N]? y
INFO[0002] ServiceAccount "argocd-manager" created in namespace "kube-system"
INFO[0002] ClusterRole "argocd-manager-role" created
INFO[0002] ClusterRoleBinding "argocd-manager-role-binding" created
Cluster 'https://kubernetes.docker.internal:6443' added
```

## Step 12. Create a new Redis application

Click "Create" and provide a repository URL as [https://github.com/argoproj/argo-cd/tree/master/manifests/base/redis](https://github.com/argoproj/argo-cd/tree/master/manifests/base/redis).

![Argo CD new application form with fields for app name, project, and sync policy](/images/site-mirror/dfaffda37d8f1f5b59f20c6a7b3f1830ee89a7cc-512x261.webp)

![Argo CD application source settings showing the Git repository URL and path to Redis manifests](/images/site-mirror/ac852f5c86faeebd7de0518c9b8d08545888a76b-1047x997.webp)

```bash
argocd app list
NAME       CLUSTER                                  NAMESPACE  PROJECT  STATUS  HEALTH   SYNCPOLICY  CONDITIONS  REPO                                 PATH                  TARGET
redisdemo  https://kubernetes.docker.internal:6443  argocd     default  Synced  Healthy  <none>      <none>      https://github.com/argoproj/argo-cd  manifests/base/redis  HEAD
```

![Argo CD resource tree view showing Redis deployment, service, and pod resources](/images/site-mirror/a411cdf17f77facb443621b85c9083a3998e9002-1047x501.webp)

![Argo CD application detail view showing Healthy sync status and resource summary for Redis](/images/site-mirror/ac6c554095ebda96497aa81158307d1fc452d82d-1047x527.webp)

![Detailed view of a Redis pod resource node showing status, labels, and metadata in Argo CD](/images/site-mirror/8d5a1e36ceb7cd98b7c11848f67556680910dd26-1047x449.webp)

## Step 13. Delete the Redis app

```bash
argocd app delete redisdemo
```

## Example: Voting app

![Architecture diagram of the voting application showing data flow between Python, Redis, .NET, Postgres, and Node.js components](/images/site-mirror/3e7e940ef0fb24747f3998ab003227850be588d5-558x622.webp)

Let's try to deploy a voting app. The voting application only accepts one vote per client. It does not register votes if a vote has already been submitted from a client.

![Component list for the voting application with technology stack labels for each service](/images/site-mirror/183c1509bd32887a3c9fb1d5330f4294a659520a-1047x588.webp)

- A Python web app which lets you vote between two options
- A Redis queue that collects new votes
- A .NET worker which consumes votes and stores them in…
- A Postgres database backed by a Docker volume
- A Node.js web app that shows the results of the voting in real time

Go to the Argo CD dashboard, enter the [repository URL](https://github.com/dockersamples/example-voting-app/tree/master/k8s-specifications), and supply the right PATH. Click "Create App" to deploy the application on your Docker Desktop.

![Voting application deployed in Argo CD with resource nodes grouped by type showing deployments, services, and pods](/images/site-mirror/b9c735670b8ab01108788a062f468c646dcb8731-1047x667.webp)

Next, visualize the complete application by choosing "Group by Node."

![Voting application resources grouped by parent resource in the Argo CD resource tree](/images/site-mirror/055c094275e8baa87c7654a56e8ed9e730cbff8a-1047x656.webp)

Grouping by parent resources:

![Events panel in Argo CD showing deployment, sync, and health-check activity logs for the voting app](/images/site-mirror/0368197bdd91c06a8b3e7a51593bb1908cb9e9a5-1047x347.webp)

Keep a close watch over the events by clicking on the "Events" section.

![Overview of all voting application resources in Argo CD showing services, deployments, and replica sets](/images/site-mirror/7dd5b6ef02c3051bf8b2033183ca44b2d67ca1b2-1047x582.webp)

Below is the complete overview of the voting application.

![Full resource graph for the voting application in the Argo CD UI with all nodes expanded](/images/site-mirror/7fc877b45d55f124c08fa532df5e7ea795a3a0d9-1047x573.webp)

Access the app via [http://localhost:31000/](http://localhost:31000/).

![Voting application frontend showing two voting options with a submit button](/images/site-mirror/4f7872b4e10080a0e0f33d5b8fd4577f1b23f0dd-1047x689.webp)

The results are accessible via [http://localhost:31001/](http://localhost:31001/).

![Voting results page showing real-time vote counts and percentages](/images/site-mirror/d3f149230e96bd49ee3ac99d803f2d871fe2c3d8-1047x506.webp)

## Next steps

Now that you have Argo CD deploying Redis applications to your Kubernetes cluster, here are some areas to explore next:

- **Redis Kubernetes Operator:** Learn how to manage Redis clusters on Kubernetes with the [Redis Kubernetes Operator tutorial](/tutorials/operate/orchestration/kubernetes-operator/).
- **Auto-sync policies:** Configure Argo CD to automatically sync changes without manual intervention using [auto-sync policies](https://argo-cd.readthedocs.io/en/stable/user-guide/auto_sync/).
- **Health checks:** Set up custom [health checks](https://argo-cd.readthedocs.io/en/stable/operator-manual/health/) so Argo CD can verify that your Redis deployment is serving traffic correctly.
- **Notifications:** Configure [Argo CD Notifications](https://argo-cd.readthedocs.io/en/stable/operator-manual/notifications/) to send alerts to Slack, email, or other channels when deployments succeed or fail.
