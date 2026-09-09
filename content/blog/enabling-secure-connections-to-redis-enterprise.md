---
title: "Enabling Secure Connections to Redis Enterprise"
linkTitle: "Enabling Secure Connections to Redis Enterprise"
url: "/blog/enabling-secure-connections-to-redis-enterprise/"
description: "Building software that utilizes secure connections to a server should be a skill every developer possesses. Even if you choose not to enable SSL in a specific production environment, you should..."
date: 2018-06-19
blogCategories:
- "Company"
- "Tech"
authors:
- "Tague Griffith"
lastmod: 2025-03-27
hidden: true
---

*By Tague Griffith, Head of Developer Advocacy · Published 19 June 2018 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

Building software that utilizes secure connections to a server should be a skill every developer possesses. Even if you choose not to enable SSL in a specific production environment, you should know how to secure connections to every server that you work with. This post is the promised follow up to [Enabling Secure Connections to Redis Enterprise Cloud in Python](/blog/enabling-secure-connections-redis-enterprise-cloud-python/) for our Java fans.

This post walks through an easy process to turn on, test and configure encrypted connections between [Redis Enterprise Cloud](/redis-enterprise/cloud/) and a Java client program using SSL. One of the confusing parts of enabling SSL for Java programs is converting the certificates and keys into a format Java understands. This is a Java-only procedure we have to sneak in between the test and configuration steps of our process.

**Toolset**

Grab these tools, so you can close that ticket for enabling SSL on Redis:

