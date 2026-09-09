---
title: "Deploy Active-Active Redis Databases With Terraform"
linkTitle: "Deploy Active-Active Redis Databases With Terraform"
url: "/blog/now-you-can-deploy-active-active-redis-databases-with-terraform/"
description: "We are happy to announce that Redis Enterprise Cloud has published its Terraform resources for managing multi-region Active-Active Redis databases."
date: 2023-03-06
blogCategories:
- "Company"
- "Product Releases"
authors:
- "Noam Stern"
lastmod: 2025-03-27
hidden: true
---

*By Noam Stern, Sr. Product Manager, Products · Published 6 March 2023 · updated 27 March 2025*

![Blog tile image](/images/blog/733959faa9b5117193c27a252af6616508473307-772x550.webp)

**We are happy to announce that Redis Enterprise Cloud has published its Terraform resources for managing multi-region Active-Active Redis databases.**

Terraform is a popular, flexible open-source tool for infrastructure automation that helps DevOps configure, provision, and manage infrastructure as code (IaC). IaC lets organizations manage infrastructure (such as virtual machines, databases, load balancers, and connection topology) using a descriptive cloud operating model. Terraform makes it easier to plan and create IaC across multiple infrastructure providers using the same workflow, which aids reliability by ensuring that deployments remain consistent.

And now Redis Cloud is making it easier to work with Terraform.

## What are active-active Redis databases?

Redis Cloud Active-Active databases synchronize data across multiple geographies. This technology makes it possible for applications to write data simultaneously to any region, with the confidence of strong eventual consistency. Developers can build globally distributed applications without needing to solve complex technical challenges, such as handling cross-region write conflicts. Redis Enterprise takes care of it for you.

Active-Active databases are most valued where business requirements include disaster recovery, geographically redundant applications, and situations where it’s important to serve data closer to users’ physical locations.

## Why deploy active-active Redis with Terraform?

Managing data across multiple regions can be complicated. This is where the Redis Active-Active architecture and Terraform work together brilliantly. With Redis Cloud’s new Active-Active Terraform resources, you can create, update and delete databases in any region at a push of a button.

In addition, you can easily define different configurations in each region. For example, you can consume 50,000 ops/sec in one region while only consuming 1,000 ops/sec in another region.

## How to get started

To create an Active-Active Redis Cloud subscription in Terraform, you need to create three Terraform resources:

1. rediscloud_active_active_subscription: You use this resource to create and manage the Active-Active subscription.
1. *r*ediscloud_active_active_subscription_database: This resource is used to create and manage the database within a specified Active-Active Subscription in your Redis Enterprise Cloud Account. Use the override_region block to modify configurations such as passwords or persistence within a specific region.

1. rediscloud_active_active_subscription_regions: In this resource, you create and manage regions within the subscription. This allows Redis Enterprise Cloud to efficiently provision your subscription within each defined region in a separate block.

Specify each database’s read and write operations within every region as part of this resource.

Here is how a subscription with one database might be deployed across two regions:

```
resource "rediscloud_active_active_subscription" "subscription-resource" {
	name = "subscription-name"
	payment_method_id = xxxxxx
	cloud_provider = "AWS"
   
	creation_plan {
	  memory_limit_in_gb = 50
	  quantity = 1
	  region {
		  region = "us-east-1"
		  networking_deployment_cidr = "192.168.0.0/24"
		  write_operations_per_second = 5000
		  read_operations_per_second = 3000
	  }
	  region {
		  region = "eu-west-1"
		  networking_deployment_cidr = "10.0.1.0/24"
		  write_operations_per_second = 2000
		  read_operations_per_second = 10000
	  }
	}
}

resource "rediscloud_active_active_subscription_database" "database-resource" {
    subscription_id = rediscloud_active_active_subscription.subscription-resource.id
    name = "database-name"
    memory_limit_in_gb = 50
    global_data_persistence = "aof-every-1-second"
    global_alert {
	name = "dataset-size"
	value = 70
    }

    override_region {
    	name = "us-east-1"
    	override_global_data_persistence = "none"    	
   }
}

resource "rediscloud_active_active_subscription_regions" "regions-resource" {
	subscription_id = rediscloud_active_active_subscription.subscription-resource.id
	region {
	  region = "us-east-1"
	  networking_deployment_cidr = "192.168.0.0/24" 
	  database {
		  database_id = rediscloud_active_active_subscription_database.database-resource.db_id
               database_name = rediscloud_active_active_subscription_database.database-resource.name
		  local_write_operations_per_second = 5000
		  local_read_operations_per_second = 3000
	  }
	}
	region {
	  region = "eu-west-1"
	  networking_deployment_cidr = "10.0.1.0/24" 
	  database {
		  database_id = rediscloud_active_active_subscription_database.database-resource.db_id
               database_name = rediscloud_active_active_subscription_database.database-resource.name
		  local_write_operations_per_second = 2000
		  local_read_operations_per_second = 10000
	  }
	}
 }

```

The creation_plan block allows the API server to create a well-optimized infrastructure for databases in the cluster. The provider uses the attributes inside the block to create initial databases. Those databases are deleted after provisioning a new subscription, after which the databases defined as separate resources are attached to the subscription.

You can use the creation_plan block only for provisioning new subscriptions. The block is if you make any further changes or if you try to import the resource.

## Ready for the next step?

For more information, consult the Redis Enterprise Cloud registry documentation.

Need more help with creating your first Active-Active Redis subscription using Terraform? This video shows how to deploy your first Active-Active resources.
