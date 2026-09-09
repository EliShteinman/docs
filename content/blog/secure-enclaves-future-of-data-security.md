---
title: "Secure Enclaves Could Be the Future of Data Security"
linkTitle: "Secure Enclaves Could Be the Future of Data Security"
url: "/blog/secure-enclaves-future-of-data-security/"
description: "If you work in cybersecurity, or if you’ve interacted with your organization’s cybersecurity team, you’ve likely heard the question, “Is everything encrypted in transit and at rest?” Encryption in..."
date: 2020-05-12
blogCategories:
- "Company"
authors:
- "Jamie Scott"
lastmod: 2025-03-27
hidden: true
---

*By Jamie Scott, Product Manager · Published 12 May 2020 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/cafb43074ab4accfbc0478da84113fa9589d4c93-772x520.webp)

If you work in cybersecurity, or if you’ve interacted with your organization’s cybersecurity team, you’ve likely heard the question, “Is everything encrypted in transit and at rest?” Encryption in transit protects data while in motion, and encryption at rest protects data in storage.

In highly regulated industries, this is standard operating procedure. In less regulated industries, it’s still a prudent practice when handling customer data.

But there’s another realm of encryption that few talk about, and that’s *encryption in use*. Encryption in use protects data when it is being processed in memory. Practically speaking, encryption in use prevents someone who has access to a server from being able to access data through a memory dump or memory forensics, which can be performed on any process running on a server. (To truly understand the importance of encryption in use, you should approach it with the mindset that your organization has already been compromised and security is about minimizing the potential damage.)

Today, encryption in use is typically done with client-side encryption. However, there is an emerging technology, called secure enclaves, that promises to solve many of the limitations of client-side encryption.

## What is client-side encryption?

Client-side encryption, or the practice of encrypting data within an application before storing it in a database, such as Redis, is the most widely adopted method to achieve encryption in use.

Client-side encryption also protects against insider threats. Reducing who can access your data transforms who you have to trust when conducting business operations. With client-side encryption, you no longer have to trust an administrator on the operating system of your database. Similarly, client-side encryption helps remove third parties from who or what you need to trust to run your application, called the trusted computing base. You no longer have to trust your cloud provider not to misuse your data because it has access to the operating system or hypervisor, you can ensure that cloud providers cannot access your data.

These benefits apply to both client side encryption and the use of a secure enclave.

## The limitations of client-side encryption

However, there are two big limitations to client-side encryption. First, functions that need to operate on data—such as simple searching functions, comparisons, and incremental operations—don’t work with client-side encryption. The command line example below shows how incrementing an encrypted number fails because the data is no longer recognized after being encrypted client side:

$ echo "33" >> secrets.txt

$ openssl aes-256-cbc -a -salt -in secrets.txt -out secrets.txt.enc

$ enter aes-256-cbc encryption password:*****

$ Verifying - enter aes-256-cbc encryption password:*****

$ cat secrets.txt.enc

U2FsdGVkX1+zYi/m14irl+JeZokh75XxRAG4HBA56bk=

$ redis-cli set mysecret U2FsdGVkX1+zYi/m14irl+JeZokh75XxRAG4HBA56bk=

OK

$ redis-cli incrby mysecret 1

(error) ERR value is not an integer or out of range

In addition, multiple services often have to access the same database, which brings with it the complexity and investment of managing encryption keys across multiple applications. This raises the administrative overhead of deploying client-side encryption.

## Secure enclaves for encryption in use

Secure enclaves promise to help reduce the barriers to encryption in use. Secure enclaves are private allocations of memory protected from use by external processes. An ecosystem of hardware vendors, cloud providers, and software makers is now forming to make the use of secure enclaves more accessible to the software community. As of April 2020, support for secure enclaves is available in some on-premises hardware, in a subset of Microsoft Azure virtual machines, and in dedicated hardware instances in Alibaba Cloud and IBM Cloud.

So, what do secure enclaves need to achieve broad success? According to the [theory of the diffusion of innovation](https://en.wikipedia.org/wiki/Diffusion_of_innovations), many emerging technologies struggle to cross the chasm between attracting early adopters and making headway with the early majority. As secure enclave technology develops and finds new followers, it is approaching that chasm, which has been the graveyard of many promising technologies. But given the technology’s momentum and the ecosystem building around it, we’re really excited about the prospects for secure enclaves.

![](/images/site-mirror/3cb4a8c1c2eff66c89cade487e587354a2019bfd-1024x357.webp)

*The chasm of innovation adoption.*

Four critical things must happen for secure enclaves to successfully cross that chasm:

1. **Hardware support:** Secure enclaves are a hardware-based implementation of encryption in use. It’s important that this technology be built into newly shipped hardware and that it be measured to be performant. The greater the hardware adoption, and the better the performance, the faster we’ll see overall adoption.
1. **Cloud provider service adoption: **Buying custom hardware to experiment with secure enclaves can be cost prohibitive for many organizations. Rapid adoption of an emerging technology like secure enclaves will be difficult if a massive investment is required. Cloud-scale infrastructure and economies of scale are essential to create an affordable playground to accelerate the adoption of secure enclaves.
1. **Software adoption simplification toolsets emerge:** Secure enclaves are complex beasts. Developing against them will require software developers to learn new ways to build and structure their applications. Software tools that enable applications to easily be adapted or created to support the use of secure enclaves will be essential to the success of this movement.
1. **Application adoption:** Finally, a critical mass of application developers must choose to invest their time into developing applications in secure enclaves.

## Secure enclaves in the Redis community

Redis is partnering with those in the community who are developing the secure enclave ecosystem. We’re working to take Redis and Redis Enterprise into the rapidly forming secure enclave ecosystem by partnering with [Anjuna](https://www.anjuna.io/), a vendor that moves existing applications as-is into enclaves with no re-coding required. While we’re still in the early stages of innovation, we aim to encourage a broader awareness to help secure enclaves cross the chasm from early adoption to early majority and promote the technology’s ongoing success.

We see three key benefits of secure enclaves for the Redis community:

1. **Encryption in use that enables functionality: Encryption in use could be a significant enabler for the Redis community. It could help protect data in Redis from unauthorized access by someone who has access to the operating system. Data stored in memory is a prime target for these attacks. While these attacks are uncommon and the compliance community has not yet mandated encryption in use, secure enclaves could help Redis expand into use cases that require the highest levels of security while minimizing the impact to Redis functionality.**
1. **Data sealing: Data protected in memory has to persist somewhere so that your database can survive a failure event. Data sealing lets you persist data to disk in an encrypted format that can be read only by the secure enclaves. Data sealing could help ensure that Redis RDB and AOF files are protected and available for use after failure events.**
1. **Decrease the need to trust cloud providers: Redis is the most widely deployed database in the cloud. Using Redis with a secure enclave could ensure that cloud providers are removed from the trusted computing base.**

## How to ensure you’re secure using secure enclaves

To fully protect your in-memory data, more than just the data in Redis needs to be encrypted. Application services developed against Redis must also be developed in a secure enclave. You will still be exposed to memory attacks if your applications are not developed using this technology.

This has been a simplified explanation of the benefits of secure enclaves, designed specifically for the Redis community. Like any emerging technology, you should be aware of secure enclave’s limitations as well as its functionality.

If you’d like to find out more about secure enclaves on a technical level, a paper called [Improving Cloud Security Using Secure Enclaves](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2016/EECS-2016-219.html), out of UC Berkeley, is a good place to start. You can also find out more by visiting [Intel’s Software Guard Extensions (SGX) site](https://software.intel.com/en-us/sgx).
