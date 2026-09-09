---
title: "Redis AI First Steps"
linkTitle: "Redis AI First Steps"
url: "/blog/redis-ai-first-steps/"
description: "At RedisConf 2019, Redis introduced a new module called RedisAI. The idea is to bring together machine learning (ML) and deep learning (DL) and execute artificial intelligence (AI) models as close..."
date: 2019-06-17
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-04
hidden: true
---

*By Redis   · Published 17 June 2019 · updated 4 March 2025*

![Blog tile image](/images/blog/32db3a71c9b8f27e19a2b7b93fc2526a2976834a-542x464.webp)

At RedisConf 2019, Redis [introduced](https://www.youtube.com/watch?v=u9dKmRQj3wE) a new module called RedisAI. The idea is to bring together machine learning (ML) and deep learning (DL) and execute artificial intelligence (AI) models as close as possible to where your data currently lives. This sounds amazing, but what if you’re brand new to all of this? What if you’re interested in machine learning, but you’re not quite sure what the heck it all means? How do you make sense of it all? Your boss’ boss is saying, “we need to integrate machine learning,” and last week you thought that meant he wanted you to run an extra compile step or something. Now you’re sitting here trying to understand a lot of new terms and how you can bring this into your organization.

Okay, first, take a deep breath and let’s take a step back. Today, we’ll start digging into some AI lingo and show you how to add the RedisAI module into your already existing Redis system and start to play around with this stuff.

## What is machine learning again?

So what exactly is machine learning? The broad concept refers to building algorithms that read data and make predictions based on that data as well as any new data that comes in. During the initial “training” period, someone looks at the model’s predictions and tells the system if each guess is good or bad. Deep learning involves building algorithms and feeding the model data, but rather than outside training, the system trains itself.

Training these systems is complex and usually happens in a totally different application (don’t worry, you don’t need to write that application unless you enjoy linear algebra). One of the most popular systems for machine learning is called [TensorFlow](https://www.tensorflow.org/) and it’s open source. TensorFlow helps you build, train and deploy ML applications and has a great community to help you get started.

## ML in the wild

You probably already interact with ML systems more than you realize. If you have a Netflix account and you click “like” or “dislike” on a certain movie or show, you’re training a model to better predict what types of movies and shows you’d enjoy. Netflix’s suggestions are directly related to the things you say you like. Sadly, this is why my queue is filled with things like [True and the Rainbow Kingdom](https://www.imdb.com/title/tt5607658/) (thanks kids).

Also, if you’ve been on the internet in the past couple of years, you’ve no doubt seen the explosion of chatbots. These are also ML/DL tools. They’re trained to answer questions and in some cases can hold pretty good conversations with a person around related topics. Of course, training can sometimes [go off the rails](https://en.wikipedia.org/wiki/Tay_(bot)), but if nothing else, it’s fun to watch!

## Where does Redis fit in?

Traditionally, all this data needs to be moved around, and that can present some serious DevOps challenges. Think about a chatbot saving the state of your conversation. That data needs to live somewhere because it’s important to the bot. It needs this conversation and context to help craft what it’s going to say next. We’d need to deserialize the data, run it through the model, and then serialize the data once it’s sent back to Redis. Doing all this uses CPU cycles and network overhead to go from one app to another and translate data between systems.

RedisAI gives you new data structures and allows Redis to manage requests to run models and execute them. Essentially, we’re running your models right where your data lives. No network overhead, no serializing/deserializing.

## How do I get started?

I’m an old-fashioned kinda guy and I like to build tools like this myself. So when I want to play around with a new module for Redis, I go to the source and build it. We’ve got a couple of different ways you can get RedisAI running locally:

### Either Install via Docker…

If you’re a Docker user, it’s trivial to get an instance of Redis with RedisAI on your system:

$ docker pull redisai/redisai

$ docker run -p 6379:6379 -it --rm redisai/redisai

You’ll still want to clone the [RedisAI repo](https://github.com/RedisAI) to get access to examples.

### …or build from source

Let’s get our hands dirty in the command line. Now, before you can make the code, you need to install two particular things: cmake and git-lfs. On my Macbook, this was as simple as using Homebrew:

$ brew install git-lfs cmake

You also need to make sure you’re running redis-server version 4.09 or greater. If you need to check, type:

$ redis-server --version

Now that you’ve checked your server version and know you’re good there, go out and clone the AI repository:

$ git clone git@github.com:RedisAI/RedisAI.git

Cd yourself into the RedisAI repo and get the dependencies:

$ bash get_deps.sh

Now build:

$ mkdir build

$ cd build

$ cmake -DDEPS_PATH=../deps/install ..

$ make

$ cd ..

If all goes according to plan, you’re ready to load the module and start playing. The process should be pretty smooth. The only issues I ran into were not having CMake installed. Once I did that, the whole process worked.

Now, before you go any further, you should make sure the Redis server isn’t running. I had forgotten that I always start it as a service on my machine, so it was just running in the background! When I was trying to load the module, everything seemed like it was working fine, but the module wasn’t actually loading. With the Redis server already running in the background, things got wonky on me and the module wasn’t loading. If you’ve used Homebrew to install Redis, stopping the Redis server should be a simple command. brew services stop Redis on my Mac does the trick.

Once you’ve stopped Redis, you can run:

$ redis-server --loadmodule build/redisai.so

You could make your life a little easier by just using the MODULE LOAD command from the CLI:

> MODULE LOAD path/to/build/redisai.so

Now, load the module into the server and you can start playing around!

## Playing with some examples

Congratulations on making it this far, now the fun begins. You have everything you need to experiment with RedisAI. If you’re new to all of this, you might not be sure of the next step, so RedisAI comes with an example you can run to see things working.

If these are your first steps into the AI world, the next thing you need to do is build and train a model. These steps are out of scope for Redis and this article (but if you’re interested, there’s some [great material available](https://github.com/nlintz/TensorFlow-Tutorials)), so we’re going to skip all that and give you some data that you can play around with right away.

I’ve set up a [repo on Github](https://github.com/JoeCianflone/redisai-example) that you can download and play around with an example Inside that folder you’ll find everything you need to get started:

![](/images/blog/86bcfbda99fc2be82febbd66980d268899b7f36d-717x130.webp)

Our example project is a CLI image classification app. We’ll give it an image and the app should be able to figure out what’s in the image. For example, we have an image of a panda, and when we give the app the picture, the app should tell us that there’s a giant panda in the image.

To get this up and running, cd into the JS folder and run either yarn or npm install. Everything you’ll need to get it going will be installed. Then all you have to do is run:

$ node mobilenet.js ../img/panda.jpg

The panda.jpg image is the header image of this blog post. If all goes well, your output should look similar to this:

![](/images/blog/08573c8c03fd890b1bc7bc0b73e518ce88b07e1a-718x226.webp)

Awesome, we got something back! Great? What does this mean exactly, what did we do? We supplied our node app a picture of a panda and a computer. Our system was trained to look at images and tell us what’s in the picture. So what we’ve done here is supply our app 2 images and the app was able to tell us what it “saw” in the images.

Quickly, we’ve been able to set up RedisAI in our Redis instance so you can give it data and watch it figure out and classify the images you give it. This example is the basic building block of facial recognition and image recognition. Now with RedisAI we’re able to work where our data lives, in Redis.
