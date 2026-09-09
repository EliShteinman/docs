---
title: "CircleCI: What it is and why it should be part of your Redis CI-CD"
linkTitle: "CircleCI: What it is and why it should be part of your Redis CI-CD"
url: "/tutorials/operate/ci-cd/circle-ci/"
description: "CircleCI is a continuous integration and continuous delivery (CI/CD) platform designed to automate the build, test, and deployment stages of software development. It integrates with version control..."
aliases:
- "/tutorials/operate-ci-cd-circle-ci/"
date: 2026-02-25
lastmod: 2026-02-26
hidden: true
---

*Published 25 February 2026 · updated 26 February 2026*

> **TL;DR:**
>
> You can use CircleCI with Redis by adding a Redis service container to your CircleCI pipeline configuration. Define your jobs in a `.circleci/config.yml` file, include a Redis Docker image as a secondary service, and CircleCI handles the rest — running your tests against a live Redis instance on every commit and deploying your application automatically.

![CircleCI platform logo with text](/images/site-mirror/a97cdb99aa02f720613b72165d1686eaa83df1f5-1585x320.webp)

## What you'll learn

- What CircleCI is and how it fits into a Redis CI/CD workflow
- How to connect a GitHub repository to CircleCI
- How to configure a `.circleci/config.yml` pipeline for a Redis application
- How to deploy a Redis-powered Python app to Heroku using CircleCI

## What is CircleCI?

