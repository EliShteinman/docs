---
title: "How to Deploy a Redis Database from a Jenkins Pipeline"
linkTitle: "How to Deploy a Redis Database from a Jenkins Pipeline"
url: "/tutorials/create/jenkins/"
description: "Jenkins is currently the most popular CI(Continuous Integration) tool, with ~15M users. It is an open source automation server which enables developers to reliably build, test, and deploy their..."
group: "For developers"
aliases:
- "/tutorials/create-jenkins/"
date: 2026-02-25
lastmod: 2026-02-25
hidden: true
mirrored: true
---

*Published 25 February 2026*

> **TL;DR:**
>
> Store your Redis Cloud API credentials in the Jenkins secret store, write a `Jenkinsfile` that exports those credentials as environment variables, and call a Python script that sends a REST request to the Redis API to provision a new database. Every pipeline run produces a fresh, consistently configured Redis instance.

### What you'll learn

- How to install and configure Jenkins for Redis deployments
- How to store Redis credentials securely in the Jenkins secret store
- How to write a `Jenkinsfile` that provisions a Redis database through the Redis REST API
- How to verify a successful deployment in the Redis management UI

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed (for running Jenkins locally)
- A running Redis Enterprise cluster with REST API access
- Admin credentials for the Redis cluster (host, port, user, password)
- Basic familiarity with Jenkins pipelines and Groovy syntax

---

