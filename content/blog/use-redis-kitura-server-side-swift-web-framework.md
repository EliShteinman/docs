---
title: "How to Use Redis with Kitura, a Server-Side Swift Web Framework"
linkTitle: "How to Use Redis with Kitura, a Server-Side Swift Web Framework"
url: "/blog/use-redis-kitura-server-side-swift-web-framework/"
description: "During a recent project, I needed to develop application services using varied technology stacks. One of my requirements was to pick a different programming language for each microservice in my..."
date: 2019-03-28
blogCategories:
- "How To and Tutorials"
authors:
- "Shabih Syed"
lastmod: 2025-03-27
hidden: true
---

*By Shabih Syed, Shabih is a Sr. Director of Product Marketing at Redis Labs. He has 13+ years of experience with software development, product management and marketing of cloud-based data management & application integration platforms. Most recently he led product marketing at Liaison Technologies (now OpenText) and has worked for HP and IBM before that. Shabih is based out of NYC. · Published 28 March 2019 · updated 27 March 2025*

![Blog tile image](/images/blog/8eed7b3a6cd0dccd9052b8700ea39770c39b18f1-200x200.webp)

During a recent project, I needed to develop application services using varied technology stacks. One of my requirements was to pick a different programming language for each microservice in my application. While Java, Node and Python were easy choices, I wanted to try something new and obscure. During a conversation with my brother, who happens to be an active iOS developer, I learned for the first time about Swift and Kitura and decided to give it a try.

Whenever I am experimenting with a new language, I try to use it with a database. In this example, I will show how easy it is to use Redis as a data store for Swift-based microservices.

I’ll begin with a brief description of my technology stack, and then walk you through the steps to build an application with these tools:

Swift is a general purpose, multi-paradigm, compiled programming language developed by Apple Inc. for iOS, macOS, watchOS, tvOS, Linux and z/OS.

Kitura is a free open source web framework written in Swift, developed by IBM and licensed under Apache 2.0. It’s an HTTP server and web framework for writing Swift server applications.

Redis is an open source (BSD licensed), in-memory data structure store, used as a database, cache and message broker. With almost 1.5 billion docker pulls, it is one of the most popular NoSQL databases.

### Step 1: Installing Swift

First, download and install the latest version of Xcode from the App Store.

Next, check if Swift is installed. In the terminal, type the ‘swift’ command and pass the ‘–version’ flag:
swift --version

Apple Swift version 4.2.1 (swiftlang-1000.0.42 clang-1000.10.45.1)

Target: x86_64-apple-darwin17.7.0

If Swift is not installed, then run the following –install command:

xcode-select --install

### Step 2: Installing Kitura

Installing the Kitura web server is pretty easy as well.

1. Create a new directory to host your project.
mkdir MyKituraApp && cd MyKituraApp

2. Initialize the new directory as a Swift project.
swift package init --type executable

Creating executable package: MyKituraApp

Creating Package.swift

Creating README.md

Creating .gitignore

Creating Sources/

Creating Sources/MyKituraApp/main.swift

Creating Tests/

Creating Tests/LinuxMain.swift

Creating Tests/MyKituraAppTests/

Creating Tests/MyKituraAppTests/MyKituraAppTests.swift

Creating Tests/MyKituraAppTests/XCTestManifests.swift

![](/images/blog/784525697edf8d075896a65f6fb9f1b41d0ec52e-1024x151.webp)

3. To add Kitura to your dependencies, edit `Package.swift`.
Open `Package.swift` and edit it so it has the following text:

```javascript
// swift-tools-version:4.2

import PackageDescription

let package = Package(
    name: "MyKituraApp",
    dependencies: [
        .package(url: "https://github.com/IBM-Swift/Kitura", from: "2.6.0")
    ],
    targets: [
        .target(
            name: "MyKituraApp",
            dependencies: ["Kitura"]),
        .testTarget(
            name: "MyKituraAppTests",
            dependencies: ["MyKituraApp"]),
    ]
)
```

4. Build the project to pull down your new dependency:
swift build

Go under the sources folder and edit `main.swift` so it has the following text, which will initiate the Kitura web-server.

```javascript
import Kitura

let router = Router()
Kitura.addHTTPServer(onPort: 8080, with: router)
Kitura.run()
```

5. Since we’ve added code to `main.swift`, you’ll need to recompile the project:
swift build

6. Now you are ready to run your Swift app.
swift run

7. Navigate to http://localhost:8080 in your browser, and it will return the following:

