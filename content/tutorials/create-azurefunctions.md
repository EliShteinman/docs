---
title: "Getting Started with Azure Functions and Redis"
linkTitle: "Getting Started with Azure Functions and Redis"
url: "/tutorials/create/azurefunctions/"
description: "Azure Functions is an event-based, serverless compute platform offered by Microsoft to accelerate and simplify serverless application development. It allows developers to write less code, build and..."
group: "For developers"
aliases:
- "/tutorials/create-azurefunctions/"
date: 2026-02-25
lastmod: 2026-02-26
hidden: true
---

*Published 25 February 2026 · updated 26 February 2026*

> **TL;DR:**
>
> Connect Azure Functions to Azure Cache for Redis to build serverless applications with fast caching and data access. Set up a Redis cache instance on Azure, configure your connection string, and call Redis from a C# Azure Function to store and query data — no server management required.

![Azure Functions and Redis logos side by side](/images/site-mirror/156c11f1d23aa5ac240010f06b0f9cb8ab221b2d-1047x1040.webp)

## What you'll learn

- How to create and configure an Azure Cache for Redis instance
- How to connect an Azure Function to Redis using a connection string
- How to build and run a C# Azure Function that reads and writes Redis data
- How to seed data into Redis and query it with Redis Insight
- How to use Redis probabilistic data structures (Count-Min Sketch) from a serverless function

## Prerequisites

