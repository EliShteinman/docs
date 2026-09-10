---
title: "How to build a Fraud Detection System using Redis"
linkTitle: "How to build a Fraud Detection System using Redis"
url: "/tutorials/howtos/frauddetection/"
description: "Imagine that your ads are generating a lot of traffic, but you are not seeing the desired results from your ad spend. This might not be a coincidence—fraudsters often try to steal digital ad..."
group: "For developers"
aliases:
- "/tutorials/howtos-frauddetection/"
date: 2026-02-25
lastmod: 2026-02-25
hidden: true
---

*Published 25 February 2026*

> **TL;DR:**
>
> You can build a real-time fraud detection system with Redis by combining Cuckoo Filters for IP blacklisting, Sorted Sets for click spam detection, Streams for event ingestion, and TimeSeries with Grafana for visualization. This tutorial walks through a Python-based implementation that catches suspicious transactions as they happen.

## What you'll learn

- How to use Redis Cuckoo Filters (a probabilistic data structure) to detect blacklisted IPs in real time
- How to identify click spamming using Redis Sorted Sets with time-windowed counting
- How to stream fraud detection events through Redis Streams and process them with RedisGears
- How to visualize fraud metrics in Grafana using Redis TimeSeries
- How to containerize and deploy the full fraud detection pipeline with Docker

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed on your local machine
- Basic familiarity with Python and Flask
- A Redis server with modules (RedisGears, RedisBloom, RedisTimeSeries) — this tutorial uses the `redislabs/redismod` Docker image
- Basic understanding of Redis data structures (Sorted Sets, Streams)

## Why do you need a real-time fraud detection system?

Imagine that your ads are generating a lot of traffic, but you are not seeing the desired results from your ad spend. This might not be a coincidence—fraudsters often try to steal digital ad marketing budgets through various sophisticated mechanisms. Faking clicks can make it appear as though a real user was engaging with the ad, but in reality when these fake clicks drive installs, the cost of the install goes to the fraudster's pocket. As companies' willingness to spend more on digital advertisements grows, the number of fraudsters in ad markets also increases.

![Illustration showing fast fraud detection with Redis, depicting how Redis processes streaming data to identify fraudulent ad clicks in real time](/images/site-mirror/2b720cddf7cc284a3ac0f9a85ca4146e5d028340-1236x378.webp)

This tutorial demonstrates a simplified use case of how fast fraud detection works—so that you can understand how to stay ahead of the fraudsters.

## What Redis data structures does this fraud detection system use?

Here's what we have used:

- Python-based fraud detector module which performs two kinds of fraud checks: IP blacklisting & click spamming
- IP blacklisting uses Redis Cuckoo Filter.
- Click spamming uses Redis Sorted Set.
- The data is then pushed to Redis Streams which is consumed by RedisGears for processing
- Redis TimeSeries gets updated and Redis Data Source for Grafana displays the dashboard

![Architecture diagram showing the fraud detection pipeline: events flow through a Python fraud detector using Redis Cuckoo Filter and Sorted Sets, then into Redis Streams processed by RedisGears, with results stored in Redis TimeSeries and visualized in Grafana](/images/site-mirror/f4a973e1a8f331324877831ad9bf45db2ec0dc4c-2000x1051.webp)

## How do you install Docker for this project?

You can follow [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/) to get Docker installed on your local system.

## How do you set up Redis with the required modules?

You will need a Redis server up and running on your local machine. You can use the below CLI to bring up Redis server with RedisGears.

```bash
 docker run -d -p 6379:6379 redislabs/redismod
```

The command will pull the image from redis docker repo and start the Redis server with all the required modules and the logs ends like this.

## How do you clone the fraud detection repository?

```bash
 git clone https://github.com/redis-developer/redis-datasets.git
```

## How do you build and run the Docker container?

Change directory to fraud-detection

```bash
 cd redis-datasets/use-cases/fraud-detection
```

