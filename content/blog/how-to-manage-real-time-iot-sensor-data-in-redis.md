---
title: "How to Manage Real-Time IoT Sensor Data in Redis"
linkTitle: "How to Manage Real-Time IoT Sensor Data in Redis"
url: "/blog/how-to-manage-real-time-iot-sensor-data-in-redis/"
description: "Imagine you’re an air-conditioner manufacturing company that sells millions of smart AC units to consumers. You are building a centralized, smart climate control system that collects sensor data..."
date: 2021-02-02
blogCategories:
- "Tech"
authors:
- "Ajeet Raina"
lastmod: 2025-03-27
hidden: true
---

*By Ajeet Raina, Technical Marketing Manager · Published 2 February 2021 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/3ab9a5e76621e9e3c8b7b5bac221b9db66dc0dd6-1999x695.webp)

![](/images/site-mirror/3781b0e5b1f939a749a1cc2200c914e565052e86-1024x356.webp)

Imagine you’re an air-conditioner manufacturing company that sells millions of smart AC units to consumers. You are building a centralized, smart climate control system that collects sensor data about a house’s temperature, pressure, and humidity and sends it to a central location for an efficiency analysis to help end users trim their electricity bills.

This blog post will show a simplified version of such a use case to demonstrate how it all works—so you can understand how to manage a wide variety of real-time IoT sensor data in Redis.

Here’s what we used:

