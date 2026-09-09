---
title: "Deploy Azure Managed Redis with AzAPI using Terraform"
linkTitle: "Deploy Azure Managed Redis with AzAPI using Terraform"
url: "/blog/deploy-azure-managed-redis-with-azapi-using-terraform/"
description: "Azure Managed Redis is now generally available – bringing the power of Redis Enterprise directly into the Azure ecosystem."
date: 2025-11-05
blogCategories:
- "Tech"
authors:
- "Thomas Findelkind"
lastmod: 2026-06-01
hidden: true
---

*By Thomas Findelkind, Senior Specialist Solution Architect · Published 5 November 2025 · updated 1 June 2026*

![Redis](/images/blog/426e05eb93e034e6b2992234b30314d91f77d7ac-1200x628.webp)

Azure Managed Redis is now generally available – bringing the power of Redis Enterprise directly into the Azure ecosystem.

However, as of Terraform **azure provider v4.5**, some features like **Persistence (RDB, AOF)** and **Non-Clustered mode** **are not yet supported**.

The solution? Use the **AzAPI provider** to deploy Azure Managed Redis **today** with full feature coverage — and **switch seamlessly** to the native provider once support arrives.

👉 Get started now: [tfindelkind-redis/azure-managed-redis-terraform](https://github.com/tfindelkind-redis/azure-managed-redis-terraform)

## Why Azure Managed Redis?

Azure Managed Redis combines **Redis Enterprise’s performance and modules** with **Azure’s native managed experience**.

You get:

- Enterprise-grade performance and high availability with up to 99.999% SLA*
- Native Azure billing, security, and identity integration
- Full module support: **RedisJSON**, **RediSearch**, **RedisBloom**, and **RedisTimeSeries**

This service is the evolution of Azure’s Redis offering — and the strategic path forward for Redis workloads in Azure.

* With recommended configuration of active georeplication.

## Azure Cache for Redis Retirement!

Microsoft has announced a clear transition timeline for Azure Cache for Redis:

| Date | Change |
|---|---|
| October 1, 2026 | No new Azure Cache for Redis instances can be created |
| Existing Instances | Supported until further notice |
| Recommended Path | Migrate to Azure Managed Redis for new deployments |

**In short:** New Redis deployments on Azure should use **Azure Managed Redis**, which brings Redis Enterprise features under Azure’s managed control plane.

## Why Use AzAPI with Terraform?

The azurerm provider doesn’t yet expose all capabilities of Azure Managed Redis.Until it does, the **AzAPI provider** lets you interact directly with Azure’s REST APIs through Terraform.

This approach gives you:

| Benefit | Description |
|---|---|
| Full feature access | Deploy Redis with features unavailable in azurerm 4.5 (e.g., persistence, non-clustered mode) |
| Future-proof design | Module interface remains stable — just flip one variable to migrate later |
| Direct API access | Use the latest Azure REST API versions without waiting for provider updates |
| Immediate usability | Ready-to-deploy module and tested examples available on GitHub |

## 
AzAPI vs. azurerm: Feature Comparison (as of v4.5)


| Feature | AzAPI Provider | azurerm v4.5 |
|---|---|---|
| Clustered Deployments | ✅ Supported | ✅ Supported |
| Non-Clustered Mode | ✅ Supported | ❌ Not yet supported |
| Persistence (RDB, AOF) | ✅ Supported | ❌ Not yet supported |
| Access Policy Assignments (Entra ID) | ✅ Supported | ❌ Not yet supported |
| Defer Upgrade | ✅ Supported | ❌ Not yet supported |
| Redis Modules (JSON, Search, Bloom, TimeSeries) | ✅ Supported | ✅ Supported |
| TLS / Encryption | ✅ Supported | ✅ Supported |
| High Availability | ✅ Supported | ✅ Supported |
| Geo-Replication | ✅ Supported | ✅ Supported |
| Managed Identity | ✅ Supported | ✅ Supported |
| Customer Managed Keys | ✅ Supported | ✅ Supported |
| Private Endpoint | ✅ Supported | ✅ Supported |

## Module Implementation: Deploy Azure Managed Redis Today!

To bridge the gap, this Terraform module uses **AzAPI** under the hood while maintaining the same interface that future azurerm resources will use.

### Example: Cluster and Database Definition

```sql
locals {
  redis_enterprise_api_version = "2025-05-01-preview"
}

# Cluster definition
resource "azapi_resource" "cluster" {
  count     = var.use_azapi ? 1 : 0
  type      = "Microsoft.Cache/redisEnterprise@${local.redis_enterprise_api_version}"
  name      = var.name
  location  = var.location
  parent_id = var.resource_group_id

  body = jsonencode({
    sku = { name = var.sku }
    properties = {
      minimumTlsVersion = var.minimum_tls_version
    }
  })

  tags = var.tags
}
```

### Example: Database with Persistence and Non-Clustered Mode

```sql
resource "azapi_resource" "database" {
  count     = var.use_azapi ? 1 : 0
  type      = "Microsoft.Cache/redisEnterprise/databases@${local.redis_enterprise_api_version}"
  name      = var.database_name
  parent_id = azapi_resource.cluster[0].id

  body = jsonencode({
    properties = {
      clientProtocol   = var.client_protocol
      evictionPolicy   = var.eviction_policy
      clusteringPolicy = "NoCluster"  
      persistence = {
        aofEnabled = true
        rdbEnabled = true
      }
      modules = [for m in var.modules : { name = m }]
      accessKeysAuthentication = "Enabled"
    }
  })
}
```

⚠️ Note:

Persistence and Non-Clustered only supported via AzAPI.

Non-Clustered: Limitations: ≤25 GB only

## Reading Access Keys

AzAPI allows direct key retrieval through the **List Keys API** — no scripts needed:

```sql
data "azapi_resource_action" "database_keys" {
  type        = "Microsoft.Cache/redisEnterprise/databases@${local.redis_enterprise_api_version}"
  resource_id = azapi_resource.database.id
  action      = "listKeys"
  method      = "POST"
  response_export_values = ["primaryKey", "secondaryKey"]
}
```

## Future-Proof Design: The use_azapi Switch

When azurerm adds full Managed Redis support, migration is effortless.

```sql
variable "use_azapi" {
  type    = bool
  default = true
}

```

To migrate later:

1. Update the module
1. Set use_azapi = false
1. Run terraform plan
1. Apply — same inputs, same outputs, native provider

No state migration required.

## Example Scenarios

The module includes six deployment examples:

- simple/ — Basic cluster setup
- high-availability/ — HA configuration for production
- with-modules/ — Redis modules showcase
- geo-replication/ — Cross-region replication
- enterprise-security/ — Customer Managed Keys, Managed Identity, Entra ID auth
- clusterless-with-persistence/ — Non-clustered mode with RDB + AOF persistence

👉 Explore the module and examples: [**tfindelkind-redis/azure-managed-redis-terraform**](https://github.com/tfindelkind-redis/azure-managed-redis-terraform)