The code is present in use-cases/fraud-detection. The app is dockerized with necessary packages (including client packages for redis modules).

Create the image using the command:

```bash
 docker build -t redis-fraud:latest .
```

Create the container using the command:

```bash
 docker run -e REDIS_HOST='<host>' -e REDIS_PORT=6379 -p 5000:5000 -d redis-fraud
```

You will get the container Id, which can be used to tail application logs.

```bash
 docker logs -f <container-id>
```

If you are using a redismod image to run Redis locally, please provide the IP of the host machine (and not localhost or 127.0.0.1).

## How does the fraud detection application work?

Let's take a look at how connections are managed in this project.

```python
 import os
 import redis
 from redisbloom.client import Client
 from singleton_decorator import singleton

 @singleton
 class RedisConn:
    def __init__(self):
        host = os.getenv("REDIS_HOST")
    port = os.getenv("REDIS_PORT")

    if not host or not port:
        raise Exception("No Redis Host or Port provided. Please provide Host and Port in docker run command as env")

    port = int(port)
    self.redis_client = redis.Redis(host=host, port=port)
    self.bloom_client = Client(host=host, port=port)

    def redis(self):
        return self.redis_client

    def bloom(self):
        return self.bloom_client
```

In line 2, we import the redis package for package. All the core Redis commands are available in this Redis package.

In line 4, we import the RedisBloom package. Since RedisBloom is a module, the clients used to interact with this module are also different. We will see more such examples below. The singleton_decorator ensures only one instance of this connection class is created, and os package is used to read the environment variables to form the connection.

### How does Redis detect IP fraud and click spamming?

Now let's take a look at how we use Redis to solve click spamming and IP fraud.