- A [Microsoft Azure account](https://azure.microsoft.com/free/) with an active subscription
- [Visual Studio Code](https://code.visualstudio.com/) installed
- [Azure Functions Core Tools v4](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-tools?tabs=v4) installed
- [.NET 6 SDK](https://dotnet.microsoft.com/download/dotnet/6.0) or later
- [redis-cli](https://redis.io/docs/latest/develop/tools/cli/) for verifying connectivity
- Basic familiarity with C# and [.NET Redis development](/tutorials/develop/dotnet/)

---

[Azure Functions](https://azure.microsoft.com/en-in/services/functions/) is an event-based, serverless compute platform offered by [Microsoft](https://azure.microsoft.com/en-in/blog/microsoft-named-a-leader-in-forrester-wave-functionasaservice-platforms/) to accelerate and simplify serverless application development. It allows developers to write less code, build and debug locally without additional setup, and deploy and operate at scale in the cloud.

### How do Azure Functions work?

[Azure Functions](https://github.com/Azure/Azure-Functions) allows you to implement your system's logic into readily available blocks of code. These code blocks are called "functions." [An Azure function's execution is triggered](https://docs.microsoft.com/en-us/learn/modules/execute-azure-function-with-triggers/) when an event is fired. Whenever demand for execution increases, more and more resources are allocated automatically to the service, and when requests fall, all extra resources and application instances drop off automatically. In short, as a developer, you can now focus on the pieces of code that matter most to you, and Azure Functions handles the rest.

Azure Functions [provides as many or as few compute resources as needed](https://docs.microsoft.com/en-us/azure/azure-functions/functions-scale) to meet your application's demand. Providing compute resources on-demand is the essence of [serverless computing](https://azure.microsoft.com/solutions/serverless/) in Azure Functions.

### What are the benefits of Azure Functions?

- Azure Functions provides automated and flexible scaling.
- It allows you to build, debug, deploy, and monitor with integrated tools and built-in DevOps capabilities.
- It [supports a variety of programming languages](https://docs.microsoft.com/en-in/azure/azure-functions/supported-languages#languages-in-runtime-1x-and-2x) such as C#, Java, JavaScript, Python, and PowerShell.
- It allows you to use Functions extensions on Visual Studio and Visual Studio Code for faster and more efficient development on your local system.
- With Azure Functions you can set up CI/CD with Azure Pipelines.
- It's a great solution for processing bulk data, integrating systems, working with IoT, and building simple APIs and microservices.
- It's used to break monolithic architectures into loosely coupled functions.
- It allows you to [deploy Functions to Kubernetes](https://docs.microsoft.com/en-us/azure/azure-functions/functions-kubernetes-keda).

In this tutorial, you will learn how to get started with Azure Functions and Redis.

### Getting started

- Step 1. Log in to Microsoft Azure Portal
- Step 2. Set up Azure Cache for Redis
- Step 3. Configure Keys for Redis Cache
- Step 4. Verify if Redis database is reachable remotely
- Step 5. Install Homebrew on Mac
- Step 6. Install Visual Studio Code
- Step 7. Install the Azure Functions Core Tools
- Step 8. Install the Azure Functions extension for Visual Studio Code
- Step 9. Connect Azure Function to Azure account
- Step 10. Clone the project repository
- Step 11. Trigger the function
- Step 12. Verify the Azure Functions app is working properly
- Step 13. Seed the Redis database
- Step 14. Run query using Redis Insight

### Step 1. Log in to Microsoft Azure Portal

Create an Azure account with an active subscription by clicking this link: [Create an account for free](https://azure.microsoft.com/free/).

![Microsoft Azure Portal login and subscription page](/images/site-mirror/5a03fab0e7dcb637a27d27bbdff54f6acdd01281-1047x701.webp)

### Step 2. How do you set up Azure Cache for Redis?

Type "Azure Cache for Redis" in the search section and select the service:

![Searching for Azure Cache for Redis in the Azure Portal search bar](/images/site-mirror/8c5088332ed1efb8e950351019ee8a7d95f24639-1047x685.webp)

Under "New Redis Cache" window, create a new resource group, select your preferred location and cache type:

![Configuring a new Azure Cache for Redis instance with resource group, location, and cache tier](/images/site-mirror/06a3544970594dd634cbe2abea5afbf126f9977b-1047x958.webp)

Once you are done with the entries, click "Review + Create" button.

![Review and Create confirmation page for the Azure Cache for Redis deployment](/images/site-mirror/a1b1bbce2628f7eb062a171eafea4a4d5b300b36-1047x417.webp)

Once the deployment is complete, you will be provided with the deployment name, subscription details and resource group.

![Deployment complete status page showing Azure Cache for Redis resource details](/images/site-mirror/a17730d830338485e09b8db7ecf9e32b54b02992-1047x541.webp)

![Resource group overview showing the deployed Redis Cache and related Azure resources](/images/site-mirror/72aefd2653912cd5845c67abe2ce67814f1d703d-717x346.webp)

For a more detailed walkthrough of creating a Redis instance on Azure, see [Create Redis database on Azure Cache](/tutorials/create/azure/portal/) or [Create a database using Azure Cache for Redis Enterprise](/tutorials/create/cloud/azure/).

### Step 3. How do you configure access keys for Redis Cache?

You will need keys to log in to the Redis database. Click "Overview" option in the left sidebar to see the Primary key and save it for future reference.

### Step 4. How do you verify that Redis is accessible remotely?

```bash
redis-cli -h demorediss.redis.cache.windows.net -p 6379
demorediss.redis.cache.windows.net:6379> info modules
NOAUTH Authentication required.
demorediss.redis.cache.windows.net:6379> auth jsn9IdFXXXXXXXXXXXXXsAzCaDzLh6s=
OK
demorediss.redis.cache.windows.net:6379> get a1
"100"
```

### Step 5. Install Homebrew on Mac

Install the Homebrew package manager by running this script:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 6. Install Visual Studio Code

Visual Studio Code is a lightweight but powerful source code editor that runs on your desktop and is available for Windows, macOS, and Linux. It comes with built-in support for JavaScript, TypeScript, and Node.js, and has a rich ecosystem of extensions for other languages (such as C++, C#, Java, Python, PHP, Go) and runtimes (such as .NET and Unity). Begin your journey with VS Code with these [introductory videos](https://code.visualstudio.com/docs/introvideos/overview).

![Visual Studio Code editor welcome screen](/images/site-mirror/e859e1ec461704fd8fb7e8c7d170c6d3006e60e4-1047x666.webp)

### Step 7. Install the Azure Functions Core Tools

```bash
brew tap azure/functions
brew install azure-functions-core-tools@4
# if upgrading on a machine that has 2.x or 3.x installed:
brew link --overwrite azure-functions-core-tools@4
```

### Step 8. Install the Azure Functions extension for Visual Studio Code

Use the Azure Functions extension to quickly create, debug, manage, and deploy serverless apps directly from VS Code.

![Azure Functions extension listing in the VS Code marketplace](/images/site-mirror/5ff79fef837be5b1cb4ee4dc5846b8adf35525ad-1047x830.webp)

### Step 9. How do you connect an Azure Function to your Azure account?

![Signing in to Azure from VS Code using the Azure Functions extension](/images/site-mirror/c05222df3b4f98e84669a1b47741fb5957739190-1047x853.webp)

### Step 10. How do you connect an Azure Function to Redis?

For this tutorial, we will be using a baby names counter app built using C#. To get started, we will first clone the repository:

```bash
git clone https://github.com/redis-developer/Baby-Names-Func
```

Add "Azure Cache for Redis" endpoint URL details in the `local-settings.json` file as shown below:

```bash
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "dotnet"
    "redisCacheConnectionString": "demorediss.redis.cache.windows.net"

  }
}
```

Open the project with Visual Studio Code by running the following command:

```bash
cd Baby-Names-Func
code .
```

This will open VS Code. The function will automatically load into the plugin.

![Baby Names Azure Function project loaded in VS Code with the Azure Functions plugin](/images/site-mirror/ddd9bfe0f9a8c06dbb975f513c92bb57d811a7bb-1047x638.webp)

### Step 11. How do you trigger and run an Azure Function locally?

Press F5 to automatically execute the function.

![Terminal output showing the Azure Function starting locally on port 7071](/images/site-mirror/d40d0081423c1055827d23aa70968a9a18300827-1047x637.webp)

If you want to manually select the repository, choose .NET framework, etc., and then click "Create new project."

![Creating a new Azure Functions project with the .NET runtime in VS Code](/images/site-mirror/f30f79c9e55be64f193afc2d2d67dca4ab9cb088-1047x636.webp)

You will find the following output under VS Code screen:

```bash
     1>Done Building Project "/Users/ajeetraina/projects/Baby-Names-Func/RedisFunctions.csproj" (Clean target(s)).

Terminal will be reused by tasks, press any key to close it.

> Executing task: dotnet build /property:GenerateFullPaths=true /consoleloggerparameters:NoSummary <

Microsoft (R) Build Engine version 17.0.0+c9eb9dd64 for .NET
Copyright (C) Microsoft Corporation. All rights reserved.

  Determining projects to restore...
  All projects are up-to-date for restore.
  RedisFunctions -> /Users/ajeetraina/projects/Baby-Names-Func/bin/Debug/net6.0/RedisFunctions.dll

Terminal will be reused by tasks, press any key to close it.

> Executing task: func host start <

Azure Functions Core Tools
Core Tools Version:       4.0.3971 Commit hash: d0775d487c93ebd49e9c1166d5c3c01f3c76eaaf  (64-bit)
Function Runtime Version: 4.0.1.16815

[2022-03-01T07:51:01.383Z] Found /Users/ajeetraina/projects/Baby-Names-Func/RedisFunctions.csproj. Using for user secrets file configuration.

Functions:

        CountBabyNames: [GET,POST] http://localhost:7071/api/getCount

        IncrementBabyName: [GET,POST] http://localhost:7071/api/increment

For detailed output, run func with --verbose flag.
```

### Step 12. Verify the Azure Functions app is working properly

![Browser showing the Azure Functions app running successfully at localhost](/images/site-mirror/5d6c13ebba186b8cbbb8a3d46501354af3056074-1047x752.webp)

### Step 13. How do you seed data into Redis from an Azure Function?

Now, let us seed BabyNames data into the Redis database.

```bash
git clone https://github.com/slorello89/Seed-Baby-Names
```

If you connect to the Redis database and run the `MONITOR` command, you should see the data being inserted into the database as shown below:

```bash
1646061655.966050 [0 122.171.48.244:60531] "CMS.INCRBY" "baby-names" "Rowen" "1"
1646061655.966050 [0 122.171.48.244:60531] "SELECT" "0"
1646061655.966050 [0 122.171.48.244:60531] "CMS.INCRBY" "baby-names" "Titus" "1"
1646061655.966050 [0 122.171.48.244:60531] "SELECT" "0"
1646061655.966050 [0 122.171.48.244:60531] "CMS.INCRBY" "baby-names" "Braxton" "1"
1646061655.966050 [0 122.171.48.244:60531] "SELECT" "0"
1646061655.966050 [0 122.171.48.244:60531] "CMS.INCRBY" "baby-names" "Alexander" "1"
1646061655.966050 [0 122.171.48.244:60531] "SELECT" "0"
1646061655.966050 [0 122.171.48.244:60531] "CMS.INCRBY" "baby-names" "Finnegan" "1"
1646061655.966050 [0 122.171.48.244:60531] "SELECT" "0"
1646061655.966050 [0 122.171.48.244:60531] "CMS.INCRBY" "baby-names" "Nasir" "1"
1646061655.966050 [0 122.171.48.244:60531] "SELECT" "0"
1646061655.966050 [0 122.171.48.244:60531] "CMS.INCRBY" "baby-names" "Fabian" "1"
1646061655.966050 [0 122.171.48.244:60531] "SELECT" "0"
1646061655.966050 [0 122.171.48.244:60531] "CMS.INCRBY" "baby-names" "Alexander" "1"
1646061655.966050 [0 122.171.48.244:60531] "SELECT" "0"
1646061655.966050 [0 122.171.48.244:60531] "CMS.INCRBY" "baby-names" "Emilio" "1"
1646061655.966050 [0 122.171.48.244:60531] "SELECT" "0"
1646061655.966050 [0 122.171.48.244:60531] "CMS.INCRBY" "baby-names" "Dax" "1"
1646061655.966050 [0 122.171.48.244:60531] "SELECT" "0"
1646061655.966050 [0 122.171.48.244:60531] "CMS.INCRBY" "baby-names" "Johnny" "1"
1646061655.966050 [0 122.171.48.244:60531] "SELECT" "0"
1646061655.966050 [0 122.171.48.244:60531] "CMS.INCRBY" "baby-names" "Mario" "1"
1646061655.966050 [0 122.171.48.244:60531] "SELECT" "0"
1646061655.966050 [0 122.171.48.244:60531] "CMS.INCRBY" "baby-names" "Lennox" "1"
```

### Step 14. How do you query Redis data with Redis Insight?

Set up Redis Insight on your local system and get connected to the Redis database. Once connected, you should be able to run the following queries:

![Redis Insight showing CMS.INFO and CMS.QUERY results for the baby-names Count-Min Sketch](/images/site-mirror/addee9e745d371da0cb205e63ecaf46dff769cde-1047x686.webp)

```bash
> CMS.INFO baby-names
1) width
2) (integer) 1000
3) depth
4) (integer) 10
5) count
6) (integer) 100000

> CMS.QUERY baby-names Johnny
1) 109
```

### Next steps

Now that you have Azure Functions connected to Redis, explore these related tutorials:

- [Create Redis database on Azure Cache](/tutorials/create/azure/portal/) — set up a standalone Azure Cache for Redis instance
- [Create a database using Azure Cache for Redis Enterprise](/tutorials/create/cloud/azure/) — provision an Enterprise-tier Redis database on Azure
- [.NET and Redis](/tutorials/develop/dotnet/) — learn the StackExchange.Redis client for .NET applications