[Jenkins](https://www.jenkins.io/) is currently [the most popular CI(Continuous Integration) tool](https://cd.foundation/announcement/2019/08/14/jenkins-celebrates-15-years/), with ~15M users. It is an open source automation server which enables developers to reliably build, test, and deploy their software. It was forked in 2011 from a project called Hudson after a [dispute with Oracle](https://www.infoq.com/news/2011/01/jenkins/), and is used for [Continuous Integration and Continuous Delivery (CI/CD)](https://stackoverflow.com/questions/28608015/continuous-integration-vs-continuous-delivery-vs-continuous-deployment) and test automation. Jenkins is based on Java and provides over [1700 plugins](https://plugins.jenkins.io/) to automate your developer workflow and save a lot of your time in executing your repetitive tasks.

![Jenkins CI/CD automation server hero illustration](/images/site-mirror/a8e1793dc42d57dffb701bc4f997457eb9972d30-1047x860.webp)

[Source:](https://www.datanyze.com/market-share/ci--319) Datanyze market analysis

[Jenkins Pipeline](https://www.jenkins.io/solutions/pipeline/) performs Continuous Delivery tasks declared in a `Jenkinsfile` stored alongside code. The [Pipeline plugin](https://plugins.jenkins.io/workflow-aggregator) has a fairly comprehensive [tutorial](https://github.com/jenkinsci/pipeline-plugin/blob/master/TUTORIAL.md) checked into its source tree. Plugins are the primary means of enhancing the functionality of a Jenkins environment to suit organization- or user-specific needs. Using a Pipeline, you can configure Jenkins to automatically deploy key pieces of infrastructure, such as a Redis database.

### How does the Jenkins Redis deployment pipeline work?

Jenkins Pipelines are the Continuous Delivery (CD) side of Jenkins. They use a `Jenkinsfile` declarative script to define the behavior of the pipeline. You can script actions in Groovy and run shell scripts from it, so you can make it do pretty much anything.

The `Jenkinsfile` instructs Jenkins to export some environment variables from the Credentials store in order to connect to the Redis server, then executes the Python pipeline script with the Deployment Configuration file given as a parameter. An example `deployment-configuration-file.json` looks like:

```bash
{
  "database": {
    "name": "made-with-jenkins",
    "port": 12345,
    "size": "S",
    "operation": "CREATE"
  }
}
```

The Python script uses predefined JSON template files that create Redis databases of fixed t-shirt sizes (S, M, L, XL). The Deployment Config file tells the Python script what the desired database name, port, and size are. A sample template file looks like:

```bash
{
    "name": "{NAME}",
    "type": "redis",
    "memory_size": 343597383
}
```

The following is an architectural diagram of how a Jenkins pipeline adds a database to a Redis cluster.

![Architecture diagram showing how a Jenkins pipeline adds a database to a Redis cluster](/images/site-mirror/273e8dc7447efc81bc09c739823098d90fe2ce6a-1047x918.webp)

### What happens when the pipeline runs?

1.  The Jenkins pipeline clones a remote git repository, containing the application code and the pipeline code.
2.  The Redis host, port, user, and password are decrypted from the credentials store and are exported as Environment variables.
3.  Jenkins runs the Python pipeline script, specifying the deployment configuration file in the git repo.
4.  The Python script uses the deployment configuration file to choose and customize a pre-populated template to use as the body of the REST create database request to Redis.

### List of Pipeline Code Files

- [jenkins-re-pipeline.py](https://github.com/masyukun/redis-jenkins-pipeline/blob/main/jenkins-re-pipeline.py) config file
    - The Python script that creates a Redis database through the Redis REST API.
- [deployment-configuration-file.json](https://github.com/masyukun/redis-jenkins-pipeline/blob/main/deployment-configuration-file.json)
    - The user-specified configuration file for creating a database.
- [redis-standard-size-s.json.template](https://github.com/masyukun/redis-jenkins-pipeline/blob/main/redis-standard-size-s.json.template)
- [redis-standard-size-xl.json.template](https://github.com/masyukun/redis-jenkins-pipeline/blob/main/redis-standard-size-xl.json.template)

## How do you configure Jenkins for Redis deployments?

### How do you install Jenkins with Docker?

You can use [Docker Desktop](https://www.docker.com/products/docker-desktop) to quickly get a Jenkins instance up and running, exposing ports 8080 (web GUI) and 50000 (inbound agents).

```bash
docker run --name jenk -p 8080:8080 -p 50000:50000 jenkins/jenkins:lts-jdk11
```

The installation will generate a first-run password in the docker-cli output.

Then open the Jenkins URL [http://localhost:8080/](http://localhost:8080/) and enter the password to unlock your instance and begin installation.

![Unlocking Jenkins using the initial administrator password](/images/site-mirror/18c003a0cf7e4cde61b70ff36366d2befff7194e-1047x780.webp)

Choose "Install suggested plugins" to perform the Jenkins configuration.

![Installing suggested plugins during the initial Jenkins setup](/images/site-mirror/60db571d37b7529c0130f57035593b0ea806a61d-1047x594.webp)

Wait for the plugins to complete the installation process.

![Form for creating the first admin user in Jenkins](/images/site-mirror/87ecc32944699131574fe33da19e0906b20d4975-1047x610.webp)

Next, you're prompted to create your admin user.

![Jenkins successfully configured and ready for use](/images/site-mirror/e0284fc15e7087ab3156b0dc81ed296c74cbfc2a-1047x563.webp)

Congratulations! Jenkins is ready!

![Jenkins dashboard homepage showing application overview](/images/site-mirror/0cdf6f7cccec1d50270e6429e722c64cb4042865-1047x553.webp)

### How do you install Python and required libraries?

If you use an existing instance of Jenkins server, you can install Python and the custom libraries from the command line interface of that machine.

Docker instances of Jenkins can be accessed by shell using the following command:

```bash
docker exec -it -u root jenk bash
```

The Python pipeline script requires the libraries `click` and `requests`. It also requires Python.

```bash
apt-get update
apt-get install -y python3-pip

pip install --upgrade pip
pip install click
pip install requests
```

Alternatively, if you are creating a new Jenkins from scratch, you can include these dependencies in a separate `Dockerfile` that builds off the base Jenkins image:

```bash
FROM jenkins:latest
USER root
RUN apt-get update
RUN apt-get install -y python-pip

# Install app dependencies
RUN pip install --upgrade pip
RUN pip3 install click
RUN pip3 install requests
```

### How do you store Redis credentials in Jenkins?

Using the left-side menu, select Manage Jenkins, then select Manage Credentials, then click the link (global).

![Navigating to the Manage Credentials menu in Jenkins](/images/site-mirror/f5545d4172d6a027b53e22b017442ca709789898-1016x1442.webp)

![Viewing global credentials in the Jenkins management interface](/images/site-mirror/b58582500449d2a01634c71beafd8a4f8cf68d40-1047x784.webp)

From here, you can specify Kind: Secret text for the 4 secrets required to connect with the Redis REST endpoint:

- REDIS_SERVER_FQDN
    - Set to the 'https://server-address' of the target Redis instance.
- REDIS_SERVER_PORT
    - Set to the Redis REST API port (default 9443).
- REDIS_USER
    - Set to the Redis admin user allowed to create databases.
- REDIS_PASS
    - Set to the Redis admin user's password.

![Form for adding new secret text credentials for Redis access](/images/site-mirror/7b1b1d084952e26ed26cf29aa55dc52b4e0265b0-1047x570.webp)

If you are using a private code repository, you may also wish to include a Personal Access Token here.

### How do you create a Jenkins pipeline for Redis?

From the dashboard, click New Item.

Enter in a name for the pipeline, and choose the Pipeline type.

![Selecting the Pipeline job type for a new item in Jenkins](/images/site-mirror/fcb2ed63e57c20014a3283caa40534ec5ef6d482-1047x725.webp)

## How do you connect a GitHub repository to the pipeline?

From the Pipeline configuration page that appears, check the GitHub box and enter the git clone URL, complete with any credentials needed to read the repository. For GitHub access, the password should be a Personal Access Token rather than the actual user password.

![Configuring the GitHub repository source for the Jenkins pipeline](/images/site-mirror/4c955deecb8610725fcbca11ff99ef5d15560443-1047x796.webp)

### What does the Jenkinsfile look like?

Scrolling down on this page to the Advanced Project Options, you can either past in the `Jenkinsfile`, or you can specify the filename if the file exists in the git repository.

![Defining the pipeline execution logic using a Jenkinsfile script](/images/site-mirror/6aec81e0103c8ca637ad4898eadf0a39d34bc1f1-1047x813.webp)

Here is an example `Jenkinsfile` containing the mapping of Credentials to the environment variables, and 2 separate stages – a Hello World which always succeeds, and a build stage that invokes the Python script. Paste this into the pipeline script section.

```bash
pipeline {
    agent any

    environment {
        REDIS_SERVER_FQDN = credentials('REDIS_SERVER_FQDN')
        REDIS_SERVER_PORT = credentials('REDIS_SERVER_PORT')
        REDIS_USER =  credentials('REDIS_USER')
        REDIS_PASS = credentials('REDIS_PASS')
    }

    stages {
        stage('Hello') {
            steps {
                echo 'Hello World'
            }
        }

        stage('build') {
            steps {
                git branch: 'main', url: 'https://github.com/masyukun/redis-jenkins-pipeline.git'
                sh 'python3 jenkins-re-pipeline.py --deployfile deployment-configuration-file.json'
            }
        }
    }
}
```

Click "Save" when the job spec is complete.

### How do you run the pipeline and verify the deployment?

Click on the pipeline you created:

![Clicking the Build Now button to start the Jenkins pipeline](/images/site-mirror/5ff0ccd32db599d2995b404302c558d2d9cce647-1047x282.webp)

Click the "Build Now" icon on the left side menu.

Click the Status icon on the left side menu in order to see the results of all the output from each of the stages of your pipeline.  
Hover over the build stage and click the Logs button of the most recent build in order to see the Python script's output.

![Viewing the detailed logs for each build stage in Jenkins](/images/site-mirror/5016f4f623fe87cd74becbe705d911a12b54d2fe-1047x1116.webp)

Sample output: you should see a verbose response from Redis's REST service in the “Shell Script” accordion pane.

There's also a “Git” output log, in case you need to debug something at that level. Any time you update the branch in the remote git repository, you should see evidence in that log that the latest changes have successfully checked out into the local Jenkins git repository.

![Verifying the newly created database in the Redis Software Management UI](/images/site-mirror/f8ef45695fc87db5083c5f39ca887d876f937585-1047x543.webp)

Open your Redis Secure Management UI at `https://servername:8443` and click on the databases menu item to verify that your database was created with the name, port, and size specified in the `deployment-configuration-file.json` file.

Congratulations! You have deployed a Redis database using a Jenkins Pipeline!

The GitHub repository is currently: [https://github.com/masyukun/redis-jenkins-pipeline](https://github.com/masyukun/redis-jenkins-pipeline)

## Next steps

Now that you can provision Redis databases from a Jenkins pipeline, explore other CI/CD integrations:

- [Argo CD for Redis CI/CD](/tutorials/operate/ci-cd/argo-cd/) – Use Argo CD for GitOps-driven Redis deployments on Kubernetes.
- [CircleCI for Redis CI/CD](/tutorials/operate/ci-cd/circle-ci/) – Integrate Redis provisioning into CircleCI workflows.