[CircleCI](https://circleci.com/) is a continuous integration and continuous delivery (CI/CD) platform designed to automate the build, test, and deployment stages of software development. It integrates with version control systems like GitHub and Bitbucket to trigger pipelines on every code change, giving teams fast feedback through a real-time dashboard.

CircleCI supports a wide range of languages and [cloud-hosted compute types](https://circleci.com/product/#hosting-options) including Docker containers, Linux VMs, macOS, Windows, and Arm executors. Pipelines are defined as code in a `config.yml` file, which makes them version-controlled, reviewable, and reproducible.

Key features include parallel job execution, built-in caching (including Redis caching), reusable configuration packages called orbs, SSH debugging, self-hosted runners, and flaky test detection.

## How does CircleCI work?

![Diagram showing the CircleCI workflow from a code commit to automated build, test, and deployment stages](/images/site-mirror/2064b9cf2e389f63626501f463f67b91c197724b-512x285.webp)

After you authorize GitHub or Bitbucket and add your repository as a project on circleci.com, every code change triggers a pipeline run. CircleCI locates your `.circleci/config.yml`, executes the defined jobs — building your code, running tests, performing security scans, and going through any approval steps — then deploys the result. You receive an email notification on success or failure.

## What are CircleCI's capabilities?

As a DevOps engineer or developer, you can:

- SSH into any job to debug build issues.
- Set up jobs to run in parallel to reduce pipeline duration.
- Configure a Redis cache with two simple keys to reuse data from previous jobs in your workflow.
- Configure self-hosted runners for unique platform support.
- Access Arm resources for the machine executor.
- Use reusable packages of configuration (orbs) to integrate with third parties.
- Use a pre-built Redis Docker image in a variety of languages.
- Use the API to retrieve information about jobs and workflows.
- Use the CLI to access advanced tools locally.
- Get flaky test detection with test insights.

## Deploy a Redis rate limiting application on Heroku using CircleCI

### Prerequisites

- A [CircleCI](https://circleci.com/) account (free tier available)
- A [GitHub](https://github.com/) account
- A [Heroku](https://www.heroku.com/) account
- Basic familiarity with Git, YAML, and command-line tools

### Getting started

In this tutorial, you will configure CircleCI to deploy a Redis rate limiting application built with Python directly to the Heroku platform.

Rate limiting is a mechanism that controls how many requests a client can make to an API endpoint within a time window, responding with a 429 status code when the limit is exceeded. The complete source code for this project is [available on GitHub](https://github.com/redis-developer/basic-rate-limiting-demo-python).

### Step 1. Log in to CircleCI with your GitHub account

Go to [https://circleci.com](https://circleci.com) and log in. Choose GitHub as the authentication method to connect your repositories directly.

![CircleCI login page showing options to authenticate with GitHub, Bitbucket, or email](/images/site-mirror/9fd554e6ad6502daed380dc29a38569b0f5610da-1600x645.webp)

### Step 2. Authorize CircleCI on GitHub

Grant CircleCI permission to access your GitHub repositories.

![GitHub OAuth authorization prompt requesting permissions for CircleCI](/images/site-mirror/c53e1147a17fe1cb55e98464f51d8f19659d0b99-807x376.webp)

### Step 3. Select your project repository and click "Setup Project"

Choose the Redis rate limiting repository from your project list.

![CircleCI project list with the Redis rate limiting repository highlighted and a Setup Project button](/images/site-mirror/c74840edec027604485623001792b69595e229af-1600x737.webp)

### Step 4. Create a CircleCI configuration file

CircleCI uses configuration as code. The entire delivery process from build to deployment is orchestrated through a single file called `config.yml`, located in a `.circleci` directory at the root of your project.

![CircleCI setup wizard offering options to create a new config.yml from a template or use an existing one](/images/site-mirror/b8844f7bdae5bd21d335f612362c96e16bd0cb58-1402x1274.webp)

Since we haven't created a `config.yml` file yet, choose the "Fast" option to start from an editable template.

![CircleCI template selector showing available sample pipeline configurations](/images/site-mirror/732dbfe6a7df09e8e6e3f29e50042e33e5b95374-1242x720.webp)

After clicking "Set Up project," you'll be prompted to select a sample config:

![CircleCI editor displaying a list of sample configuration files to choose from](/images/site-mirror/4094ed31d1696995f6d0bd6466aad061ad80ac2d-1600x1018.webp)

Add the following content to `.circleci/config.yml` and save the file:

```yaml
version: 2.1
orbs:
    heroku: circleci/heroku@1.2.6
workflows:
    heroku_deploy:
        jobs:
            - heroku/deploy-via-git
```

This configuration pulls in the Heroku orb (`circleci/heroku@1.2.6`), which provides a set of pre-built Heroku jobs and commands. The `heroku/deploy-via-git` job deploys your application from your GitHub repository directly to your Heroku account.

### Step 5. Merge the pull request

Once you save the new configuration, CircleCI creates a pull request in your repository. Go ahead and merge it.

![GitHub pull request view showing the new CircleCI config.yml ready to be merged](/images/site-mirror/88831403a756f422e4abb92dea41e5f5423b28c4-1600x1039.webp)

### Step 6. Set up your Heroku account

[Follow these steps](https://redis.io/create/heroku/portal) to set up a Heroku account and create a new app called `rate-limit-python`. You'll need your Heroku API key for the next step.

![Heroku dashboard showing the creation of a new application named rate-limit-python](/images/site-mirror/cea40b42b56126b8a9a4a94b4d1e2524a7c5ad73-1600x838.webp)

### Step 7. Configure Heroku environment variables on CircleCI

Before CircleCI can deploy to Heroku, you need to set up an authenticated connection between the two platforms. In your CircleCI project settings, navigate to **Build Settings > Environment Variables** and create two variables:

- **HEROKU_APP_NAME** — the name of your Heroku application (e.g., `rate-limit-python`)
- **HEROKU_API_KEY** — your Heroku account API key, found under **Account Settings > API Key** in the Heroku dashboard

![CircleCI project settings page showing the Environment Variables section with HEROKU_APP_NAME and HEROKU_API_KEY configured](/images/site-mirror/81e8776545dedacce2780142298f4f7da46774c2-1600x889.webp)

### Step 8. Trigger the build

As soon as you merge the pull request, CircleCI triggers the pipeline automatically. You can monitor the build progress in the CircleCI dashboard.

![CircleCI dashboard showing the pipeline run with a successful build and deploy job](/images/site-mirror/8637a0e3a54820306e8d105cd5501afbc92cc704-1600x814.webp)

Once the build completes, your application is deployed. The Heroku build log confirms a successful deployment:

```bash
remote:        Installing collected packages: ...
remote:        Successfully installed Django-4.0.3 redis-4.2.0 ...
remote: -----> Discovering process types
remote:        Procfile declares types -> web
remote: -----> Compressing...
remote:        Done: 75.3M
remote: -----> Launching...
remote:        Released v11
remote:        https://rate-limit-python.herokuapp.com/ deployed to Heroku
```

![Browser view of the deployed Redis rate limiting application running on Heroku](/images/site-mirror/ab52c1f2398a3977f29cb116e47dda8c4e300064-1518x1016.webp)

## Next steps

- Learn how to set up [Argo CD for Redis CI/CD](/tutorials/operate/ci-cd/argo-cd/) as an alternative GitOps-based deployment approach
- Explore the [CircleCI orb registry](https://circleci.com/developer/orbs) for reusable Redis-related configurations
- Read the [Redis Docker Hub page](https://hub.docker.com/_/redis) to find official images for your CircleCI pipelines