![](/images/blog/d5494af136f09061a26ca4b164978a5caafd0830-1024x543.webp)

### Step 3: Get Redis

I use Redis Cloud, a fully managed Redis database-as-a-service in this example. Creating a Redis instance with Redis Cloud is easy and free, and there are other options available as well (feel free to explore them in [Get Started with Redis](/get-started-with-redis/)).

1. Visit the Redis [Get Started](/try-free/) page, and click SIGN UP under the “Cloud Hosted” section. You will land at the following page:

![](/images/blog/e8f4355a4097dfa1799f76b145c376383877274a-1024x814.webp)

2. Login to create your subscription and select a free (30MB) Redis database.

![](/images/blog/a637d7741a52d3fa6a1056012604682b64cd58c4-1024x933.webp)

3. Name your database and activate it.

![](/images/blog/acf93fb38fd498389dcd97818bd29c1d20acbb3f-1024x540.webp)


4. Take note of your database endpoint and password.

![](/images/blog/9e7ed64baa902698f704675e6d50f44948c71d53-1024x822.webp)

In this example, redis-15878.c91.us-east-1-3.ec2.cloud.redis.com is the URL of your Redis database and 15878 is the port.

### Step 4: Connecting with Redis using the Kitura-Redis client

[Kitura-Redis](https://github.com/IBM-Swift/Kitura-redis) is a pure Swift client for interacting with a Redis database.

1. To add Kitura-Redis to your dependencies, you’ll need to edit `Package.swift` again.
Open `Package.swift` and edit it so it now has the following text:

```javascript
// swift-tools-version:4.2

import PackageDescription

let package = Package(
    name: "MyKituraApp",
    dependencies: [
        .package(url: "https://github.com/IBM-Swift/Kitura", from: "2.6.0"),
        .package(url: "https://github.com/IBM-Swift/Kitura-redis.git", from: "2.1.0")
    ],
    targets: [
        .target(
            name: "MyKituraApp",
            dependencies: ["Kitura","SwiftRedis"]),
        .testTarget(
            name: "MyKituraAppTests",
            dependencies: ["MyKituraApp"]),
    ]
)
```

2. Now you’ll use **Kitura-Redis** to establish a connection with your Redis database* in the cloud and set a key called “Redis” with a value “On Swift”.

This is a simple example, but you can, of course, use Redis in more complex ways.

Go under your sources folder and edit `main.swift` so it has the following text:

* Make sure to update , and with your Redis Cloud database configuration.

```javascript
import Kitura
import Foundation
import SwiftRedis

let router = Router()
Kitura.addHTTPServer(onPort: 8080, with: router)

let redis = Redis()

//Establish connection with Redis

redis.connect(host: "", port: ) { (redisError: NSError?) in

   //Check for if host and port are incorrect
    if let error = redisError {
        print(error)
    }

    //If connection to Redis successful then pass in the password

    else {

        let password = ""
	    redis.auth(password) { (pwdError: NSError?) in
	    	if let errorPwd = pwdError {
	        	print(errorPwd)
	    	}
	    	else {
	    		print("Password Authentication Is Successful")
	    	}
	    }

        print("Established Connection to Redis")

        // Set a key
        redis.set("Redis", value: "on Swift") { (result: Bool, redisError: NSError?) in
            if let error = redisError {
                print(error)
            }
            // Get the same key
            redis.get("Redis") { (string: RedisString?, redisError: NSError?) in
                if let error = redisError {
                    print(error)
                }
                else if let string = string?.asString {
                    print("Redis (string)")
                }
            }
        }
    }
}
Kitura.run()
```

3. Since you’ve added code to `main.swift`, you’ll need to recompile the project:
swift build

4. Now you are ready to run your Swift app and will see the following:
swift run

Redis Password Authenticated
Connected to Redis
Redis on Swift

5. Using [Redis CLI](/blog/get-redis-cli-without-installing-redis-server/), you can check if the key value you set in ‘main.swift’ is successful.
redis-15878.c91.us-east-1-3.ec2.cloud.redis.com:15878> Keys *

1) Redis

redis-15878.c91.us-east-1-3.ec2.cloud.redis.com:15878> GET Redis

on Swift

For more information, visit the following pages:

[Swift](https://swift.org/)
[Kitura](https://www.kitura.io/)
[IBM Swift/Kitura](https://github.com/IBM-Swift/Kitura)
[IBM Swift/Kitura-Redis](https://github.com/IBM-Swift/Kitura-redis)

**Happy Swifting with Redis!**
