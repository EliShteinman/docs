---
title: "Shipping Now: Redis Enterprise Software 6.2.18, the Most Secure Redis Software Ever"
linkTitle: "Shipping Now: Redis Enterprise Software 6.2.18, the Most Secure Redis Software Ever"
url: "/blog/redis-enterprise-software-6-2-18/"
description: "Redis Enterprise Software 6.2.18 is out! We’re delighted with this new release, which has a renewed focus on security, and we think you will be, too."
date: 2022-11-29
blogCategories:
- "Company"
- "Product Releases"
authors:
- "Brandon Felker"
- "Adi Shtatfeld"
- "Yoav Peled"
lastmod: 2025-07-03
hidden: true
mirrored: true
---

*By Brandon Felker, Adi Shtatfeld, Yoav Peled · Published 29 November 2022 · updated 3 July 2025*

![Blog tile image](/images/site-mirror/e57ce5ae765acbdde99a86d6e4f69b7f57e8abef-772x550.webp)

**Redis Enterprise Software 6.2.18 is out! We’re delighted with this new release, which has a renewed focus on security, and we think you will be, too**.

Here’s an overview of the reasons we think that you’ll be as excited as we are.

## Security first

Security concerns naturally are everyone’s top priority. We at Redis understand those challenges, particularly in enterprise organizations, and are working diligently to enhance our products’ security to comply with regulations and industry requirements.

At the top of the list for [Redis Enterprise Software 6.2.18](/downloads/) are two new top enterprise-grade security features.

### Audit connection events

In computer systems, an audit trail means the process of tracking events and activities that take place while the system is in use. According to the U.S. [National Institute of Standards and Technology](https://csrc.nist.gov/csrc/media/publications/shared/documents/itl-bulletin/itlbul1997-03.txt), “Audit trails can provide a means to help accomplish several security-related objectives, including individual accountability, reconstruction of events (actions that happen on a computer system), intrusion detection, and problem analysis.” For database systems, one key activity to audit is database connections.

Auditing connections helps you track and troubleshoot connection activity: who connected to a database, when the connection was established, for how long it was active (until a disconnection event), and what authentication events were sent during that time. For instance, an e-commerce site might track a payment process’ origin and record that it began at 1:00, lasted 20 seconds, and then disconnected. If you later encounter a problem with the payment – the transaction wasn’t completed due to a network failure or a refused credit card – everyone concerned can see what happened and when.

Starting with version 6.2.18, Redis Enterprise Software lets you audit database connections and authentication events.

For example, one of our customers, a large European [financial](/industries/financial-services/) institution, wants to track failed login attempts to its databases. While occasional login failures are common and acceptable, repeating login failures from the same origin might indicate an attempt to hack the system. Once auditing is enabled, [Redis Enterprise Software](/enterprise/) generates and publishes connection audit records, which the customer can then consume and process for detecting such cases.

![Redis Enterprise software update](/images/site-mirror/ef88ca04416dc4e6f6f7def089905bfb9d0a4cb6-269x312.webp)

Using audit in Redis Enterprise Software involves a few steps:

- Configure the destination to which audit data is to be sent.
- Setup a listener at the destination to consume the audit data
- Enable audit for your database

Once your listener consumes the data, you can store, process, and analyze it according to your needs.

For more details and examples, see the [audit documentation](https://docs.redis.com/latest/rs/security/audit-events/).

### Private key encryption

Also, starting with version 6.2.18, Redis Enterprise Software lets you integrate private key encryption with a third-party password manager.

When enabled, private key encryption encrypts private keys stored in the cluster configuration store (CCS). The encryption mechanism is managed entirely by Redis Enterprise and does not require any level of human interaction.

A third-party password manager is an encrypted digital storage. The password manager stores passwords that are used to access applications or user accounts. A good password manager can also be used to generate secure passwords for applications and user accounts, which makes it an important tool in the CISO toolbag. Using a password manager removes the responsibility of remembering a password which makes it easier to use better passwords, such as longer passwords that contain random characters.

Enterprise customers have internal compliance requirements to manage encryption keys using third-party password managers. To help our customers meet those internal compliance needs, we developed a method by which private key encryption can be managed using a third-party password manager.

Many of our global financial customers are integrating this feature with external password managers (such as [Vault](https://www.vaultproject.io/) and [Cyberark](https://www.cyberark.com/products/privileged-access/)) to externally manage the encryption key. This allows them to follow their internal guidance requiring passwords to be managed using an external secure password management system controlled by their certificate teams.

## But that’s not all: More 6.2.18 features that’ll make you smile

Adding more security features was a top priority. But we want to draw your attention, too, to a few new enhancements that can help with daily tasks such as troubleshooting and upgrades.

### Tips and tricks available with 6.2.18:

#### Retrieve the MEMORY USAGE of an Active-Active database

[Memory usage](https://redis.io/commands/memory-usage/) is a Redis command that reports the total memory footprint of a key: MEMORY USAGE key [SAMPLES count]. It includes the memory allocation of the data and any additional memory allocations required for managing the key and its value.

Starting with 6.2.18, you can use this command for keys in Active-Active databases; We mostly use it to determine which key consumes a lot of memory, and one way to do it is by running redis-cli with the --memkeys option.

#### Display all details of an Active-Active database task

When investigating Active-Active databases issues, you can use the crdb-cli task list command to display the running and recent tasks for all the active-active databases in the cluster. Run crdb-cli task --task-id <task-id> to get more information about a given task. For more information, read about the [crdb-cli tool](https://docs.redis.com/latest/rs/references/cli-utilities/crdb-cli/).

#### Use an API to identify the Master node

Use the API /v1/nodes/status or /v1/nodes/<uid>/status/ to get the node’s role: primary (master) or secondary (slave). This API is extremely useful when applying node maintenance or when [upgrading a cluster](https://docs.redis.com/latest/rs/installing-upgrading/upgrading/#cluster-upgrade-process) where you start with the primary (master) node.

#### Track certificates expiration in Prometheus

An expired certificate can cause outages and client disconnections in the cluster. Today the cluster alerts about soon-to-be-expired certificates via the UI and email. Now you can monitor your certificates’ expiration using [Redis integration with Prometheus](https://docs.redis.com/latest/rs/clusters/monitoring/prometheus-integration/) as well.

The primary goal for Redis Enterprise Software 6.2.18 was adding security features to help create a safe journey for the user and to make life easier for administrators working with our product.

[We invite you to download the new version for a 30-day free trial. Try it out today!](/downloads/)
