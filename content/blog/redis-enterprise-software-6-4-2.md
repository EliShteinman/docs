---
title: "Redis Enterprise 6.4.2 Highlights Client Validation and Access Management Features"
linkTitle: "Redis Enterprise 6.4.2 Highlights Client Validation and Access Management Features"
url: "/blog/redis-enterprise-software-6-4-2/"
description: "In Redis Enterprise 6.4.2, we enhanced existing security features: extended client certificate validation and publish/subscribe access management. Here’s what they mean to you."
date: 2023-02-23
blogCategories:
- "Company"
- "Product Releases"
authors:
- "Adi Shtatfeld"
lastmod: 2025-03-27
hidden: true
---

*By Adi Shtatfeld, Senior Product Manager · Published 23 February 2023 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/ffee4c018d17dcb311675868068392fa6592f384-772x550.webp)

**In Redis Enterprise 6.4.2, we enhanced existing security features: extended client certificate validation and publish/subscribe access management. Here’s what they mean to you.**

All of us know how important it is to protect company data. At the top of our priority list for Redis Enterprise 6.4.2 was to add two enterprise-grade security features.

## Redis 6.4.2 enterprise-grade security features

Security is always on your minds, and it’s on ours, too.

### Mutual TLS authentication with subject validations

**Transport Layer Security** (**TLS**) is a cryptographic protocol widely used to secure communication between computer applications. One common use is a web application connecting and authenticating a server, after which all the exchanged data is encrypted before being sent over the network. TLS was proposed by the Internet Engineering Task Force (IETF), which describes it as “the core security protocol of the Internet.”

**Mutual TLS**, or mTLS, is a method used for mutual authentication. mTLS ensures that both the server and the client authenticate each other at the same time. This is achieved by the server providing a server certificate to the client and the client providing a client certificate to the server. mTLS is performed during the TLS handshake at the beginning of the session.

In Redis Enterprise, a database can be configured to use mTLS. In this case, when a client attempts to connect to the database, Redis Enterprise authenticates the client’s certificate during the TLS handshake before allowing it to connect to the database.

But what happens when several clients are all given a valid client certificate, and you want only a subset of them to access a certain database?

This is where the new feature, additional certificate validations, comes in handy.

Starting with version 6.4.2, Redis Enterprise lets you perform additional validations on authenticated client certificates.

It uses the public key certificate’s subject field, which contains additional information about the identity of the client to which the certificate belongs. This way, before allowing a client to connect to the database, Redis Enterprise performs two steps:

- The certificate is authenticated cryptographically.
- The certificate’s subject information is compared to the database’s configured list of allowed subjects. The connection is allowed only if a match is found.

For example, one of our customers, a large U.S.-based financial institution, wants to better control which clients can access which databases based on their client certificates. Their clients are all using valid client certificates but with different subject values. Once the “Additional Certificate Validations” option is enabled for a database and the list of allowed subjects is properly configured, the customer can now control which subset of client certificates can access the database.

Using mTLS in Redis Enterprise involves a few steps:

- Enable the TLS and mTLS options for a database
- Load the relevant certificate authority (CA) root or intermediate certificate for the database
- Add a list of allowed subject lines
- Select the “Additional Certificate Validations by full subject” option

![](/images/site-mirror/ecf2cf1ae0c893e886860219046bff6d91eb6da3-1228x483.webp)

### Enhanced access management for Redis ACL publish and subscribe

**Publish/subscribe** (pub/sub) is a messaging method that allows non-direct communication. A client or application can publish messages to a shared resource, and other clients/applications can subscribe to the resource and receive these messages.

In Redis, this resource is called a *channel*, and it provides a fast, lightweight, and scalable solution. Pub/sub channels operate like a radio station, meaning you need to be connected to receive the message. Their synchronous nature makes pub/sub channels useful for implementing real-time notifications, sending messages between microservices, or communicating between different parts of an application.

And naturally, the software has to protect these resources.

**Access Control List (ACL)** is a list of rules, each of which grants or denies access to resources or actions. ACLs are a powerful tool for organizations to restrict unauthorized users from accessing sensitive business information or performing unauthorized operations.

To accommodate users’ needs, Redis is continuously enhancing its ACL functionality and coverage. With the release of Redis Enterprise 6.2, ACLs were enhanced to allow and disallow access to pub/sub channels.

Why would anyone want to protect pub/sub channels? An invalid message sent to a channel disrupts the application. It may cause data corruption, data loss, or even an outage. By restricting all access and permitting only the relevant users to a specific channel, we can reduce the chance of someone accessing or sending messages when they are not supposed to, whether maliciously or unintended.

There are two primary methods for protecting resources.

The first is implicit access, where you have access to everything, and restrictions are put in place to limit access. An example of this is entry into a restaurant: anyone is allowed to come in unless someone has been placed on some type of denied entry list.

The second method is explicit grant: you do not have access unless you are granted permission explicitly. An example of this is boarding an aircraft. Nobody is allowed onto the aircraft until their credentials have been verified to allow for entry. The second method is the more secure method for protecting an asset.

This is the approach that Redis has taken, choosing to restrict all pub/sub channels except the ones you permit using ACLs. With Redis Enterprise 6.4.2, this policy can now be enforced by configuring a cluster-wide default option that applies to all the channels in all the databases. To avoid a breaking change, the 6.4.2 installation-provided value of acl-pubsub-default is permissive (allchannels) to comply with previous Redis versions. Once all databases in the cluster are in Redis version 6.2 (or higher in future versions), we recommend setting this value to “restrictive” (resetchannels).

If you are using ACLs and pub/sub channels, we recommend reviewing your databases and ACL settings. Plan to switch to restricted mode, which will be the new default of acl-pubsub-default in future Redis Enterprise releases.

## But that’s not all: More 6.4.2 features that will save you time and resources

Our emphasis in this release was the aforementioned security features. But we added more than that!

#### Generating self-signed certificates

Redis Enterprise provides self-signed TLS certificates. That allows customers who don’t use trusted CA signed certificates to use Redis Enterprise securely. Those self-signed certificates are valid for one year by default; we advise customers to renew those certificates before they expire.

We now provide a user-friendly script to create new self-signed certificates in one go. You can create new self-signed certificates quickly and easily, with no prior knowledge required. You then load these certificates into Redis Enterprise in a few simple steps.

#### Flexibility to choose what you need

Redis Enterprise offers a rich variety of services, but sometimes you don’t need all of them. Redis provides the tools to remove services so you can save memory resources and focus on what’s important to you. We recently added the ability to disable the alert manager, the service that is responsible for sending email alerts:


rladmin cluster config alert_mgr [<enabled | disabled> ]


Disabling this service can come in handy if you have an alternative alerting system. We recommend using this feature with discretion.

With Redis Enterprise 6.4.2, creating applications is faster, more efficient, flexible, and above all, safe for users throughout their journey. Download the 6.4.2 release and start a free 30-day trial today!