Gist: [https://gist.github.com/Sachin-Kottarathodi/c3a0647d3fdd0fe8a76425e0594e11c5](https://gist.github.com/Sachin-Kottarathodi/c3a0647d3fdd0fe8a76425e0594e11c5)

```python
 def ip_fraud(self, data):
     exists = RedisConn().bloom().cfExists(Constants.IP_CUCKOO_FILTER_NAME, data['ip'])
     if exists:
         data['fraud_type'] = Constants.IP_BLACKLIST
         data['status'] = Constants.FRAUD

     return exists

 def click_spam(self, data):
    is_click_spammed = False
    count = RedisConn().redis().zcount(data.get('device_id'), data['ts'] - self.click_spam_window_in_sec, data['ts'])
    if count >= self.click_spam_threshold:
         is_click_spammed = True
         data['fraud_type'] = Constants.CLICK_SPAM
         data['status'] = Constants.FRAUD
    return is_click_spammed

 def publish(self, data):
    RedisConn().redis().xadd(Constants.STREAM_NAME, data, id='*')
```

In the above code, Cuckoo Filter is used to find blacklisted IP fraud. Cuckoo Filter is a probabilistic data structure that's part of Redis. Checking for existence of IP in Cuckoo Filter is done using the cfExists method provided by bloom client.

> **TIP**
>
> The Cuckoo Filter can return false positives. To configure the error rate, the `cf.reserve` command can be used to create the filter, and a custom bucket size can be provided.

To identify click spam, we use the zcount method of sorted sets provided in redis package. Using zcount, we find the number of clicks from a device in a certain pre configured window. If the count received is greater than a certain threshold, we identify it as anomalous.

Finally, data is pushed to Redis Streams using the xadd command. id='\*' indicates Redis Streams to generate a unique id for our message.

### How do you register RedisGears for stream processing?

When the app appears, a gear is registered, which reacts to the stream that we use to push data.

Gist:[https://gist.github.com/Sachin-Kottarathodi/f9dac7a3342a3643e792e2143a6adf7d](https://gist.github.com/Sachin-Kottarathodi/f9dac7a3342a3643e792e2143a6adf7d)

```python
 from gearsclient import GearsRemoteBuilder as GearsBuilder
 from redistimeseries.client import Client

 def stream_handler(item):
  data = item['value']
  member = json.dumps(
    {'device_id': data['device_id'],
    'transaction_id': data['transaction_id'],
    'ts': data['ts'],
    })
  redis.Redis().zadd(data.get('device_id'), {member: data['ts']})
  Client().incrby(data['fraud_type'], 1)

  GearsBuilder(reader='StreamReader', r=redis_conn, requirements=["redis", "redistimeseries"]).foreach(stream_handler).register('data_stream')
```

As mentioned before, since RedisGears and Redis TimeSeries are modules, we need to use the clients provided in their respective packages.

We use the GearsRemoteBuilder class to build the Gear. StreamReader ensures that the stream_handler function is executed for every new message from the stream. The stream_handler adds the data to the sorted set using zadd (This information is used in zcount to identify click_spam) and increments the count of time series for clean and fraud types using incrby of the Redis TimeSeries module, which is later used for visualization.

![Redis Insight dashboard showing registered RedisGears functions for the fraud detection stream handler](/images/site-mirror/11fd90de00dce10152296b182471ca1a9003f7db-1386x328.webp)

Gear registration can be checked on Redis Insight as well.

### How do you expose the fraud detection API with Flask?

Finally, we incorporate the flask app which exposes the end point for trigger.

Gist: [https://gist.github.com/Sachin-Kottarathodi/2a6cccb29b4a9fdc7d58086af07aa6eb](https://gist.github.com/Sachin-Kottarathodi/2a6cccb29b4a9fdc7d58086af07aa6eb)

```python
 from flask import Flask, request
 from fraud_checks import FraudChecks
 from setup import Setup
 app = Flask(__name__)

 @app.route('/', methods=['POST'])
 def check_fraud():
    try:
    response = FraudChecks().check_fraud(request.get_json())
    code = 200
    except Exception as e:
    print("Error occurred ", e)
    response = str(e)
    code = 500

    return response, code

 if __name__ == '__main__':
    Setup().init()
    app.run(port=5000, debug=False, host='0.0.0.0')
```

Here, the app is exposed on port 5000. Before starting the server, our init method of setup is called to register the gear. The endpoint calls the function that does the fraud checks and returns the response.

### How do you test the fraud detection endpoint?

The application is written in python and exposes an endpoint which accepts a few parameters. Use the below command to invoke the application:

```bash
 $ curl --request POST 'localhost:5000' --header 'Content-Type: application/json' --data-raw '{
      "device_id": "111-000-000",
      "ip": "1.1.1.1",
      "transaction_id": "3e4fad5fs"}'
 clean
```

Since initially no data is available in Cuckoo Filter, all IPs will be allowed through. To add data to Cuckoo Filter, connect to Redis using cli and run the command

```bash
 cf.addnx ip_cf 1.1.1.1
```

Run the post command with this IP again. This time, the result will be ip_blacklist.

![Terminal output showing a curl request returning ip_blacklist after adding the IP to the Redis Cuckoo Filter](/images/site-mirror/7d0f5ec479a55a55e4e30f8cd3ca28d51fbbfcbd-1400x234.webp)

### How does click spam detection work?

The app is configured to allow two events in a window of 10 seconds from the same device. To verify, make more than two curl requests within 10 seconds and the result will be `click_spam`.

![Terminal output showing a curl request returning click_spam after exceeding the threshold of requests within the time window](/images/site-mirror/d35b2a1f0be56944056d7411fad002bb55dbf140-1408x212.webp)

Optional: The following variables can be configured during the 'docker run' command. -e CLICK_SPAM_THRESHOLD=3 -e CLICK_SPAM_WINDOW_IN_SEC=10

## How do you visualize fraud detection results with Grafana?

It's exciting to see the fraud detection plotted in Grafana. To implement this, run the command below:

```bash
 docker run -d -e "GF_INSTALL_PLUGINS=redis-app" -p 3000:3000 grafana/grafana
```

Point your browser to https://<IP_ADDRESS>:3000.

![Grafana login page with username and password fields for accessing the fraud detection dashboard](/images/site-mirror/23c3f70e0f312026b4a1af305d57973e6831c411-1186x1148.webp)

Login as 'admin' with password as 'admin', you can reset the password after your first login.

![Grafana data source configuration page showing the list of configured data sources](/images/site-mirror/e18cb04889e5511ce451d09faa9f70b160cee8dd-1238x626.webp)

Click on the gear icon on the left panel (Configuration) and choose Data Sources.

![Grafana Add data source page with search field and available data source types](/images/site-mirror/44d71be6186d3aac3783c871158b5b9657309b6c-1234x790.webp)

Choose 'Add data source'.

![Search results showing Redis Data Source plugin in the Grafana data source selection screen](/images/site-mirror/a3422a05f8c14bb37e8c7ac7a8a7e315090d679f-1236x552.webp)

Search for Redis and choose Redis Data Source.

![Grafana Import dashboard screen with the Import via panel JSON text box for pasting the Fraud Stats dashboard configuration](/images/site-mirror/c14ee910248de86f666804c7226644e787c8a916-1140x1080.webp)

Copy and paste the [raw json content](https://github.com/redis-developer/redis-datasets/blob/master/use-cases/fraud-detection/Fraud-Stats-Grafana.json) in the 'Import via panel json' box. Click on Load.

![Successfully imported Fraud Stats dashboard in Grafana showing the dashboard name and data source configuration](/images/site-mirror/d8907432886de1fa4f85ef7e332f766b41194557-1232x968.webp)

This creates a dashboard 'Fraud Stats'. If you get an error while importing the dashboard, try changing the name and UUID of the dashboard.

![Fraud Stats Grafana dashboard displaying real-time bar charts comparing clean vs fraud event counts from Redis TimeSeries](/images/site-mirror/6bff19dd937087eaf7f0c5c891a308d774b33f79-1234x370.webp)

![Detailed view of the Fraud Stats Grafana dashboard showing time-series graphs of fraud detection metrics including IP blacklist and click spam events](/images/site-mirror/3af529f292c1062dbef8aae9be6455d5d2e26722-1238x644.webp)

## Conclusion & future work

- If we consider the entire flow starting from fraud check, from event streaming to data processing to visualization (using insights), all of this would have required multiple components and extensive orchestration. With Redis Ecosystem, most of this is removed.
- This is just the beginning of more checks that can be done on events. A lot of other checks can be done using modules and data structures. For example; Redis provides geospatial data structures built over sorted sets. Since latitude and longitude can be derived from IP using IP to location conversion providers, a lot of insight can be derived on whether the event can be fraudulent or not.
- To reject servicing requests altogether, the redis-cell module to rate limit requests against a key can be used.

## Next steps

Now that you've built a basic fraud detection system with Redis, explore these related tutorials to expand your fraud prevention capabilities:

- [Transaction Risk Scoring with Redis](/tutorials/howtos/solutions/fraud-detection/transaction-risk-scoring/) — Learn how to score transactions for risk in real time using Redis data structures, adding another layer to your fraud detection pipeline.
- [Digital Identity Validation with Redis](/tutorials/howtos/solutions/fraud-detection/digital-identity-validation/) — Discover how to validate digital identities using Redis to prevent identity-based fraud alongside your transaction monitoring.
- [Build modern fraud-detection platforms with Redis Cloud](https://redis.io/solutions/fraud-detection/) — See how Redis Cloud provides an enterprise-grade foundation for fraud detection at scale.

## References and Links

- [Source Code](https://github.com/redis-developer/redis-datasets/tree/master/use-cases/fraud-detection)
- [Build modern fraud-detection platforms with Redis Cloud](https://redis.io/solutions/fraud-detection/)
