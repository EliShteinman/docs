---
title: "Redis Cloud Introduces Short-Lived TLS Certificates"
linkTitle: "Redis Cloud Introduces Short-Lived TLS Certificates"
url: "/blog/redis-short-lived-tls-certificates/"
description: "We’re changing some of our security practices. Here is what you need to know to ensure a smooth transition."
date: 2023-03-21
blogCategories:
- "Announcements"
- "Company"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 21 March 2023 · updated 27 March 2025*

![Blog tile image](/images/blog/0a106f0a0c58ececbd27e81f6f7e658aeffe8f2f-772x550.webp)

**We’re changing some of our security practices. Here is what you need to know to ensure a smooth transition.**

As part of our commitment to continuously improve security measures at Redis, we will soon start replacing the [TLS certificates](https://www.internetsociety.org/deploy360/tls/basics/) for all Redis [Cloud database](/glossary/cloud-database/) services in favor of the short-lived certificates issued by the [publicly trusted](https://cert-manager.io/docs/reference/tls-terminology/#publicly-trusted) GlobalSign Certificate Authority.

## What do you stand to gain from these upcoming changes?

**In short: better security.**

The somewhat longer answer is that the TLS certificates in use today are issued by a [self-signed](https://cert-manager.io/docs/reference/tls-terminology/#what-does-self-signed-mean-is-my-ca-self-signed) Certificate Authority (CA). This means that no trusted third party verified that these certificates were issued on behalf of Redis.

There is no reason for concern, though. You can – and should! – still download our public certificate bundle, which is published in the Redis Cloud [admin console](https://app.redislabs.com/#/account-settings/account). That bundle can assure you that Redis genuinely signed the certificates presented by our database services.

However, the new TLS certificates are issued by a publicly trusted CA called GlobalSign, which means that you don’t have to take our word for the trustworthiness of the certificate.

In this context, “publicly trusted” means at least two things:

- These trusted CAs are audited regularly. That means that they adhere to strict policies and procedures about the manner in which they confirm the identities of the organizations on whose behalf they issue certificates.
- GlobalSign’s root certificates are shipped with and trusted by most web browsers and operating systems by default. Therefore it may very well be that your Redis client already trusts the GlobalSign issuer.

Once we introduce the GlobalSign certificates, they will be issued as “short-lived” certificates. That’s considered a security best practice; ask your CISO! In our case, it means that the [leaf certificates](https://cert-manager.io/docs/reference/tls-terminology/#leaf-certificates) presented to your Redis client by our database services will be valid for three months. We will automatically rotate those certificates well ahead of their expiration date.

Since your Redis client should already trust the GlobalSign CA (more about that later), after the rotation of these leaf certificates, any new connections should establish seamlessly; existing connections should not be affected.

## How to know if you will be affected

If you have not enabled TLS on any of your Redis Cloud databases, then you have nothing to do.

If you currently have TLS-enabled databases in Redis Cloud, then you should make sure that your Redis client will continue to accept the database certificates before and after the change. (See below for how to do that.)

So when should you expect these new certificates? That depends on your Redis Cloud subscription tier and when your subscription was provisioned:

| Fixed | Anytime | April 15, 2023 | All Fixed tier databases currently still present the old self-signed certificates. From April 15th onwards, these certificates will gradually be replaced by the new GlobalSign certificates. |
|---|---|---|---|
| Flexible | Prior to November 30, 2022 | July 1, 2023 | Any Flexible tier database whose subscription was provisioned before November 30th, 2022, currently still presents the old self-signed certificates. Beginning on July 1, these certificates will gradually be replaced by the new GlobalSign certificates. |
| Flexible | After November 30, 2022 | N/A | Any Flexible tier database whose subscription was provisioned on or after November 30, 2022, already received the new certificates. If your Redis client can connect over TLS at the moment, you should not have to take any action. |

## Making sure your Redis client trusts the database certificate before and after the change?

If your Redis client is configured to validate the certificate that is presented by the database (which is not always the case), then it tries to confirm that the certificate was signed by a chain that it trusts. Typically, this trust is either established by providing the public chain of the database certificate to your Redis client directly or adding it to your client’s trust store (depending on your environment, this could be your operating system or Kubernetes trust store or a jks file).

For example, with redis-cli you can provide the database’s public chain to the client, as shown in this example. The cacert parameter should point to a file containing the public database certificate in PEM format:

```
~ redis-cli -h <host> -p <port> --tls --cacert <path to>/redis_ca.pem

```

As mentioned above, the public certificates of Redis Cloud’s databases are published in the Redis Cloud admin console, which is available both from the “Account Settings” and the “Database Configuration” pages. (For more details, see the [TLS documentation](https://docs.redis.com/latest/rc/security/database-security/tls-ssl/).) If you downloaded this public chain anytime after August 2022, the PEM file contains a bundle of the old self-signed certificate chains, as well as the root CA of the new GlobalSign certificates. If you downloaded this public chain before August 2022, make sure to download the latest version and update your Redis Client trust store.

To ensure you are safe, you can inspect this PEM bundle with the keytoolthat comes with Java. On Linux, you can use certtool. It would look something like this:

```
~ keytool -printcert -file <path to>/redis_ca.pem | grep "Owner:"
Owner: CN=SSL Certification Authority, O=Garantia Data
Owner: CN=RCP Intermediate Certificate Authority, O=RedisLabs, ST=CA, C=US
Owner: CN=RedisLabs Root Certificate Authority, O=RedisLabs, L=CA, ST=CA, C=US
Owner: CN=GlobalSign, O=GlobalSign, OU=GlobalSign Root CA - R3

```

The PEM bundle should contain four certificates: theGlobalSign Root CA, plus three self-signed certificate chains used for the old certificates for Fixed and Flexible tier subscriptions.

If your client trust store contains all four certificates, then you should be safe; expect a smooth transition once we start the migration to the GlobalSign certificates. If your Redis client trust store does not contain the GlobalSign root CA certificate, take action now to ensure that your client will not reject TLS connections after the migration.

## Frequently asked questions (FAQs)

If you are affected and your Redis client does not trust the GlobalSign-issued certificates after the transition, your Redis client will likely start rejecting connections to your database.


If you are not using TLS at all at the moment, then you do not have to take any action. Should you at some point in the future want to enable TLS, make sure to download the Redis Cloud CA public certificate PEM bundle at that time and provide it to your Redis client.


Any Flexible tier databases for subscriptions that were created after November 30, 2022, were provisioned with the new TLS certificates issued by GlobalSign. Therefore, if you can currently connect successfully over TLS, you should be fine.

**Note that Fixed tier databases will still undergo the transition. Please make sure that your Redis client’s trust store contains the public certificates of both the old as well as the new GlobalSign chains.*


If your Redis client uses a Redis Cloud PEM bundle that was downloaded in or after August 2022, then in principle, you should be fine. We still recommend that you take the time to ensure that the bundle contains the GlobalSign root CA. (Nobody likes surprises. Especially this kind.)

You can inspect this PEM bundle with the keytoolthat comes with Java:

```
~ keytool -printcert -file <path to>/redis_ca.pem | grep "Owner:"
Owner: CN=SSL Certification Authority, O=Garantia Data
Owner: CN=RCP Intermediate Certificate Authority, O=RedisLabs, ST=CA, C=US
Owner: CN=RedisLabs Root Certificate Authority, O=RedisLabs, L=CA, ST=CA, C=US
Owner: CN=GlobalSign, O=GlobalSign, OU=GlobalSign Root CA - R3

```

Alternatively, on Linux, you can also use certtool**.**

You can inspect the PEM bundle you downloaded from Redis Cloud with the keytoolthat comes with Java and find the first few lines for certificate number 4 issued by GlobalSign:

```
~ keytool -printcert -file <path to>/redis_ca.pem
[...]
Certificate[4]:
Owner: CN=GlobalSign, O=GlobalSign, OU=GlobalSign Root CA - R3
Issuer: CN=GlobalSign, O=GlobalSign, OU=GlobalSign Root CA - R3
Serial number: 4000000000121585308a2
Valid from: Wed Mar 18 12:00:00 IST 2009 until: Sun Mar 18 12:00:00 IST 2029
Certificate fingerprints:
	 SHA1: D6:9B:56:11:48:F0:1C:77:C5:45:78:C1:09:26:DF:5B:85:69:76:AD
[...]

```

Now compare the SHA1 fingerprint of the certificate in the PEM bundle to the thumbprint of the R3 GlobalSign Root Certificate on the official publication of the [GlobalSign Root Certificates](https://support.globalsign.com/ca-certificates/root-certificates/globalsign-root-certificates). If the fingerprints match, then you can be sure that the certificate in the PEM bundle is indeed the public certificate of the R3 Root CA published by GlobalSign.

If you downloaded it in or after August 2022, the PEM bundle contains the following four certificates:

| 1 | SSL Certification Authority | Fixed Root CA (self-signed) | September 2023 |
|---|---|---|---|
| 2 | RCP Intermediate Certificate Authority | Flexible Intermediate | February 2028 |
| 3 | RedisLabs Root Certificate Authority | Flexible Root CA (self-signed) | February 2038 |
| 4 | GlobalSign | GlobalSign Root CA | March 2029 |

The change we are asking you to make now is to trust the GlobalSign root CA (if your Redis client does not trust it already). This GlobalSign root CA should be valid until March 2029, so if we allow for some lead time up to then, we will likely not ask you to replace it within the next five years.


You can use the openssl package for this, as shown below. If the issuer is anything other than GlobalSign**,** then your database has not yet received a short-lived certificate.

```
~ openssl s_client -showcerts -connect \
 <hostname>:<port> 2> /dev/null < /dev/null | grep '^issuer'

```

If you successfully confirmed that your database presents your Redis client with a certificate issued by the GlobalSign trust chain (see question above), it should be safe to remove the other Redis self-signed public certificates from the trust store. Once the entire Redis Cloud fleet is migrated to the new certificates, we will publish a new PEM bundle in the Redis Cloud admin console that contains only the relevant GlobalSign Root CA.

The redis_user.crtand redis_user_private.key files belong to the certificate that you may have created in the Redis Cloud console for “TLS client authentication,” through which the database authenticates your client. These client certificates are not affected by this change (although client certificates can expire as well and should be replaced in a timely manner).
