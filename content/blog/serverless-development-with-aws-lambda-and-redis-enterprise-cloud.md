---
title: "Serverless Development with AWS Lambda and Redis Enterprise Cloud"
linkTitle: "Serverless Development with AWS Lambda and Redis Enterprise Cloud"
url: "/blog/serverless-development-with-aws-lambda-and-redis-enterprise-cloud/"
description: "In this blog post, you will learn how to integrate AWS Lambda and Redis Enterprise Cloud. Using a sample movie-database application, you will discover how to build and deploy two Lambda functions,..."
date: 2020-12-15
blogCategories:
- "Tech"
authors:
- "Tugdual Grall"
lastmod: 2025-03-27
hidden: true
---

*By Tugdual Grall, Technical Marketing Manager · Published 15 December 2020 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/04e20abfc0d47f2155c49d092b42104c4e652d0e-1393x829.webp)

In this blog post, you will learn how to integrate [AWS Lambda](https://aws.amazon.com/lambda/) and [Redis Enterprise Cloud](/try-free/). Using a sample movie-database application, you will discover how to build and deploy two Lambda functions, one in [Node.js](https://nodejs.org/), one in [Python](https://www.python.org/). These two Lambda functions are used to interact with the Redis database to insert, update, delete, and query. The application uses the [RediSearch](https://redis.comevents-and-webinars/search/) API that provides rich query and search functionalities. [Serverless](https://aws.amazon.com/serverless/), using AWS Lambda, fits into the growing trend towards microservice architectures as it allows developers to reduce the scope of a business “service” into a small project that can be implemented using the programming language of their choice. To learn more, watch the video below and read on for a quick overview of AWS Lambda and a deeper dive into how to build an application using Redis Enterprise Cloud and Lambda:

[Click here to view video](https://www.youtube.com/embed/UJHk1cTfs3g)

## A quick look at AWS Lambda

If you’re not already familiar with AWS Lambda—the company’s serverless compute runtime, also known as a Function-as-a-Service ([FaaS)](https://en.wikipedia.org/wiki/Function_as_a_service)—here are the basics you need to know. (Lambda experts can jump ahead to the next section.) AWS Lambda allows applications to run a function on demand in response to a particular event, making it a good way to build event-driven architecture (EDA) applications. AWS Lambda functions, fully managed by AWS, can be created using various [programming languages](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html). Perhaps the best part of AWS Lambda is that developers don’t usually need to fully understand the application lifecycle to use it.

AWS Lambda can be invoked using several different methods: directly from the AWS Console, using events from other AWS Services such as [SNS](https://aws.amazon.com/sns/), [SQS](https://aws.amazon.com/sqs/), or [Kinesis](https://aws.amazon.com/kinesis/), or even from the AWS Console, [CloudWatch](https://aws.amazon.com/cloudwatch/), or [S3](https://aws.amazon.com/s3/) events. In our sample movie-database application, the Lambda functions will be invoked using an HTTP REST endpoint, this is done using the [AWS API Gateway](https://aws.amazon.com/api-gateway/). (You can find more about AWS Lambda function invocation [in the documentation](https://docs.aws.amazon.com/lambda/latest/dg/lambda-invocation.html).)

**AWS Lambda HTTP execution process**

Specifically, requests via HTTP are routed to AWS’ API Gateway management tool, which parses the body, header, and parameters, and then triggers our Lambda function with this payload:

![](/images/site-mirror/5a6f695c1c5da9f2c2ac8aa1e7478dc189a72625-1024x215.webp)

*Exposing a AWS Lambda function in the API Gateway.*

As a developer, you simply write code to expose the REST endpoint and configure the deployment to expose it inside the AWS API Gateway. (We’ll discuss this further in the next section covering our sample movie-database application.)

**State and data management in serverless applications**

AWS Lambda is a stateless environment. In many applications, though, you still want to share state between services or calls, and Redis can help. For simple state management, AWS developers often use ElastiCache, but many applications require more than state management, they also need persistence, rich data, high performance, and a query model. [Redis Enterprise Cloud](/redis-enterprise-cloud/overview/) provides a fully managed service on AWS (Google Cloud and Microsoft Azure are also supported).

## Redis movie-database sample application

Now we’re ready to look at our sample movie-database application to see the key steps to build an application using Redis Enterprise Cloud and AWS Lambda.

The application uses the dataset that has been documented in the [RediSearch Getting Started tutorial](https://github.com/RediSearch/redisearch-getting-started/blob/master/docs/003-create-index.md#sample-dataset), which consists of a movie catalog, made of Redis Hashes. As shown in the chart below, the frontend is built using [Vue.js](https://vuejs.org/), which calls REST endpoints to:

- List, sort, and filter movies
- Edit movies and add/delete comments
- Search movies using full-text search and faceted search

![](/images/site-mirror/86598a6d0b42e9904b00966f0be400f7cde17307-1024x609.webp)

![](/images/site-mirror/77a1a3b250012f5aa95e53883bb73f2b7814e125-960x540.gif)

*A demo of the sample movie-database application using AWS Lambda functions.*

As mentioned above, the application leverages the AWS API Gateway, AWS Lambda, and Redis Enterprise Cloud for the datastore. In addition, the Python service uses [AWS Key Management Service](https://aws.amazon.com/kms/) to store and encrypt the Redis database password.

## Install and run the demonstration application

To get started, you’ll need a few prerequisites:

- An [AWS account setup](https://aws.amazon.com/), credentials, with the [CLI Installed](https://aws.amazon.com/cli/)
- A Redis Enterprise Cloud [account and database, with the RediSearch module enabled](/modules/get-started/)
- [Git](https://git-scm.com/)
- [Node.js](https://nodejs.org/)
- [Python](https://www.python.org/)
- The [Redis command line interface (CLI)](https://redis.io/topics/rediscli)

Once you have everything assembled, let’s walk through the process of installing and running the sample application.

**Step 1: Get the Redis Enterprise Cloud database information**

If you have not yet created a database on Redis Enterprise Cloud, please do so using the information in our [Get Started with Redis Modules](/modules/get-started/) guide.

When you are connected to the Redis Enterprise Cloud, you can find the database connection information in the web console; be sure you add the module “RediSearch 2” to the database.

![](/images/site-mirror/a46f194ecaf194a834dd9ecf44101e6abd0786d5-962x296.webp)

*Redis Enterprise Cloud database information for our sample movie-database application.*

You will need the following properties to connect the Lambda functions to your Redis database:

- REDIS_HOST: redis-18541.xxx.xxxx.xxx.cloud.redis.com
- REDIS_PORT: 18541
- REDIS_PASSWORD : <the password showed on the screen>

**Step 2: Get the project from GitHub**

Clone the repository to your local environment, and move it to the project directory

```javascript
> git clone https://github.com/redis-developer/aws-redis-cloud-demo.git

> cd aws-redis-cloud-demo
```

The project directory structure is shown here:

```javascript
aws-redis-cloud-demo
├── README.md
├── front-end                   => Vue.js project
│   ├── .env.development        => to set the Lambda URLs in dev mode
│   ├── .env.production         => to set the Lambda URLs in production mode    
│   ├── ...
│   └── vue.config.js
│   └── ...
├── movie-comments-microservice => The Python, comments service
│   ├── .chalice
│   │   └── config.json         => Lambda & Service configuration  
│   ├── app.py
│   ├── chalicelib              => Contains application code and lib
│   │   └── ….
│   ├── readme.md
│   └── requirements.txt
└── movies-list-microservice    => The Node.js, movie service
    ├── import_movies.redis     => Dataset file
    ├── ...
    ├── serverless.yml          => Lambda & Service configuration
    ├── src
    │   └── ...
    └── ...
```

**Step 3: Import the movie-database dataset into your application**

The file aws-redis-cloud-demo/movies-list-microservice/import_movies.redis contains all the Redis commands to insert movies into the database. The commands used are:

- [HSET](https://redis.io/commands/hset) for each movie
- [FT.CREATE](https://redis.io/commands/ft.create/) to create a RediSearch index.

To import the dataset, open a terminal and run the following command:

```javascript
> export REDISCLI_AUTH=<YOUR_DB_PASSWORD>
> redis-cli -h redis-18541.xxx.xxxx.xxx.cloud.redis.com \
        -p 18541 < movies-list-microservice/import_movies.redis
```

**Step 4: Configure the application to use your Redis Enterprise Cloud instance**

Before testing the application, you must configure the Node.js and Python services with your Redis Enterprise Cloud database instance. Open these files:

- ./movies-list-microservice/serverless.yml
- ./movie-comments-microservice/.chalice/config.json

Then set the Redis host, port, and password: (REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)

**Step 5: Build and run the movie microservice (Node.js)**

Follow the steps listed here to build and run the project. (You can also find all the information in the project’s [Readme file](https://github.com/redis-developer/aws-redis-cloud-demo/blob/main/movies-list-microservice/README.md).)

1. Install the [serverless](https://www.serverless.com/) framework

```javascript
> npm install -g serverless
```

2. Go to the movies-list-microservice directory

```javascript
> cd movies-list-microservice
```

3. Install dependencies

```javascript
> npm install
```

4. Run the Lambda function locally

```javascript
> npm start
```

5. Test the service by opening a browser call to the REST service: [http://localhost:3000/api/movies/1](http://localhost:3000/api/movies/1)

6. Deploy the service to AWS, by running the following command to deploy the function to your AWS environment:

```javascript
> serverless deploy
................................
Serverless: Stack update finished...
Service Information
service: movies-list-microservice
stage: api
region: us-east-1
stack: movies-list-microservice-api
resources: 33
api keys:
  None
endpoints:
  GET - https://<xxx>.execute-api.<reg>.amazonaws.com/api/movies/search
  GET - https://<xxx>.execute-api.<reg>.amazonaws.com/api/movies/group_by/{field}
  GET - https://<xxx>.execute-api.<reg>.amazonaws.com/api/movies/{id}
  POST - https://<xxx>.execute-api.<reg>.amazonaws.com/api/movies/{id}
functions:
  listMovies: movies-list-microservice-api-listMovies
  searchMovies: movies-list-microservice-api-searchMovies
  getMovie: movies-list-microservice-api-getMovie
  saveMovie: movies-list-microservice-api-saveMovie
layers:
  None
```

7. Test the API by pointing your browser to https://<xxx>.execute-api.<reg>.amazonaws.com/api/movies/1

Note: if you receive an error, check the functions log in [AWS CloudWatch](https://aws.amazon.com/cloudwatch/) to see what happened.

***A deeper look at the code:***

- The [package.json](https://github.com/redis-developer/aws-redis-cloud-demo/blob/main/movies-list-microservice/package.json) file contains the dependencies used by this Node.js project. This project is quite simple, and uses the following dependencies:
  - The [redis](https://www.npmjs.com/package/redis) and [redis-redisearch](https://www.npmjs.com/package/redis-redisearch) libraries are used to connect to Redis and exposed RediSearch commands.
  - The [aws-lambda](https://www.npmjs.com/package/aws-lambda) library is used to call all the AWS Lambda functions to deploy a node application to your AWS environment.
- The [serverless.yml](https://github.com/redis-developer/aws-redis-cloud-demo/blob/main/movies-list-microservice/serverless.yml) file defines the serverless functions mapping HTTP actions to the JavaScript function that will be called (defined in handler.ts), and contains the environment variables (mostly a Redis connection string in this demonstration).
- The [handler.ts](https://github.com/redis-developer/aws-redis-cloud-demo/blob/main/movies-list-microservice/src/handler.ts) file is the class that captures the event coming from the AWS Gateway and calls the application library SearchService, which is doing all the calls to the Redis database.
- The [SearchService.ts](https://github.com/redis-developer/aws-redis-cloud-demo/blob/main/movies-list-microservice/src/services/SearchService.ts) file contains all the methods to interact with the Redis database and use the Redis and RediSearch API: client.ft_search(), client.aggregate(), client.hmset(), and more. (You can learn more about the Redis and RediSearch commands at [Redis University](https://university.redis.com/) and the [Getting Started with RediSearch 2.0 tutorial on GitHub](https://github.com/RediSearch/redisearch-getting-started/blob/master/README.md).

**Step 6: Build and run the comments microservice (Python)**

Here are the steps to build and run the project. (You can also find all the information in the project’s [Readme file](https://github.com/redis-developer/aws-redis-cloud-demo/blob/main/movie-comments-microservice/README.md).)

1. Move to the Python project and create a virtual environment:

```javascript
> cd movie-comments-microservice

> python3 -m venv chalice-env

> source chalice-env/bin/activate
```

2. Install the dependencies:

```javascript
> pip install -r requirements.txt
```

3. Set up the AWS environment, run the following command, and configure your ID and Secret:

```javascript
> aws configure

AWS Access Key ID [None]: ****************ABCD
AWS Secret Access Key [None]: ****************abCd
Default region name [None]: us-west-2
Default output format [None]:
```

4. Deploy the service to AWS, by running the following command to deploy the function to your AWS environment:

```javascript
> chalice deploy

Reusing existing deployment package.
Updating policy for IAM role: movie-comments-microservice-dev
Creating lambda function: movie-comments-microservice-dev
Creating Rest API
Resources deployed:
  - Lambda ARN: arn:aws:lambda:us-east-1:11111111111:function:movie-comments-microservice-dev
  - Rest API URL: https://XXXXXXX.execute-api.us-east-1.amazonaws.com/api/
```

***A deeper look at the code:***

- The [requirements.txt](https://github.com/redis-developer/aws-redis-cloud-demo/blob/main/movie-comments-microservice/requirements.txt) file contains the dependencies used by this Python project. This project is quite simple, and uses the following dependencies:
  - [Chalice](https://aws.github.io/chalice/) is the AWS framework used to create serverless applications in Python
  - [redis](https://pypi.org/project/redis/) and [redisearch](https://pypi.org/project/redisearch/) access Redis and use the RediSearch API
- The [config.json](https://github.com/redis-developer/aws-redis-cloud-demo/blob/main/movie-comments-microservice/.chalice/config.json) file defines the serverless application and is used to define the environment variables—in this application, the Redis database connection information.
- The [app.py](https://github.com/redis-developer/aws-redis-cloud-demo/blob/main/movie-comments-microservice/app.py) file is the application entry point that defines all the REST endpoints using various routes. The application imports various dependencies, especially the CommentService that is used to interact with Redis. When you want to use multiple files you must put the files in the [chalicelib](https://aws.github.io/chalice/topics/multifile) folder.
- The [comment_service.py](https://github.com/redis-developer/aws-redis-cloud-demo/blob/main/movie-comments-microservice/chalicelib/services/comments_service.py) file contains all the interactions with Redis to create, query and delete comments. An interesting point for the comment feature is the search() method. This method is used to retrieve the comments for a movie sorted by the date of creation using a search_client.search() call.

*Optionally, you can store the Redis database password in *[*AWS Key Management Service*](https://aws.amazon.com/kms/)*. You can find the configuration steps in the project *[*documentation*](https://github.com/redis-developer/aws-redis-cloud-demo/tree/main/movie-comments-microservice#setting-up-kms)*.*

**Step 7: Run the frontend application**

1. Go to the frontend directory and install the dependencies:

```javascript
> cd front-end

> npm install
```

2. Edit the .env.development file to set the URL of the movie and comment services:

```javascript
VUE_APP_MOVIES_SERVICE=https://<xxx>.execute-api.<reg>.amazonaws.com/api
VUE_APP_COMMENTS_SERVICE=https://<xxx>..execute-api.<reg>.amazonaws.com/api
```

3. Run the application:

```javascript
> npm run serve
```

4. Open your browser, and go to [http://localhost:8084](http://localhost:8084)

You can now navigate in the application, update and search movies, and add/delete comments.

*Optionally, you can use S3 and *[*CloudFront*](https://aws.amazon.com/cloudfront/)* to deploy the Vue application in your AWS environment and serve it publicly to your users. This is explained in the project *[*documentation*](https://github.com/redis-developer/aws-redis-cloud-demo/tree/main/front-end#deploying-to-s3)*.*

## Conclusion

Working with AWS Lambda and Redis Enterprise Cloud simplifies the deployment of your services. Using Redis Enterprise Cloud with RediSearch, you can easily query Redis data using values, allowing you to use Redis as the main database of your services.

Redis Enterprise Cloud is compatible with Redis, allowing you to [easily migrate](/redis-enterprise-cloud/migrate/) your existing Redis deployments, both OSS and managed services. You just need to change the connection parameters (such as database endpoints). There are multiple ways to perform a live migration, including:

- Blue-green deployments
- Synchronizing Amazon ElastiCache and Redis Enterprise Cloud using [Active Passive Geo-Distribution](/redis-enterprise/technology/active-passive-geo-distribution/)
- Using our open source [RIOT tool ](https://github.com/redis-developer/riot)to migrate your data

In addition to [RediSearch](/search/), Redis Enterprise Cloud lets you use other promising data models such as [graph](/modules/redis-graph/), [JSON](/json/), [time series](/timeseries/), and [Bloom filters](/modules/redis-bloom/), and offers a wide variety of other database features critical in production environments, including [high availability](/redis-enterprise/technology/highly-available-redis/), [scalability](/redis-enterprise/technology/linear-scaling-redis-enterprise/), [persistence](/redis-enterprise/technology/durable-redis-2/), [security](/redis-enterprise/technology/enterprise-grade-redis-security/), and [Active-Active geo-distribution](/active-active/).

Want to learn more? Check out our [AWS re:Invent home page](/aws-reinvent/) and read these tutorials and blog posts:

- [Get Started with Redis Modules on AWS](/modules/get-started/)
- [6 Key Features to Consider When Choosing a DBaaS Provider](/blog/6-key-features-to-consider-when-choosing-a-dbaas-provider/)
- [How Redis Enterprise Cloud Meets the Needs of Maturing Enterprise Customers on AWS](/blog/how-redis-enterprise-cloud-meets-the-needs-of-maturing-enterprise-customers-on-aws/)
- [Watch our recent Tech Talk on how to scale and turbocharger your Redis in AWS](/events/scaling-and-turbocharging-redis-in-aws/)