- [Redis Enterprise Cloud account](https://app.redis.com/#/sign-up)
- [OpenSSL](https://www.openssl.org/source/)
- [Java SE JDK](http://www.oracle.com/technetwork/java/javase/downloads/index-jsp-138363.html)
- [Jedis](https://github.com/xetorthio/jedis)

You will also need to have the [Bash](https://en.wikipedia.org/wiki/Bash_(Unix_shell)) shell installed so you can run a small script that we provide. If your operating system doesn’t include Bash as part of the standard install, you will need to install it or translate our script into your preferred shell.

To use SSL, your Redis Enterprise Cloud subscription must have the SSL feature enabled. If your account isn’t already enabled for SSL, you will need to contact the Redis support team to enable it. You’ll find a link to contact the support team in the main menu of your account dashboard. Documentation for setting up SSL can be found in the [Redis Enterprise Cloud Operations and Administration Guide](/redis-cloud-documentation/securing-redis-cloud-connections/).

**SSL vs. TLS**

Just a reminder: as in our Python post, we are going to follow the informal convention of using the acronym “SSL” to refer to either “SSL” or “TLS”-secured connections. Even though Redis Enterprise Cloud currently (June 2018) uses version 1.2 of the TLS protocol to secure connections, both Redis Enterprise Cloud and Jedis use “SSL,” so we are going to follow suit.

**Steps One and Two**

The first two steps are identical to those used to set up SSL for a Python client. Instead of repeating it all here, we’re just going to refer you back to our [Python post.](/blog/enabling-secure-connections-redis-enterprise-cloud-python/) There is lots of useful information in that post for working with SSL in any language. I recommend that you read everything up to Step 3 before you continue.

The process starts to diverge for Java after Step 2, so we’re going to insert a Step 2.5 here to transform the credential files you downloaded from Redis Enterprise Cloud into a format that works well with JavaSE.

**Step 2.5: Transforming the Credentials**

As a standard part of JavaSE, Oracle provides a variety of security services, including the [Java Cryptography Architecture (JCA)](https://docs.oracle.com/javase/8/docs/technotes/guides/security/crypto/CryptoSpec.html). The JCA defines a set of APIs for Java applications to invoke security services that are implemented by plug-in providers. Applications are free to use any available provider (who often provide additional services beyond the standard API), but most applications use the [default providers](https://docs.oracle.com/javase/8/docs/technotes/guides/security/SunProviders.html) shipped with the JDK.

The challenge of using the default providers is that they don’t support the PEM format that is commonly used with Linux SSL libraries to store certificates and keys. In the JCA, credential material is stored in password-protected [keystore](https://en.wikipedia.org/wiki/Keystore) repositories. In Java applications, it is common to use two repositories: one is referred to in documentation as a keystore and the other is referred to as a truststore. The keystore is used to store the certificates and private keys for the client software and the truststore is used to store trusted certificates from certificate authorities. The PEM format is used by Redis Enterprise Cloud, so we’ve created a script using OpenSSL and the [Java Keytool](https://docs.oracle.com/javase/10/tools/keytool.htm) to execute all of the commands necessary to convert your PEM files into a truststore and keystore usable for your Java client programs.

The following script, transmogrify.sh, should be run from the directory where you unpacked your redis_credentials.zip. The script uses the Redis Certificate Authority certificate (redis_ca.pem) to create a truststore (redis_truststore.p12) and uses the client certificate (redis_user.crt) and corresponding private key (redis_user_private.key) to create a keystore (redisclient_keystore.p12). While the client keystore is password protected, you should still take steps to ensure the security of your keystore. Both the keystore and the truststore will need to be distributed to every client that connects to a particular Redis database instance, so again you will want to integrate these files into your credential management system.

```python
#!/bin/bash

echo -n "store password: "
read -s storepass
echo ""

## Create Truststore from PEM file
keytool -import -noprompt -trustcacerts -alias redislabs-ca -file redislabs_ca.pem -keystore redislabs_truststore.p12 -storepass $storepass -storetype PKCS12
keytool -list -keystore redislabs_truststore.p12 -storepass $storepass

## Create Keystore from certificate and private key
openssl pkcs12 -export -in redislabs_user.crt -inkey redislabs_user_private.key -out redisclient.p12 -passout pass:$storepass
keytool -importkeystore -noprompt -srckeystore redisclient.p12 -srcstoretype PKCS12 -srcstorepass $storepass -destkeystore redisclient_keystore.p12 -deststoretype PKCS12 -storepass $storepass
rm redisclient.p12
keytool -list -keystore redislabs_truststore.p12 -storepass $storepass

```

Java versions prior to JDK9 favored the proprietary [Java KeyStore (JKS) format](https://docs.oracle.com/javase/10/tools/keytool.htm#JSWOR-GUID-5990A2E4-78E3-47B7-AE75-6D1826259549), but starting with JDK9, Java defaults to the industry standard [PKCS12 format](https://en.wikipedia.org/wiki/PKCS_12). This script creates PKCS12 format stores, but if you can modify the script, use the JKS format by changing the store type option and the file extension.

**Step 3: Configure SSL in your client code**

The final step to enable SSL in your Java client is to modify the client code to establish an SSL connection. Our sample code will establish a secure connection to our Redis Enterprise Cloud instance, then send the Redis PING command. Our modified code looks like:

```python
import redis.clients.jedis.Jedis;

public class SSLTest
{
    private static final String HOSTNAME = "your Redis Enterprise endpoint";
    private static final int PORT = 6379;

    public static void main (String[] args) {

        try {
           Jedis jedis = new Jedis(HOSTNAME, PORT, true);
           jedis.connect();
           jedis.auth("secret");

           System.out.println(jedis.ping());

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

```

You’ll notice, nowhere in the code do we reference the keystore or the truststore that we created for our Java program in Step 2.5. The default behavior of the JCA providers authenticates the server; we just have to provide our key and certificate information. This can be done with system properties read by the JCA providers. Add the following parameters to your IDE application configuration or the java command line:

```python
-Djavax.net.debug=ssl:handshake
-Djavax.net.ssl.keyStoreType=PKCS12
-Djavax.net.ssl.keyStore=/Users/tague/dev/ssl-testj/redisclient_keystore.p12
-Djavax.net.ssl.keyStorePassword=redislabs
-Djavax.net.ssl.trustStoreType=PKCS12
-Djavax.net.ssl.trustStore=/Users/tague/dev/ssl-testj/redislabs_truststore.p12
-Djavax.net.ssl.trustStorePassword=redislabs

```

modifying them to use the appropriate locations and passwords from your system.

The keystore properties:

- javax.net.ssl.keyStoreType=PKCS12
- javax.net.ssl.keyStore=/Users/tague/dev/ssl-testj/redisclient_keyStore.p12
- javax.net.ssl.keyStorePassword=redis

specify the type (aka format), location and password for the keystore created by the transmogrify script. Similarly, the trustStore properties:

- javax.net.ssl.trustStoreType=PKCS12
- javax.net.ssl.trustStore=/Users/tague/dev/ssl-testj/redis_truststore.p12
- javax.net.ssl.trustStorePassword=redis

specify the type, location and password of the trustStore. The final property javax.net.debug=ssl:handshake is an optional property used to enable debugging information.

Configuring Jedis to use SSL is not particularly difficult, but it can be off-putting at first if you’re unfamiliar with the steps necessary to convert PEM credentials into Java key and truststores.

Hopefully, this post provided our Java fans with the same gentle introduction to setting up a secure connection to Redis Enterprise Cloud that we gave to the Python developers. I do want to leave you with one final reminder about security: most organizations have specific policies and procedures for managing passwords and private keys. Please make sure to check with your operations and security teams to ensure you’re following their guidelines.
