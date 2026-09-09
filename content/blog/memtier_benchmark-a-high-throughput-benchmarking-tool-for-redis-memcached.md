---
title: "memtier_benchmark: A High-Throughput Benchmarking Tool for Redis & Memcached"
linkTitle: "memtier_benchmark: A High-Throughput Benchmarking Tool for Redis & Memcached"
url: "/blog/memtier_benchmark-a-high-throughput-benchmarking-tool-for-redis-memcached/"
description: "Benchmarking is the practice of measuring the performance of a system to identify its limits. Benchmarking is an integral part of our service’s development process and we use it both for regression..."
date: 2013-07-02
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 2 July 2013 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

Benchmarking is the practice of measuring the performance of a system to identify its limits. Benchmarking is an integral part of our service’s development process and we use it both for regression testing (verifying performance has not been reduced between releases) and also as an aid for optimizing database performance. It is generally considered good practice to measure the performance of your system periodically as well as after every change made to ensure it is achieving maximal performance and to potentially uncover relevant issues. To facilitate the execution of these benchmark runs, we developed our own benchmarking tool that we fondly call memtier_benchmark.

This tool can be used to generate various traffic patterns against both Memcached and Redis instances. It provides a robust set of customization and reporting capabilities all wrapped into a convenient and easy-to-use command-line interface. We use it extensively for all our benchmarking needs, both in development as well as to help share our knowledge with the broader community (for example, as we did in [this blog post](/blog/benchmark-shared-vs-dedicated-redis-instances)). We’ve released memtier_benchmark source code under the [GPLv2](https://www.gnu.org/licenses/gpl-2.0.html) licensing scheme, and you can download it from [our github account](https://github.com/GarantiaData/memtier_benchmark). The following are some highlights about the tool.

- It supports both Redis and Memcached (binary and text) protocols so you can use it to test both and even compare their performance under different scenarios
- memtier_benchmark is capable of launching multiple worker threads (using the -t option), with each thread driving a configurable number of clients (the -c option). Multiple threads enable you to better utilize the hardware resources of your benchmarking client and generate high traffic loads even using a single server.
- When you instruct the tool to do multiple iterations of the benchmark run (the -x option), it will automatically produce reports for the best and worst runs as well as aggregated averages
- You can control the ratio between GET and SET operations with the ratio option to measure performance when dealing with different access patterns
- The tool offers control over the pattern of keys used by the GET and SET operations (key-pattern option). Each operation’s pattern can be set independently to be random or sequential.
- Keys’ expiry can be common or randomly set from a configurable range (the expiry-range option)

For more information about these and other features of the tool, below is memtier_benchmark’s usage clause (printed with the help switch). Do feel free to give it a go and let us know what you think.

```javascript
Usage: memtier_benchmark [options]
A memcache/redis NoSQL traffic generator and performance benchmarking tool.

Connection and General Options:
  -s, --server=ADDR              Server address (default: localhost)
  -p, --port=PORT                Server port (default: 6379)
  -S, --unix-socket=SOCKET       UNIX Domain socket name (default: none)
  -P, --protocol=PROTOCOL        Protocol to use (default: redis).  Other
                                 supported protocols are memcache_text,
                                 memcache_binary.
  -x, --run-count=NUMBER         Number of full-test iterations to perform
  -D, --debug                    Print debug output
      --client-stats=FILE        Produce per-client stats file
      --out-file=FILE            Name of output file (default: stdout)
      --show-config              Print detailed configuration before running

Test Options:
  -n, --requests=NUMBER          Number of total requests per client (default: 10000)
  -c, --clients=NUMBER           Number of clients per thread (default: 50)
  -t, --threads=NUMBER           Number of threads (default: 4)
      --test-time=SECS           Number of seconds to run the test
      --ratio=RATIO              Set:Get ratio (default: 1:10)
      --pipeline=NUMBER          Number of concurrent pipelined requests (default: 1)
      --reconnect-interval=NUM   Number of requests after which re-connection is performed
      --multi-key-get=NUM        Enable multi-key get commands, up to NUM keys (default: 0)
  -a, --authenticate=PASSWORD    Authenticate to redis using PASSWORD
      --select-db=DB             DB number to select, when testing a redis server

Object Options:
  -d  --data-size=SIZE           Object data size (default: 32)
  -R  --random-data              Indicate that data should be randomized
      --data-size-range=RANGE    Use random-sized items in the specified range (min-max)
      --data-size-list=LIST      Use sizes from weight list (size1:weight1,..sizeN:weightN)
      --expiry-range=RANGE       Use random expiry values from the specified range

Imported Data Options:
      --data-import=FILE         Read object data from file
      --generate-keys            Generate keys for imported objects

Key Options:
      --key-prefix=PREFIX        Prefix for keys (default: memtier-)
      --key-minimum=NUMBER       Key ID minimum value (default: 0)
      --key-maximum=NUMBER       Key ID maximum value (default: 10000000)
      --key-pattern=PATTERN      Set:Get pattern (default: R:R)

      --help                     Display this help
      --version                  Display version information
```

EDIT: check out the description of memtier_benchmark’s new version with [pseudo-random data, Gaussian access pattern and range manipulation here](/blog/new-in-memtier_benchmark-pseudo-random-data-gaussian-access-pattern-and-range-manipulation)
