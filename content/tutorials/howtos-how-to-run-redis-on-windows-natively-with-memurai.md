---
title: "How to run Redis on Windows Natively"
linkTitle: "How to run Redis on Windows Natively"
url: "/tutorials/howtos/how-to-run-redis-on-windows-natively-with-memurai/"
description: "Memurai for Redis brings the full power and performance of Redis to Windows - natively, seamlessly, and without compromise. Visit memurai.com for installation packages and more information."
aliases:
- "/tutorials/howtos-how-to-run-redis-on-windows-natively-with-memurai/"
date: 2026-02-25
lastmod: 2026-02-26
hidden: true
---

*Published 25 February 2026 · updated 26 February 2026*

> **TL;DR:** **How do I run Redis on Windows?**
>
> Install [Memurai](https://www.memurai.com/?utm_source=redis&utm_medium=referral&utm_campaign=redis_blog_Q2_2025), a native Windows port fully compatible with Redis 7. Download the installer, run through the GUI or silent command-line setup, and connect with `memurai-cli.exe` on port 6379 — no WSL or Docker required.

![Memurai – Data Store](/images/site-mirror/e40cf4e6b58b85dc480a47c8aaf9a1d6645cad88-1200x630.webp)

**Memurai for Redis** brings the full power and performance of Redis to Windows - natively, seamlessly, and without compromise. Visit memurai.com for installation packages and more information.

This guide will walk you through installing and configuring [Redis on Windows](https://www.memurai.com/?utm_source=redis&utm_medium=referral&utm_campaign=redis_blog_Q2_2025) with Memurai. You'll also find key information on system requirements and supported features.

## Prerequisites

Before installing Memurai for Redis on Windows, make sure your system meets the following requirements:

- **Operating system:** Windows 10 / Windows Server 2012 or newer (64-bit only)
- **Recommended:** Windows 10 or Windows Server 2016+ for best performance
- **Disk space:** enough room for the Memurai installation and your data set
- **Permissions:** administrator access to install services and configure firewall rules

## How do Memurai, WSL, and Docker compare for running Redis on Windows?

If you need Redis on Windows, there are three main options. Here's how they compare:

|                             | **Memurai (native)**                   | **WSL (Windows Subsystem for Linux)** | **Docker Desktop**            |
| --------------------------- | -------------------------------------- | ------------------------------------- | ----------------------------- |
| **Setup complexity**        | Simple installer                       | Requires WSL 2 + Linux distro         | Requires Docker Desktop       |
| **Performance**             | Native Windows performance             | Near-native via Hyper-V               | Container overhead            |
| **Windows service support** | Yes — runs as a native service         | No — manual process management        | Container lifecycle only      |
| **Redis compatibility**     | Redis 7.2.6 API                        | Full (runs official Redis)            | Full (runs official Redis)    |
| **Best for**                | Windows-first development & production | Developers already using WSL          | Cross-platform / CI workflows |

Memurai is the best choice when you want a hassle-free, native Redis experience on Windows 10 or 11 without running a Linux layer or a container runtime.

## How to install Memurai for Redis

You can install Memurai for Redis either via a graphical installer or using the command line.

### GUI installation

- During installation, you can choose to install Memurai as a Windows service. If skipped, you can still set it up as a service later via command line.
- You can specify the port number during service installation and opt to create a firewall rule (if Windows Firewall is active). The selected port is saved in the configuration file and can be updated later by editing the file and restarting the service.
- The Windows service runs under the `NT AUTHORITY\NetworkService` account by default, but this can be changed in the Services management console. Memurai is configured to start automatically with Windows.
- The Memurai installer includes the main executable `memurai.exe`, the Memurai client `memurai-cli.exe`, and other tools. It also installs a default configuration file, `memurai.conf`, fully compatible with the Redis® 7 API.

![Memurai GUI installation](/images/site-mirror/f82b6579caf6357363f4148f230c80a1fc961b34-496x389.webp)

### Command line installation

To install Memurai silently with default settings, run:

`C:\>msiexec /quiet /i memurai.msi`

Where `memurai.msi` is the path to the installation file.

![Memurai CLI installation](/images/site-mirror/853a8d42e78d68ad7b770d23f7a54b083e8660d4-657x177.webp)

You can override default settings with specific parameters:

| Option name               | Default value                |
| ------------------------- | ---------------------------- |
| INSTALLFOLDER             | "C:\\Program Files\\Memurai" |
| ADD_INSTALLFOLDER_TO_PATH | 1                            |
| INSTALL_SERVICE           | 1                            |
| PORT                      | 6379                         |
| ADD_FIREWALL_RULE         | 1                            |

Example 1: Custom install path, add to PATH, no Windows service:

`C:\>msiexec /quiet /i Memurai.msi INSTALLFOLDER="C:\MyApps\Memurai" ADD_INSTALLFOLDER_TO_PATH=1 INSTALL_SERVICE=0`

Example 2: Install with default location, no PATH addition, service on port 8000:

`C:\>msiexec /quiet /i Memurai.msi ADD_INSTALLFOLDER_TO_PATH=0 PORT=8000`

#### How to configure Memurai?

If installed as a Windows service, Memurai can run with either default or custom configurations.

To run with the default config:

`C:\Users\<username>\memurai.exe`

To use a custom configuration, modify the default config file.

#### What is the configuration file?

The configuration file is a plain text file where each line starts with a keyword followed by its arguments:

`keyword arg1 arg2 ... argN`

Arguments that include spaces must be enclosed in quotes:

`logfile "C:\logs\memurai log.txt"`

You can use both \\ and / as path separators:

`logfile "C:/logs/memurai log.txt"`

#### How to edit the configuration file?

Copy the default memurai.conf, modify it as needed, and run Memurai with it:

`C:\Users\<username>\memurai>memurai.exe memurai.conf`

### What Redis configuration flags does Memurai support?

Memurai supports all standard Redis configuration flags **except** the following:

- `always-show-logo`
- `activedefrag`
- `active-defrag-ignore-bytes`
- `active-defrag-threshold-lower`
- `active-defrag-threshold-upper`
- `active-defrag-cycle-min`
- `active-defrag-cycle-max`
- `daemonize`
- `supervised`
- `syslog-enabled`
- `syslog-ident`
- `syslog-facility`
- `unixsocket`
- `unixsocketperm`

If these flags are included in the config file, Memurai will ignore them.

### Are there any Memurai-specific configuration flags?

Yes, Memurai introduces a few unique flags:

- `instance-name`: Assigns a name to the Memurai instance, shown in Windows Event Logs and the log file to help differentiate between multiple instances.
- `winlog-level`: Sets the verbosity level of logging for Windows Event Log entries.

For detailed installation and configuration options, refer to the [official Memurai docs](https://docs.memurai.com/en/installation.html?utm_source=redis&utm_medium=referral&utm_campaign=redis_blog_Q2_2025).

## Frequently asked questions

### What are the minimum system requirements for Memurai?

Memurai is compatible with:

- Windows 10 and Windows Server 2012 or newer
- For best results, use Windows 10 or Windows Server 2016+
- Only 64-bit Windows versions are supported

### Which Redis version is Memurai compatible with?

Memurai fully supports the Redis 7.2.6 API, so any Redis client library or tool that works with Redis 7 will work with Memurai out of the box.

### What are the known limitations of Memurai?

- Unix domain sockets are not supported (Windows does not have them)
- A small number of Linux-specific config flags are excluded because they are irrelevant for Windows (see the [unsupported flags list](#what-redis-configuration-flags-does-memurai-support) above)

### Can I use Memurai in production?

Yes. [Memurai Enterprise Edition](https://portal.memurai.com/auth/register?utm_source=redis&utm_medium=referral&utm_campaign=redis_blog_Q2_2025) is designed for production workloads with unlimited uptime, host connections, and RAM utilization.

For a full list of FAQs, check out the [Memurai FAQ](https://www.memurai.com/faq?utm_source=redis&utm_medium=referral&utm_campaign=redis_blog_Q2_2025).

## Next steps

Now that Redis is running on your Windows machine via Memurai, here are some ways to continue:

- **Explore Redis commands** — try the [Redis Quick Start](/tutorials/howtos/quick-start/) tutorial to learn the core data structures and commands.
- **Connect from your application** — use any Redis client library (Python, Node.js, .NET, Java, etc.) and point it to `localhost:6379`.
- **Go to production** — try [Memurai Enterprise Edition](https://portal.memurai.com/auth/register?utm_source=redis&utm_medium=referral&utm_campaign=redis_blog_Q2_2025) free for 90 days with unlimited uptime and RAM utilization.
- **Stay up to date** — Memurai engineers are working on full compatibility with Redis 8. Visit [memurai.com](https://www.memurai.com/?utm_source=redis&utm_medium=referral&utm_campaign=redis_blog_Q2_2025) for updates.

## Get started with Memurai today

Gone are the days of frustrating workarounds and unsupported builds just to get Redis running on Windows. Memurai gives you the speed, simplicity, and reliability of Redis, fully optimized for your Windows environment.

Interested? Try [Memurai Enterprise Edition](https://portal.memurai.com/auth/register?utm_source=redis&utm_medium=referral&utm_campaign=redis_blog_Q2_2025) free for 90 days - ideal for production use, with unlimited uptime, host connections, and RAM utilization. Register through the new Memurai Portal to experience the production-ready Enterprise Edition.

If you have any questions about Memurai—including pricing or technical details—feel free to reach out to us through the chatbot on our [website](https://www.memurai.com/?utm_source=redis&utm_medium=referral&utm_campaign=redis_blog_Q2_2025).
