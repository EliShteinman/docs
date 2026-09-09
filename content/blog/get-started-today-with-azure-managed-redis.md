---
title: "Get started today with Azure Managed Redis"
linkTitle: "Get started today with Azure Managed Redis"
url: "/blog/get-started-today-with-azure-managed-redis/"
description: "Late last year, Redis and Microsoft announced Azure Managed Redis (public preview) , a fully-managed, scalable, in-memory data store that gives Azure developers everything they need to build high-..."
date: 2025-04-21
blogCategories:
- "Tech"
authors:
- "Purna  Mehta"
lastmod: 2026-08-13
hidden: true
---

*By Purna  Mehta, Senior Product Manager · Published 21 April 2025 · updated 13 August 2026*

![Blog tile image](/images/site-mirror/653a979558e5537fa55ec6af031a8304102b6120-772x552.webp)

Late last year, Redis and Microsoft announced [Azure Managed Redis (public preview) ](https://azure.microsoft.com/en-us/products/managed-redis/), a fully-managed, scalable, in-memory data store that gives Azure developers everything they need to build high-performing, reliable and secure apps. Azure Managed Redis supports both traditional caching and caching for AI apps and workloads, offering vector data structures and vector search, alongside secondary indexing for full-text search, exact matching, geospatial queries, numeric data handling, and fast data processing. Today, we’ll take a deeper look at some of the benefits Azure Managed Redis offers, and walk you through how to get started Azure Managed Redis builds on our existing integration with Microsoft Azure on the Enterprise and Enterprise Flash tiers for Azure Cache for Redis. Customers that migrate from any Azure Cache for Redis tier get higher throughput and more cost savings at equivalent memory sizes as well as simplified deployment workflow, secure-by-default approach, and deep integration within the Microsoft Azure ecosystem.

*You can create a cache within minutes starting*
*as low as 500MB for less than $12 per month. *[*Try it now.*](https://login.microsoftonline.com/organizations/oauth2/v2.0/authorize?redirect_uri=https%3A%2F%2Fms.portal.azure.com%2Fsignin%2Findex%2F&response_type=code%20id_token&scope=https%3A%2F%2Fmanagement.core.windows.net%2F%2Fuser_impersonation%20openid%20email%20profile&state=OpenIdConnect.AuthenticationProperties%3DYyw5PUPBFn3-I_um5kXZnSinMOVZDwnVXH7Pp-jO32TEjqnjWxNxf6vZIGWnPPlfpIjZU4qof0N5vm_qMkqeGtdqA-1U_oo3BLCEPrIBNdEUOgnWbiUPsht1eXIUuN13nBZeGS6p_M-Cx4B-SFEAcTgvt2aYj_wKdbj9wdWtJZMt6wGlDC0y0xlFMEjlHeQ_SxyKXhNK1TG7WrakuX-_W7_TL8MZ87P68mvnPf7XqBKxonB2r8aZ8eORsS6liC2f-_5tjbdMYdoE4Pa0vTjquoX4Msg1oHmpvaaUmNVgDSYCz5T9VpEuaWt5bW7heLTYi5S8CZXFdUqgERcjoydZWRLRcnSLKXWuT2D1vSgTNvwuFnVTnQfJcf3fOZy5BV1gwRg5pJrBszAOnPNM0FyMq27prgKoIZuMZaR6Vf5hSz28q2vMpUYOFUJtpQC9NubBJvMoNzs6bdekoJ8AFnnjK9gMBYh3BPfUK2yQ1oTbHi8NzAKBJ4Iu0tOKJ8nrjvPd579opunrOR0hvhA80JWVqA&response_mode=form_post&nonce=638808655982921187.ZGRhZTI2MGEtZGQyNy00ZWYxLWI4NjItMmZiN2M0MzQ2YjMyZTk4MmQxYjUtNmYyYy00YTgyLWE4YzYtMjc5OWVkMzhhZTk0&client_id=c44b4083-3bb0-49c1-b47d-974e53cbdf3c&site_id=501430&client-request-id=2b88f97f-7d2b-430e-8de1-d8a495ca96c7&x-client-SKU=ID_NET472&x-client-ver=8.3.0.0&sso_reload=true)

### Simplified deployment workflow

The simplified deployment workflow is achieved with a simplified SKU structure, based on different performance requirements that customers have from their workloads. For example, memory intensive workloads can choose Memory Optimized SKU, while compute intensive workloads can use Compute Optimized SKU. There are also balanced SKUs which provide a healthy balance of memory and compute resources and Flash Optimized SKU for cost-effective scaling of caches with large datasets. This ensures that all features are available across all SKUs, eliminating the complexity of navigating different tiers for specific capabilities. Customers can choose a SKU based on their workload and network requirements, making the selection process straightforward. Scaling operations are seamless—whether you need more resources or increased capacity, you don’t have to worry about deciding between scaling up or scaling out. [Scaling operations](https://learn.microsoft.com/en-us/azure/redis/how-to-scale) are available directly through the portal and API, allowing for a streamlined approach. This reduces friction in both procurement and operations, enabling effortless growth as your needs evolve.

### Secure-by-default approach

Azure Managed Redis supports password-free authentication via Microsoft Entra ID, alongside traditional access keys. While access keys are simple, they come with security and management challenges. With Entra ID integration, you can authenticate using a service principal or managed identity, ensuring a more secure and seamless experience. Additionally, TLS is enabled on all caches by default for both internal connections as well as client connections to the Redis instance. Azure Managed Redis also integrates seamlessly with Azure Networking resources like VNET, Subnet, and Private Endpoints to provide security at all layers of the application.

### Deep integration within the Microsoft Azure ecosystem

Being a first-party service, it seamlessly [integrates with key Azure services like Azure SQL](https://www.linkedin.com/pulse/creating-scalable-apis-azure-cache-redis-enterprise-roberto-perez-ofwlf/), Azure Cosmos DB, Azure Log Analytics, and platforms like Azure AI Foundry, enabling optimized “better together” workflows for enhanced performance and efficiency. With built-in consumption and utilization tracking, billing is more transparent and frictionless, ensuring a streamlined experience.

Additionally, [broad availability across regions](https://learn.microsoft.com/en-us/azure/redis/migrate/migrate-overview#regional-availability-for-azure-managed-redis) ensures that organizations can deploy and operate securely, no matter their compliance or sovereignty requirements. Our teams are collaboratively and actively working on region and cloud expansions. If there is a region you really need, please talk to your Microsoft account team and share your feedback.

### Try it out now

Note that Azure Managed Redis is currently in public preview and you can sign up now to learn how it enables building faster agents in a [live webinar](https://events.redis.io/ai-agents-amr) on April 22. In the meantime, check out the detailed [documentation](https://learn.microsoft.com/en-us/azure/redis/overview) on the official Microsoft Learn website. Once you have familiarized yourself with Azure Managed Redis, you can create a new cache within minutes by using the Azure portal, Azure CLI, Azure API and also using [Infrastructure as Code tools](https://www.linkedin.com/pulse/simplifying-azure-managed-redis-deployment-code-iac-examples-perez-dmm2c/). Below is an example workflow of creating a new cache using the Azure portal:

1. Navigate to the Azure portal, click on “Create a resource”

![](/images/site-mirror/85a035e68b47b6bb5f4a815206dcbcdec746e693-2037x1279.webp)

1. Search for Azure Managed Redis, select the correct tile and click on “Create” which takes you to the basic configuration for deployment.

![](/images/site-mirror/5ef23cca915e75115694dd1306a6663596e02dd1-2046x1271.webp)

1. Fill out the form and to learn more about each of the form fields, check out the official documentation.

![](/images/site-mirror/43a870d2e8df4d3dd81df04aa57aa24c98ca9ada-2041x1279.webp)

![](/images/site-mirror/d4352ce9b223d38aa784c8a0d7c1b61401e5bdfb-2041x1279.webp)

![](/images/site-mirror/087e014ba652b9e1ca537cbc0b96d51cd27cf0ca-2048x1275.webp)

![](/images/site-mirror/087e014ba652b9e1ca537cbc0b96d51cd27cf0ca-2048x1275.webp)

![](/images/site-mirror/86bc400df07eda0d0c660130f86be7831298558d-2038x1278.webp)

![](/images/site-mirror/95e9671e5a328d30f606a4592da1bcb1aaf14676-2044x1278.webp)

![](/images/site-mirror/6678d82bd20bfb5117d4faa45890fda1e9639bc3-2043x1277.webp)

1. After you review and create the service, it takes a few minutes to deploy the Azure Managed Redis instance. You can track the progress in the Activity Log and you will be able to see a message when it is created successfully.

![](/images/site-mirror/e27eac7f9e410b582214fd71b45d46651cfd4113-2045x1276.webp)

1. Microsoft Entra authentication is the recommended way to connect with Azure Managed Redis. However, for the purposes of this demo, we will use Access Keys for authentication. Note down the endpoint and connection information from the portal. We will use this information in the subsequent steps to connect to this Redis instance using Redis Insights.

![](/images/site-mirror/bf9682c6a7c823d59a76ac49ba0dac49964d750d-2044x1278.webp)

![](/images/site-mirror/fbdbaf7a612df901e4ced0361deafa7abe0b48fc-2047x1277.webp)

1. Now open the Redis Insights application and configure the connection details. Also note that TLS is enabled by default, so you must enable TLS from Redis Insights as well.
1. Once connected successfully, you will see that the newly created cache is empty. You can use the tools with Redis Insights to quickly populate the cache with some data.

![](/images/site-mirror/c99ca90d31bbed6bc5224646b6554bb19e812a5f-1080x608.gif)

1. In this demo, we will use the Import feature and use an .rdb file to populate the cache.

![](/images/site-mirror/c2e18de2a32e708a8c33aca20dbd992e708890bf-2045x1278.webp)

![](/images/site-mirror/89bb005b8451af3ce67059e73404eab444c3365f-2040x1278.webp)

![](/images/site-mirror/d9d60ff3290d699ccc70f9fe52c50888ea65e625-2043x1279.webp)

1. Once the import is complete, you will see a message on the Portal and see the data in Redis Insights.

![](/images/site-mirror/946a54a4b98af7884dc7db364e90bdd65b97397d-2044x1277.webp)

![](/images/site-mirror/4a3e98ca79ada60344681a44839134d2f3d1b3c4-2044x1277.webp)

### Share your feedback

If you’re already using Azure Managed Redis, we’d love to hear from you. Please take a moment and [**fill out this online survey**](https://forms.gle/Jf9c81cWy4LrFBgHA). We would appreciate your insights.
