---
title: "Deploy and Manage Redis Enterprise Cloud With Pulumi"
linkTitle: "Deploy and Manage Redis Enterprise Cloud With Pulumi"
url: "/blog/redis-cloud-supports-pulumi/"
description: "Redis Cloud is now supported by Pulumi, an infrastructure as code (IaC) platform that allows developers to manage cloud resources using familiar programming languages. With Redis Cloud and Pulumi,..."
date: 2023-05-16
blogCategories:
- "Uncategorized"
authors:
- "Noam Stern"
lastmod: 2025-03-27
hidden: true
---

*By Noam Stern, Sr. Product Manager, Products · Published 16 May 2023 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/676937211117dcd0a61f3c035cf1e36c88fdee73-772x552.webp)

**Redis Cloud is now supported by Pulumi, an infrastructure as code (IaC) platform that allows developers to manage cloud resources using familiar programming languages. With Redis Cloud and Pulumi, you can automate the creation and configuration of Redis Cloud resources and ensure consistency across environments.**

[Pulumi](https://www.pulumi.com/) is a cloud-native IaC platform that lets developers define and manage cloud resources using their favorite programming languages, including [Node.js](/blog/redis-om-node-js/), [Python](/blog/introducing-redis-om-for-python/), Go, C#, and YAML. Pulumi offers a consistent, composable, and reusable way to manage resources that can be version-controlled and shared with others.

When you use Pulumi with Redis, you can automate the creation and configuration of[ Redis Cloud](/redis-enterprise-cloud/overview/) resources; doing so lets you spend less time on manual tasks and more time building your applications. Pulumi also provides testing and validation tools to ensure infrastructure reliability. You can write tests to validate a Redis Cloud configuration and catch errors before they cause problems in production.

The Redis Cloud provider for Pulumi is built as a [bridge provider](https://github.com/pulumi/pulumi-terraform-bridge#pulumi-terraform-bridge) through [Terraform](https://registry.terraform.io/providers/RedisLabs/rediscloud/latest/docs). It provides the same functionality as the Terraform provider but with the added benefits of using Pulumi.

Want to see what’s possible? Here’s a step-by-step walkthrough to show how to create your first Redis resource using Pulumi.

## Managing a Redis Cloud provider with Pulumi

Before you get underway, [install Pulumi](https://www.pulumi.com/docs/get-started/install/)[.](https://www.pulumi.com/docs/get-started/install/.) And then…

**Set up a Pulumi project and install the Redis Cloud provider package** for your chosen language; in this example, it’s Python. You can do this by creating a new directory and running the following commands:

```bash
$ mkdir my-redis-project
$ cd my-redis-project
$ pulumi new rediscloud-python

```

You will be asked to provide the configured credit card details and the Redis Cloud credentials as part of the Redis Cloud provider package installation.

[Watch the video](https://www.pulumi.com/learn/building-with-pulumi/secrets/)

The setup is done!

This creates a new Pulumi project with a basic file structure.

**Write the Pulumi code**. Now it’s time to write the Pulumi code to create and configure a Redis Cloud subscription and database in the __main__.py file that was created as part of the previous step.

This shows what the code might look like in Python:

```python
import pulumi
import pulumi_rediscloud

config = pulumi.Config()

# The configured credit card details
card = pulumi_rediscloud.get_payment_method(
    card_type=config.require("cardType"),
    last_four_numbers=config.require("lastFourNumbers"),
)

# Creating a Redis Cloud subscription
subscription = pulumi_rediscloud.Subscription(
    "my-subscription",
    name="my-subscription",
    payment_method="credit-card",
    payment_method_id=card.id,
    cloud_provider=pulumi_rediscloud.SubscriptionCloudProviderArgs(
        regions=[
            pulumi_rediscloud.SubscriptionCloudProviderRegionArgs(
                region="us-east-1",
                multiple_availability_zones=True,
                networking_deployment_cidr="10.0.0.0/24",
                preferred_availability_zones=["use1-az1", "use1-az2", "use1-az5"],
            )
        ]
    ),
# The creation_plan block below allows the API server to create an optimized infrastructure for your databases in the cluster. The provider uses the attributes inside it to create initial databases. Those databases are deleted automatically after provisioning a new subscription. The creation_plan block can ONLY be used for provisioning new subscriptions. The block is ignored if you make any further changes or try to import a resource. The actual databases of the subscription are defined as separate resources (see pulumi_rediscloud.SubscriptionDatabase resource below).
    creation_plan=pulumi_rediscloud.SubscriptionCreationPlanArgs(
        memory_limit_in_gb=10,
        quantity=1,
        replication=True,
        support_oss_cluster_api=False,
        throughput_measurement_by="operations-per-second",
        throughput_measurement_value=20000,
        modules=["RedisJSON"],
    ),
)

# Creating a Redis Cloud database
database = pulumi_rediscloud.SubscriptionDatabase(
    "my-db",
    name="my-db",
    subscription_id=subscription.id,
    protocol="redis",
    memory_limit_in_gb=10,
    data_persistence="aof-every-1-second",
    throughput_measurement_by="operations-per-second",
    throughput_measurement_value=20000,
    replication=True,
    modules=[
        pulumi_rediscloud.SubscriptionDatabaseModuleArgs(
            name="RedisJSON",
        )
    ],
)

# Export the private endpoint of the new database
endpoint = database.private_endpoint

```

This code assembles a Redis Cloud flexible subscription in AWS us-east-1 and a database within this subscription with 10GB of memory and 20,000 ops/sec throughput.

**Deploy the infrastructure**. Finally, you can deploy the Redis Cloud infrastructure. You accomplish this by running the following command:

```bash
$ pulumi up

```

This creates the Redis Cloud resources and saves the private endpoint URL in a variable called endpoint so you can use it in your applications.

![created resources with pulumi and redis.](/images/site-mirror/987da05ab863fb33e77d2f7d56ce7367d3a281ef-1999x972.webp)

*The resources have been created successfully!*

You can now manage your Redis cloud resources using Pulumi. That means you can add and remove Redis Cloud resources and update and delete the ones we just created.

## What’s next?

Ready to learn more? Here are your possible next steps.

- [Register for a Redis workshop on Pulumi](https://www.pulumi.com/resources/introduction-to-redis-and-pulumi/)
- [Create Redis Cloud resources with Pulumi](https://www.pulumi.com/registry/packages/rediscloud)
- [Create Redis Cloud resources with Terraform](https://registry.terraform.io/providers/RedisLabs/rediscloud/latest/docs)