1. A[**BME680 environmental sensor**](https://shop.pimoroni.com/products/bme680-breakout) to simulate a smart air conditioner and send data to Redis
1. The[**RedisTimeSeries module**](/timeseries/) to add time-series capabilities to Redis and store the data in time-series format
1. [**Grafana with Redis Data Source**](https://grafana.com/grafana/plugins/redis-datasource) to create graphs for usage analysis

![](/images/site-mirror/adc1855790479608f47e78d7327f4846056d8dec-1024x419.webp)

**Hardware requirements:**

- [Jetson Nano: ](https://developer.nvidia.com/buy-jetson?product=jetson_nano&location=US)2GB Model ($59)
- A 5V 4Amp charger
- [128GB SD card](https://www.amazon.com/SanDisk-128GB-microSDXC-Memory-Adapter/dp/B073JYC4XM)
- [BME680 sensors](https://cdn-shop.adafruit.com/product-files/3660/BME680.pdf)

**Software requirements:**

- Jetson SD card image from [NVIDIA](https://developer.nvidia.com/embedded/downloads)
- [Etcher software](https://www.balena.io/etcher/) installed on your system

## Preparing Your Jetson Nano for OS Installation

- Unzip the SD card image downloaded from [https://developer.nvidia.com/embedded/downloads.](https://developer.nvidia.com/embedded/downloads)
- Insert the SD card into your system.
- Bring up the Etcher tool and select the target SD card to which you want to flash the image.

![](/images/site-mirror/a0ac0945fb2e3e6afa030f45e45c132fd3a12614-1024x597.webp)

Follow this 10-step process to see how it all fits together:

## Step 1: Get your sensors

![](/images/site-mirror/827ab4d828fee3084880a92066231f7812c6db41-1024x1024.webp)

There’s a huge variety of sensors on the market, but this demonstration uses a Pimoroni BME680 breakout board. [BME680](https://cdn-shop.adafruit.com/product-files/3660/BME680.pdf) is an integrated environmental sensor developed for mobile applications and wearables, where size and low power consumption are key requirements. It can measure temperature, pressure, humidity, and indoor air quality, and is Raspberry Pi and Arduino-compatible.

## Step 2: Set up your IoT board

![](/images/site-mirror/9199492c37ac544a873854de250e95370df3a85a-1024x762.webp)

For this demonstration, we’re using an [NVIDIA ](https://developer.nvidia.com/embedded/jetson-nano)[**Jetson Nano**](https://developer.nvidia.com/embedded/jetson-nano)[ board](https://developer.nvidia.com/embedded/jetson-nano), a small, powerful computer for developers to learn, explore, and build AI applications for edge devices. Priced at $59, it’s basically a developer kit that includes a Jetson Nano module with 2GB memory and delivers 472 GFLOPS of compute power. This demonstration should also work with other popular IoT devices, such as the Raspberry Pi, Arduino, Banana Pi, etc.

## Step 3: Wire it up

The BME680 plugs directly into a Jetson Nano board without any connecting wires.

![](/images/site-mirror/b927723eb5b4dd3f319248d4624160da218ea691-768x1024.webp)

## Step 4: Get your sensor working

After wiring the sensors, we recommend running I2C detection with i2cdetect to verify that you see the device: in our case it shows 76. Please note that the sensor communicates with a microcontroller using I2C or SPI communication protocols.

```javascript
$ i2cdetect -r -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- 76 --
```

## Step 5: Get ready to Redis

You will need a Redis server up and running, either on your local laptop or in the cloud, and the Redis server must be compiled with the RedisTimeSeries module. In this demonstration, we’re using [Redis Enterprise Cloud](/redis-enterprise-cloud/overview/), a fully managed cloud database service that comes with the RedisTimeSeries module already built in and integrated.

## Step 6: Set up Redis Enterprise Cloud

If you are completely new to RedisTimeSeries, check out our [RedisTimeSeries Quick Start tutorial](https://redis.io/docs/data-types/timeseries/quickstart/). It explains how to get started with Redis Enterprise Cloud and how to enable RedisTimeSeries. You will need a few details for this implementation:

- Redis database name
- Redis database endpoint
- Port number
- Default user password

![](/images/site-mirror/2572c476f599233da5b1ce6773e36619a701e7d4-1024x689.webp)

## Step 7: Clone the project repository

```python
$ git clone https://github.com/redis-developer/redis-datasets
$ cd redis-datasets/redistimeseries/realtime-sensor-jetson

```

Reading the sensor values from the BME680 is fairly straightforward, but requires you to set a few configuration values. You can also run the sensor in two different “modes”—with or without gas readings. Just taking temperature, pressure, and humidity readings lets you sample data much faster.

Let’s look first at the library import and the configuration settings. Open a terminal window, create a file, and then type the following:

```python
import bme680
import time
import datetime
import csv
import argparse
import redis

```

The first module, **bme680,** allows you to easily write Python code that reads the humidity, temperature, and pressure from the sensor. Similarly, there are other Python modules, such as **time, **to handle time-related tasks, **redis **to import Redis Python modules, and so on. We’re using the time library to introduce a small delay between each reading of the sensor to help ensure consistent results.

```python
print("""read-sensor.py - Displays temperature, pressure, humidity, and gas.
Press Ctrl+C to exit!
""")

try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except IOError:
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

# These calibration data can safely be commented
# out, if desired.

print('Calibration data:')
for name in dir(sensor.calibration_data):

    if not name.startswith('_'):
        value = getattr(sensor.calibration_data, name)

        if isinstance(value, int):
            print('{}: {}'.format(name, value))

# These oversampling settings can be tweaked to
# change the balance between accuracy and noise in
# the data.

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

```

The **sensor = bme680.BME680()** command creates an instance of the sensor that we’ll use to configure the settings and get the sensor’s readings. The **_oversample** settings we established for the humidity, pressure, and temperature measurements are designed to strike a balance between accurate readings and minimizing noise. The higher the oversampling, the greater the noise reduction, albeit accompanied by a reduction in accuracy.

The **_filter** protects sensor readings against transient changes in conditions, e.g. a door slamming that could cause the pressure to change momentarily, and the IIR filter removes these transient spiky values.

Shown in the code below, the gas measurement has a few settings that can be tweaked. It can be enabled or disabled with **set_gas_status**. Disabling it allows the other readings to be taken more rapidly, as mentioned above. The temperature of the hot plate and how long it’s held at that temperature can also be altered, although we recommend not changing these settings if your gas resistance readings look sensible.

```python
print('\n\nInitial reading:')
for name in dir(sensor.data):
    value = getattr(sensor.data, name)

    if not name.startswith('_'):
        print('{}: {}'.format(name, value))

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)

# Up to 10 heater profiles can be configured, each
# with their own temperature and duration.
# sensor.set_gas_heater_profile(200, 150, nb_profile=1)
# sensor.select_gas_heater_profile(1)


parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, help="redis instance port", default=6379)
parser.add_argument(
    "--password", type=int, help="redis instance password", default=None
)
parser.add_argument("--verbose", help="enable verbose output", action="store_true")
parser.add_argument("--host", type=str, help="redis instance host", default="127.0.0.1")


args = parser.parse_args()

```

Next, we define the **Redis connector, **where we specify the Redis instance host, port, and password. As shown below, the code below defines the various RedisTimeSeries keys, such as a temperature key (TS:TEMPERATURE), pressure key (TS:PRESSURE), and humidity key (TS:HUMIDITY).

```python
# redis setup
redis_obj = redis.Redis(host=args.host, port=args.port, password=args.password)
temperature_key = "ts:temperature"
pressure_key = "ts:pressure"
humidity_key = "ts:humidity"

```

The sensor.get_sensor_data() instruction gets the data from the sensor and populates the three variables with temperature, humidity, and pressure.

Next, a “transactional pipeline” is constructed by calling the .pipeline() method on a Redis connection without arguments. Under the covers, the pipeline collects all the commands that are passed until the .execute() method is called. As you can see, we used RedisTimeSeries’ TS.ADD command to populate the sensor data structure. You can access the complete code via this [GitHub Repository](https://github.com/redis-developer/redis-datasets/blob/master/redistimeseries/realtime-sensor-jetson/sensorloader.py).

## Step 8: Execute the script

Before you execute the script, you will need to import the bme680 and smbus Python modules, as shown here:

```python
$ pip3 install bme680

```

```python
$ pip3 install smbus

```

Make sure you supply the right Redis Enterprise Cloud database endpoints, username, and password:

```python
$ python3 sensorloader.py --host <Redis Enterprise Cloud host> --port <port>  --password <password> 

```

You can run the monitor command to verify that sensor data is being populated, as shown here:

```python
$ redis-cli -h redis-12929.c212.ap-south-1-1.ec2.cloud.redislabs.com -p 12929
redis-12929.c212.ap-south-1-1.ec2.cloud.redislabs.com:12929> auth <password>
OK
redis-12929.c212.ap-south-1-1.ec2.cloud.redislabs.com:12929> monitor
OK
1611046300.446452 [0 122.179.79.106:53715] "info" "server"
1611046300.450452 [0 122.179.79.106:53717] "info" "stats"
1611046300.450452 [0 122.179.79.106:53716] "info" "clients"
1611046300.486452 [0 122.179.79.106:53714] "info" "memory"
1611046300.486452 [0 122.179.79.106:53713] "info" "server"
1611046300.494452 [0 122.179.79.106:53715] "info" "memory"
1611046300.498452 [0 122.179.79.106:53717] "info" "commandstats"
1611046300.522452 [0 122.179.79.106:53716] "dbsize"
1611046301.498452 [0 122.179.79.106:53714] "info" "memory"
1611046301.498452 [0 122.179.79.106:53713] "info" "server"
1611046301.498452 [0 122.179.79.106:53715] "info" "server"
1611046301.498452 [0 122.179.79.106:53716] "info" "clients"
1611046301.498452 [0 122.179.79.106:53717] "info" "stats"
1611046301.554452 [0 122.179.79.106:53714] "info" "memory"
1611046301.562452 [0 122.179.79.106:53717] "info" "commandstats"

```

## Step 9: Deploy Grafana

It’s exciting to see the sensor data plotted in Grafana. To implement this, run the command below:

```python
$ docker run -d -e "GF_INSTALL_PLUGINS=redis-app" -p 3000:3000 grafana/grafana

```

Be sure that you have [Docker Engine](https://www.docker.com/products/container-runtime) running in your system, either on your desktop system or in the cloud. For this demonstration, I have tested it on [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop).

Point your browser to https://<IP_ADDRESS>:3000. Use “admin” as username and password to log in to the Grafana dashboard.

![](/images/site-mirror/9bd0d0a532c8fa0f9b48d07b52db2d2a39cef7ec-1024x982.webp)

Click the Data Sources option on the left side of the Grafana dashboard to add a data source.

![](/images/site-mirror/1ba23f00c39956980046da3117421fc382e31f05-1024x513.webp)

Under the Add data source option, search for Redis and the Redis data source will appear as shown below:

![](/images/site-mirror/72da1b2a4de03cf8911d97d59a63eaf63bf955c7-1024x648.webp)

![](/images/site-mirror/50a9d0b6e29145985e7af81d6af04f4b8c5c9370-1024x489.webp)

Supply the name, Redis Enterprise Cloud database endpoint, and password, then click Save & Test.

![](/images/site-mirror/544b4527a62f10a2d328cf33ac552cd7dce2cb0a-906x1024.webp)

Click Dashboards to import Redis and Redis Streaming. Click Import for both these options.

![](/images/site-mirror/012fe9f0773758d5bd17111898c8e3a85165ba5f-1024x425.webp)

Click on Redis to see a fancy Grafana dashboard that shows the Redis database information:

![](/images/site-mirror/e3cc002bd7109a8b4c91785b3603aeda6a8e366f-1024x253.webp)

![](/images/site-mirror/ca58dc6a9fcbfc6e98e99e1a401d68967549e8bf-1024x475.webp)

## Step 10: Plot RedisTimeSeries sensor data in Grafana

Finally, let’s create a sensor dashboard that shows temperature, pressure, and humidity. To start with temperature, first click on + on the left navigation window. Under Create option, Select Dashboard and click on the Add new panel button.

![](/images/site-mirror/efa65d12d4b7bdc2990d00fd5fa562664cd19570-1024x445.webp)

A new window will open showing the Query section. Select SensorT from the drop-down menu, choose RedisTimeSeries as type, TS.GET as command and ts”temperature as key.

![](/images/site-mirror/bf24481a31d4bfa1e146c972cd06582a564e4aaf-1024x461.webp)

Choose TS.GET as a command.

![](/images/site-mirror/1b3eb6b3cdbafcc81cf5159ed755a45fc81165ec-1024x404.webp)

Type ts”temperature as the key.

![](/images/site-mirror/f9cef15901c083f6885d2bcd63aa5084432352c4-1024x371.webp)

Click Run followed by Save, as shown below:

![](/images/site-mirror/97653db111fffe5155d4adce692c0d11220c10c3-1024x415.webp)

Now you can save the dashboard by your preferred name:

![](/images/site-mirror/bea0e8e1deaf09bb696a78f539820af5158bd86f-936x688.webp)

Click Save. This will open up a sensor dashboard. You can click on Panel Title and select Edit.

![](/images/site-mirror/feb7b300f7179ac5b70952beb2386dd2c4805f5d-1024x542.webp)

Type Temperature and choose Gauge under Visualization.

![](/images/site-mirror/16cea49974d63fea558d160ffdef8354566b1a45-494x1024.webp)

Click Apply and you should be able to see the temperature dashboard as shown here:

![](/images/site-mirror/3cbf71105a1c73af7c9a004206e33890d43fed85-1024x514.webp)

Follow the same process for pressure (ts:pressure) and humidity (ts:humidity), and add them to the dashboard. You should be able to see the complete dashboard readings for temperature, humidity, and pressure. Looks amazing. Isn’t it?

![](/images/site-mirror/657e86897fe057e19f1e9d28868d5e474623bd87-1024x902.webp)

## What’s next

This demo shows how RedisTimeSeries combines the benefits of Redis and a purpose-built time-series database. The combination allows you to easily track environmental factors by effectively storing and managing RedisTimeSeries data. Finally, by integrating Grafana with RedisTimeSeries, you can create a useful, informative dashboard that lets you zoom in and out on the charts in real time.

This sample application is just one example of the many cool things you can do with RedisTimeSeries. For more ideas, check out these interesting use cases:

[**Build Your Financial Application on RedisTimeSeries**](/blog/build-your-financial-application-on-redistimeseries/)

[**3 Real-Life Apps Built with Redis Data Source for Grafana**](/blog/3-real-life-apps-built-with-redis-data-source-for-grafana/)

[**Real-Time Observability with Redis and Grafana**](/blog/real-time-observability-with-redis-and-grafana/)
