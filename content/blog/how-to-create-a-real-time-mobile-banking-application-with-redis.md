---
title: "How to Create a Real-time Mobile Banking Application With Redis"
linkTitle: "How to Create a Real-time Mobile Banking Application With Redis"
url: "/blog/how-to-create-a-real-time-mobile-banking-application-with-redis/"
description: "Fast, accurate, and up to date, RedisBank provides you with instant access to your finances with just a few swipes on your smartphone. Since mobile banking has propelled itself forward from the..."
date: 2022-03-29
blogCategories:
- "Uncategorized"
authors:
- "Redis Growth Team"
lastmod: 2026-09-01
hidden: true
---

*By Redis Growth Team · Published 29 March 2022 · updated 1 September 2026*

![Blog tile image](/images/blog/63bee3b2dc6173ff50beacd9d16965d32c7ba5bb-772x550.webp)

Fast, accurate, and up to date, RedisBank provides you with instant access to your finances with just a few swipes on your smartphone. Since mobile banking has propelled itself forward from the financial fringes and into the mainstream, we’ve all gotten used to the idea of having our entire banking information in our pockets wherever we go.

In response to this transition towards digital, [Lars Rosenquist](https://github.com/NLxAROSA) has built an application that allows you to create your very own mobile banking application. By using Redis, all of your financial information will be available in real-time, allowing you to monitor, record, and plan your finances accurately.

Let’s take a look at how Lars managed to put this application together. But before we go into the nuts and bolts of this app, we’d like to point out that we have an exciting range of applications for you to check out on the [Redis Launchpad](https://launchpad.redis.com/).

[Click here to view video](https://www.youtube.com/embed/JEruQaQ9XpU)

So make sure to have a peak after this post!

## How to Create A Mobile Banking Application With RedisBank

1. What will you build?
1. What will you need?
1. Architecture
1. Getting started
1. Accessing the application
1. How it works
1. How to run the application on Azure Spring Cloud
1. Troubleshooting tips on Azure Spring Cloud
1. Known issues

## 1. What will you build?

You’ll build an online banking application that will provide you with real-time updates on your bank account. With RedisBank, you’ll be able to keep a close eye on your spending and adopt a healthier relationship with money.

Below we’ll walk you through each step of the building process and highlight all of the required components to bring this application to life.

Ready to get started? Ok, let’s dive straight in.

## 2. What will you need?

- [**Java**](https://www.javascript.com/): used as a high-level, object-oriented programming language.
- [**Spring Boot**](https://spring.io/projects/spring-boot): used as an open sourced Javascript framework.
- [**Bootstrap**](https://getbootstrap.com/): used as an open source front-end development framework for building websites and apps.
- [**CSS**](https://www.w3schools.com/css/): used as a style sheet language for describing the presentation of a document written in a markup language.
- [**Vue**](https://vuejs.org/): used as a progressive framework for creating user interfaces.

This app also uses a range of Redis core data structures and modules. These include:

- [**Redis Streams**](https://redis.io/docs/latest/develop/): provides real-time transactions
- [**RedisTimeSeries**](https://redis.io/docs/data-types/timeseries/): provides real-time updates on your balance
- [**RediSearch**](https://redis.io/docs/interact/search-and-query/): provides a search for transactions
- [**Sorted Sets**](https://redis.io/commands/ZADD): for the ‘biggest spenders’
- [**Redis hashes**](https://redis.io/topics/data-types): provides session storage

## 3. Architecture

![RedisBank Architecture For Launchpad Post](/images/blog/883fe89499c8edae6d00229aabc4b6d9bead8a87-1024x544.webp)

This is a SpringBoot application that consists of APIs and a front end.

- The basis of everything is the transaction generator which generates all of the bank transactions. Please note that this is just a component to generate test data. In a real world scenario, we would expect the data to be populated from elsewhere (outside of the app).
- For every bank transaction that’s being made, the data is put on RedisStreams. The stream is then picked up by the transaction forwarder.
- The transaction forwarder takes the transaction information from RedisStreams and puts it on a WebSocket connection that can be consumed by the Web UI. These transactions are also being used to populate a secondary index using RedisSearch and that exposes the search API.
- The bank balance resulting in the bank transaction is also put into RedisTimeSeries data structure which is being exposed by the balance API.
- All accumulative values of all bank transactions are placed in a sorted set so that the biggest spenders API can be returned.

## 4. Getting Started

#### Prerequisites

1. [JDK 11 or higher](https://openjdk.java.net/install/index.html)
1. [Docker Desktop](https://www.docker.com/products/docker-desktop)
1. [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
1. [Azure Spring Cloud extension for the Azure CLI](https://docs.microsoft.com/en-us/cli/azure/spring-cloud?view=azure-cli-latest)

### Step 1: Clone the Repository

```python
git clone https://github.com/redis-developer/redisbank/

```

### Step 2: Run Redis Stack Docker container locally

```python
docker run -d --name redis-stack -p 6379:6379  redis/redis-stack-server

```

### Step 3: Execute the below CLI to run Spring boot app with Maven

```python
./mvnw clean package spring-boot:run

```

**Results**

```python
[INFO] --- maven-compiler-plugin:3.8.1:testCompile (default-testCompile) @ redisbank ---
[INFO] Changes detected - recompiling the module!
[INFO] Compiling 2 source files to /Users/ajeetraina/projects/redisbank/target/test-classes
[INFO] 
[INFO] <<< spring-boot-maven-plugin:2.4.5:run (default-cli) < test-compile @ redisbank <<<
[INFO] 
[INFO] 
[INFO] --- spring-boot-maven-plugin:2.4.5:run (default-cli) @ redisbank ---
[INFO] Attaching agents: []

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/
 :: Spring Boot ::                (v2.4.5)

```

## 5. Accessing the Application

Navigate to [http://localhost:8080](http://localhost:8080/) and login using the following credentials:

- **Username:** <enter your username>
- **Password:** <enter your password>

Please refer to [this](https://github.com/redis-developer/redisbank/blob/main/src/test/java/com/redislabs/demos/redisbank/FakeIBanUtilTest.java) file for the credentials as these values are hard-coded for demonstration purpose.

Below is a screenshot of what the login page should look like.

Once you log in, you’ll land on the main portal page (see below).

From here, you’ll be able to get a tighter grip on your finances through a number of different portal features. These include:

- **Real-time transaction updates: **Redis’ low latency ensures that all transactions are updated in real-time to provide you with the latest information about your finances.
- **Graph illustrations of bank balance: **allows users to get a clear visualization of their financial situation.
- **Purchase history: **allows users to monitor spending history in granular detail.
- **Search highlights: **allows users to pick out specific search terms from the database.

## 6. How it works

[Redis Stream](https://redis.io/docs/manual/data-types/streams/)s is an append-only log. The data generation app will put transactions on the Stream and the application will subscribe to this Stream and will consume any income transactions and send them to the frontend over a Websocket connection.

- Add a new class called BankTransactionForwader to the application that implements the InitializingBean, DisposableBean and StreamListener<String, MapRecord<String, String, String>> interfaces. Make sure to give it an @Component annotation so Spring will pick it up and autowire the dependencies.

The first two interfaces allow you to implement the afterPropertiesSet()method and the destroy()method which you’ll use for the setup and cleanup of your subscription to the Redis Stream.

The third one makes you implement the nMessage(MapRecord<String,String, String> message) which is the callback that will be executed whenever a new bank transaction comes in via the Redis Stream.

- Add three parameters to the method signature (which will be autowired) in the constructor of the BankTransactionForwarder: a RedisTemplate, a SimpMessageSendingOperations and a Config object (the Config object is already provided in the application and provides Stomp/Websocket configuration info from the RestController to the frontend). Store them in instance variables.
- In the afterPropertiesSet() method, create a new StreamMessageListenerContainer<String, MapRecord<String, String, String>> object and store it in an instance variable called container.
- To create the StreamMessageListenerContainer, use the following: StreamMessageListenerContainer.create(redis.getConnectionFactory(), StreamMessageListenerContainerOptions.builder().pollTimeout(Duration.ofMillis(1000)).build()).
- In the same method, start the newly created container using container.start()
- In the same method, create a new subscription to the Stream using container.receive(StreamOffset.latest("transactions_user"), this) and store it in an instance variable called subscription
- In the same method, call subscription.await(Duration.ofSeconds(10))to wait until the subscription is active.

At this point you’ll be subscribed to the Redis Stream. Whenever a new message arrives on the Stream, the onMessage(…) method of this class will be called. You’ll still need to carry out this method, so let’s look over how this is done.

- In the onMessage(...) method, call the convertAndSend(config.getStomp().getTransactionsTopic(), message.getValue()) on the SimpMessageSendingOperations that you stored in the constructor.
- In the destroy(...) method, cancel the Subscription and stop the Container using

```python
if (subscription != null) {
    subscription.cancel();
}
 
if (container != null) {
    container.stop();
}

```

Up to now we’ve created a MessageListener and subscribed to Redis Streams of BankTransactions and, for each incoming BankTransaction, forward the BankTransaction to the Stomp/Websocket topic.

Now let’s see how this works in our application. Firstly, run the data generation app in a terminal window. After that one is running, in a separate terminal window, build and run the app:

```python
./mvnw clean package
./mvnw spring-boot-run

```

Both should be running at this point, so navigate to [http://localhost:8080](http://localhost:8080/) and log in using username/password. You should have access to an overview of transactions as well as a few non-optimized areas of the app (we’ll hop onto this shortly).

You should see new transactions appearing approximately every ten seconds. If not, check your source code and see whether you’ve missed any annotations. Now let’s go over how you can add the search feature.

### Adding RediSearch capabilities

- Begin by stopping both the data generation app and the banking app.
- In the TransactionOverviewController class we’ve provided most of the scaffolding for you so you can focus on building in the Redis and Spring Data sections.
- Inside the searchTransactions(@RequestParam("term") String term) method, use RediSearch to search the transactions generated by the data generation app and present them onto the user interface. You can do so by adding the following code:

```python
RediSearchCommands<String, String> commands = srsc.sync();
    SearchOptions options = SearchOptions
            .builder().highlight(Highlight.builder().field("description").field("fromAccountName")
                    .field("transactionType").tag(Tag.builder().open("<mark>").close("</mark>").build()).build())
            .build();
 
    SearchResults<String, String> results = commands.search(SEARCH_INDEX, term, options);

```

**Note**: When adding imports, choose the com.redislabs imports.

The first statement creates a RediSearch connection that uses the RediSearch client library. The second one creates SearchOptions based on your preferences. The third statement executes the search and returns the results.

- Now you’ll need to run the data generation app again and then build and run the banking app. Afterwards, navigate to [http://localhost:8080](http://localhost:8080/) and try out the search.
- Enter the letters onli in the search box and see what happens. You’ll notice that it will select all transactions of Type Online payment and highlight the word Online.
- Now enter the letters paym in the search box and see what happens. You’ll notice that it will select all transactions with the word BMW in the name field.

### Adding the balance over time view

The data generation app also populates a TimeSeries for the bank balance of each account. This is updated every time there’s a new transaction. You can query this TimeSeries and pass the result to the user interface so it can show the balance over time in a visual diagram. Now let’s get started:

- Stop both the data generation app and banking app.
- In the TransactionOverviewController class in the balance(Principal principal) method, add the following:

```python
String balance_ts_key = BALANCE_TS + principal.getName();
Map<String, String> tsValues = tsc.range(balance_ts_key, System.currentTimeMillis() - (1000 * 60 * 60 * 24 * 7),
        System.currentTimeMillis());
Balance[] balanceTs = new Balance[tsValues.size()];
int i = 0;
 
for (Entry<String, String> entry : tsValues.entrySet()) {
    Object keyString = entry.getKey();
    Object valueString = entry.getValue();
    balanceTs[i] = new Balance(keyString, valueString);
    i++;
}
return balanceTs;

```

What you’re essentially doing here is asking for the time series values stored under the key of BALANCE_TS between now and (now -1 week). You’ll then need to copy the results into a Balance array and return it.

You may notice that you’ll be using the Principal name here to suffix the TimeSeries key. This means that if you log in with a different user, it will be a different key.

- Start the data generation app
- Create and run the app. You’ll see that the balance over time is populated. Notice how it updates with each incoming transaction.

**Note:** in this example we didn’t use an additional client library for a reason. Instead, we extended the [Lettuce library](https://lettuce.io/) and provided an interface that we injected. Extending Lettuce is a fantastic way of adding Redis Module functionality into your app whilst limiting the amount of dependencies.

### Adding the ‘biggest spenders’ feature to the app

Adding this feature onto the app will show the biggest deductors from your bank account. Because of this the data-generation app is populating a Sorted Set. For every transaction, it will add the value of the transaction to a member of the sorted set of which the key is the counter-account’s name as well as the total amount of transactions for that account.

- Inside the searchTransactions(@RequestParam("term") String term) method, use RediSearch to discover the transactions generated by the data generation app and present them onto the user interface. You can do this by adding the following code:

```python
String biggestSpendersKey = SORTED_SET_KEY + principal.getName();
Set<TypedTuple<String>> range = redis.opsForZSet().rangeByScoreWithScores(biggestSpendersKey, 0,
        Double.MAX_VALUE);
if (range.size() > 0) {
    BiggestSpenders biggestSpenders = new BiggestSpenders(range.size());
    int i = 0;
    for (TypedTuple<String> typedTuple : range) {
        biggestSpenders.getSeries()[i] = Math.floor(typedTuple.getScore() * 100) / 100;
        biggestSpenders.getLabels()[i] = typedTuple.getValue();
        i++;
    }
    return biggestSpenders;
} else {
    return new BiggestSpenders(0);
}

```

This will retrieve the members of the Sorted Set by their score from 0 up to Double.MAX_VALUE. You’ll then put the result in a BiggestSpenders object.

- Run the data generation app.
- Build and run the app, and watch in awe as the biggest spenders are now shown in the app!

You should now be running, so navigate to [http://localhost:8080](http://localhost:8080/) and log in using username/password. At this point you’ll now see an overview of transactions.

### What’s Happening in Redis?

**Redis Streams**

The data generation app generates a bank transaction every 10 seconds or so and puts it in a Stream. You can query the stream using:

```python
xread count 10000 streams transactions_user 0-0

```

This will provide all of the entries on the transactions_username Stream. Remember that your app subscribed to this Stream via Spring Data, so every time a new element is added to the Stream it will be processed by the app and sent to the user interface.

**Sorted Set**

The data generation app also adds every transaction to a Sorted Set. This will add the transaction amount to the score, adding up the totalled transaction amount per account name and storing it in a sorted set. You’ll then be able to identify the biggest spenders by simply querying the Sorted Set like this:

```python
zrangebyscore bigspenders_username 0 10000 withscores

```

**TimeSeries**

The data generation app also adds the bank accounts balance to a TimeSeries every time there is a new transaction being generated. This allows you to view the balance over time by using a query such as:

```python
ts.range balance_ts_username 1623000000000 1653230682038 (use appropriate timestamps or it will return an empty array)

```

**Hashes**

Each transaction is stored as a Hash in Redis so it can be indexed by RediSearch. You’ll be able to search for each transaction just like in the example below:

```python
ft.search transaction_description_idx Fuel
ft.search transaction_description_idx Fuel highlight
ft.search transaction_description_idx Fuel highlight tags <mytag> </mytag>

```

**Session Data**

Session data is also stored in Redis. This requires no code from your end whatsoever – adding the dependencies is enough.

## 7. How to run the application on Azure Spring Cloud

1. Follow the steps from ‘Running locally’
1. Make sure you’re logged into the Azure CLI
1. Add the Azure Spring Cloud extension to the Azure CLI az extension add –name spring-cloud. If you already have the extension then make sure it’s up to date by using az extension update --name spring-cloud.
1. Create an Azure Spring Cloud instance using az spring-cloud create -n acrebank -g rdsLroACRE -l northeurope (this may take a few minutes).
1. Create an App in the newly created Azure Spring Cloud instance using az spring-cloud app create -n acrebankapp -s acrebank -g rdsLroACRE --assign-endpoint true --runtime-version Java_11
1. Modify the application properties so it points to your newly created ACRE instance by using the code below:

```python
spring.redis.host=your ACRE hostname
spring.redis.port=your ACRE port (default: 10000)
spring.redis.password= your ACRE access key

```

1. Modify the application properties so the WebSocket config will point to the Azure Spring Cloud app instance endpoint that was created in step 3.

```python
stomp.host=your ASC app endpoint URL (Default: <appname>-<service-name>.azuremicroservices.io)
stomp.port=443
stomp.protocol=wss

```

1. Rebuild the app using ./mvnw package
1. Deploy the app to Azure Spring Cloud by using the code below:

```python
az spring-cloud app deploy -n acrebankapp -s acrebank -g rdsLroAcre --jar-path target/redisbank-0.0.1-SNAPSHOT.jar

```

## 

## 8. Troubleshooting tips on Azure Spring Cloud

Use the below code to get the application logins:

```
az spring-cloud app logs -n acrebankapp -g rdsLroAcre -s acrebank

```

**Note:** The project is compiled with JDK11 since it’s the max LTS version that’s supported by Azure Spring Cloud. The project will also be able to run locally or on other platforms up to JDK16.

## 9. Known issues

Below are some known issues that you may come across:

1. **Thread safety:** Data is generated off a single stream of transactions, which means it’s the same for all users. It’s not a problem with the current iteration.
1. **Hard-coded values.** Code users have hardcoded values throughout the code. These need to be replaced with proper variables.

## Conclusion: Giving users easy, accurate, and real-time mobile banking with Redis.

Mobile banking is the new norm and it has to be fast, easy, and accurate for it to be effective. The digital era has made us all accustomed to seamless digital interactions that are updated in real-time, and failing to meet these expectations will create a sub-optimal application that’s destined for the rocks.

But through its advanced capabilities and low latency, Redis is able to guarantee real-time data transmission, eliminating the likelihood of any lags from occurring. From just a few taps on their mobile device, users can access their banking information and gain a holistic and accurate view of their finances.

To gain a more visual insight into how this application was created, make sure you check out Lars’s [YouTube video here](https://www.youtube.com/watch?v=JEruQaQ9XpU).

And if you’ve enjoyed this post, make sure to visit the [Redis Launchpad](https://launchpad.redis.com/) where you’ll have access to a whole variety of different applications that are making an impact on everyday lives.

Check it out. Be inspired. And join in the Redis fun!

[Watch the video](https://launchpad.redis.com/)

## Who built this app?

### Lars Rosenquist

![Author Image of RedisBank](/images/blog/78f885acc99af0fb841a670011efc3d3bbaf5a3f-460x460.webp)

Lars has a broad range of experience in the software industry but currently works as a solution architect manager to help others reach the best of their abilities. Make sure to follow his [GitHub page](https://github.com/NLxAROSA) to stay up to date with all of his projects.
