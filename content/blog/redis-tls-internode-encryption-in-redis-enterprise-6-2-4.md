---
title: "Redis TLS – Internode Encryption in Redis Enterprise 6.2.4"
linkTitle: "Redis TLS – Internode Encryption in Redis Enterprise 6.2.4"
url: "/blog/redis-tls-internode-encryption-in-redis-enterprise-6-2-4/"
description: "Redis Enterprise 6.2.4 introduced internode encryption. The scope of internode encryption in Redis Enterprise is to achieve TLS encryption for all internal Redis cluster connections between nodes,..."
date: 2022-05-19
blogCategories:
- "Tech"
authors:
- "Brandon Felker"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Brandon Felker, Contributor · Published 19 May 2022 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/75ed0055a3331176e223ebd163657c388c58573f-772x550.webp)

[Redis Enterprise 6.2.4](https://docs.redis.com/latest/rs/release-notes/rs-6-2-4-august-2021/) introduced internode encryption. The scope of internode encryption in Redis Enterprise is to achieve TLS encryption for all internal Redis cluster connections between nodes, including:

1. Enhancing control plane connections to encrypt CCS (Cluster Configuration Store) replication.
1. All connections to primary node CCS from replica nodes.
1. Data plane connections to encrypt shard replication between nodes.
1. All proxy to shard connections between nodes.

![](/images/site-mirror/bd573d2826a32720f525f433b6385ac90b40de25-1024x909.webp)

## Redis Enterprise: Design Considerations

Redis Enterprise uses several techniques to optimize performance and availability. The Redis cluster uses a shared-nothing architecture, which increases reliability and availability and makes it easy to add and remove nodes. When approaching the requirement to encrypt all internode connections, the team focused on availability and operational simplicity.

A distributed, always-on system such as Redis Enterprise powers many mission-critical applications. It is required to meet the highest standard of operational availability. [Redis Cloud](/redis-enterprise-cloud/overview/), powered by Redis Enterprise, provides 99.999% availability, meaning it can only be down for a few minutes a year. Internode cluster communications are critical to maintaining quorum (control path operations) and enabling [Redis replication](/redis-enterprise/technology/highly-available-redis/) (data path operation). Therefore, it is imperative to have high availability to maintain the reliability of internode communications at all times.

## What is a Private Certificate Authority (CA)?:

A **Private Certificate Authority (CA)** is a cluster-specific certificate authority that functions like a publicly-trusted CA. The Redis cluster creates its own private root certificate which can issue other private certificates for each node. Private certificates issued by a Private CA are not publicly trusted. The Private CA is not exposed outside of the cluster. The Private CA is not shared between Redis clusters, or with any external client or service. The certificates signed by the Private CA (end-entity certificates) are exclusive to the node they are issued to.

The Private CA utilized in Redis Enterprise provides a seamless internal self-rotation mechanism. Certificate rotation will be accomplished automatically prior to expiration. Certificate rotation can also be accomplished upon request through the REST API. Alerting will also be provided for monitoring by application, database, and security teams. The Private CA removes the dependency on an external CA availability for certificate rotation, removing a potential point of failure and improving the overall availability of the cluster.

Redis Enterprise achieves this through the use of a Private Certificate Authority (CA) to manage the certificates required for internode encryption. Customers typically have the following primary concerns associated with the use of a Private CA.

### Customer Concerns:

1. No self-signed certificates or Private CA’s are allowed in our environment.
1. A Private CA is not publicly trusted and therefore cannot establish trust for external communication.
1. Private CA’s are often not adequately protected against compromise.

The first concern really isn’t a security concern. This is a compliance requirement. Many organizations have written blanket policies to disallow self-signed certificates entirely without considering valid use cases where a self-signed certificate is the best option. This requirement makes sense for many instances, but not all, and has caused those same organizations to require in-depth processes to grant exclusions for instances where the blanket policy does not fit. One example is Redis Enterprise internode encryption. In this specific example, a Private CA serves a specific purpose.

First, let’s define a **self-signed certificate**. A self-signed certificate is one that is not signed by a publicly trusted third-party CA. This type of certificate is created, issued, and signed by the organization responsible for the website or application the certificate is issued for. These certificates are free to issue and use the same ciphers as certificates issued by a trusted third-party CA.

You may ask yourself: “If an organization does not allow the use of self-signed certificates, what is the alternative?” The typical alternative is to use certificates that have been issued by a trusted third-party CA. An organization can purchase these certificates from many different third parties trusted CA’s and then issue the certificates to their website or application. A certificate issued by a trusted third-party CA is the same as a self-signed certificate as far as security is concerned.

The next question we should ask is – What, difference, if any, is there between a self-signed certificate and a certificate issued by a trusted third-party CA? Each certificate supports the same ciphers. Each consists of root, intermediate, and leaf certificates. Each can also be expired or revoked as needed. The only difference is a functional difference between a self-signed certificate and a certificate issued by a trusted third-party CA. That function is trust. A trusted third-party CA can issue certificates that can be used to establish trust between two unrelated entities.

When is trust required? Trust is a required part of the solution when two unrelated entities are communicating. A good example of this is the communication between a web browser and a web application. Using a third-party trusted CA-issued certificate allows for encrypted communication but also lets the web browser know that the web application is indeed who they present itself to be. As a result, the browser will prompt the user if they trust the web application and want to continue the communication.

**When is trust not required?** Trust is not a required part of the solution when two related entities are communicating. Redis Enterprise’s internode encryption is a good example of this type of communication. Redis Enterprise consists of one cluster, and a single cluster can contain multiple nodes. There can be single or multiple databases on a node, as well. Because each node belongs to the same cluster, no third party is required to establish trust. Each node already trusts every other node because they belong to the same cluster.

### Redis Enterprise Solution:

Redis Enterprise mitigates these compliance and security concerns because the Private CA-generated certificates are only used within the cluster. Because each of the nodes are known and trusted by all other nodes within the same cluster, a third-party trusted CA adds nothing and is not required to establish trust within the Redis cluster.

---
