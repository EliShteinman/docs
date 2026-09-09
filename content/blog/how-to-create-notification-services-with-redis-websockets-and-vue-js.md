---
title: "How to Create Notification Services with Redis, Websockets, and Vue.js"
linkTitle: "How to Create Notification Services with Redis, Websockets, and Vue.js"
url: "/blog/how-to-create-notification-services-with-redis-websockets-and-vue-js/"
description: "It is very common to get real-time notifications when navigating in a web application. Notifications could come from a chat bot, an alerting system, or be triggered by an event that the app pushes..."
date: 2020-08-19
blogCategories:
- "Tech"
authors:
- "Tugdual Grall"
lastmod: 2026-09-01
hidden: true
---

*By Tugdual Grall, Technical Marketing Manager · Published 19 August 2020 · updated 1 September 2026*

![Blog tile image](/images/blog/953736d7c55dcbcf9451f6485ce4b21353c2fde1-527x462.webp)

It is very common to get [real-time notifications](/docs/really-know-redis/) when navigating in a web application. Notifications could come from a chat bot, an alerting system, or be triggered by an event that the app pushes to one or more users. Whatever the source of the notifications, developers are increasingly using Redis to create notification services.

In modern applications powered by a microservices architecture, Redis is often used as a simple cache and as a primary database. But it is also used as a communication layer between services using a persistent [messaging layer](/solutions/messaging/) powered by [Redis Streams,](/docs/getting-started-redis-streams/) a lightweight eventing system using its well-known [Pub/Sub](/glossary/pub-sub/) (Publish/Subscribe) commands.

In this blog post, we’ll show you how easy it is to create a small notification service using Redis Pub/Sub to send messages to a web application, developed with [Vue.js](https://vuejs.org/), [Node.js](https://nodejs.org/), and WebSockets.

[Watch the video](https://www.youtube.com/watch?v=Rs31Qvnuv5A&feature=youtu.be)

**Prerequisites**

This demo service uses:

- [Docker](https://www.docker.com/)
- [Redis 5.0.x or later](/downloads/) (this demo uses the Redis Docker container)
- [Node.js](https://nodejs.org/) 10.x with Node package manager (npm)
- [nodemon](https://www.npmjs.com/package/nodemon), a simple tool that automatically restarts your application during development
- [Vue CLI](https://cli.vuejs.org/)

### Starting Redis server

If you do not have already a Redis instance running, you can start it using Docker; in a terminal, run this command:

> docker run -it --rm --name redis-server -p 6379:6379 redis

Redis should now be up and running and ready to accept connections.

## Creating the WebSocket server with Node.js

To configure the project with the proper structure, open a terminal and enter the following commands:

```python
> mkdir notifications

> cd notifications

> mkdir notif-server

> cd notif-server

```

Create a new Node.js project using npm *(the -y parameter will set all values to the default one)*:

```python
> npm init -y

> npm install ws redis

```

The final command above adds the [WebSocket](https://www.npmjs.com/package/ws) and [Redis](https://www.npmjs.com/package/redis) dependencies to your project. You are now ready to write some code!

**Writing the WebSocket server**

Open your favorite code editor for Node.js (I use [Visual Studio Code](https://code.visualstudio.com/)) and simply enter the code “code .” to open the current directory. In your editor, create a new file called server.js.

```python
const WebSocket = require('ws');
const redis = require('redis');

// Configuration: adapt to your environment
const REDIS_SERVER = "redis://localhost:6379";
const WEB_SOCKET_PORT = 3000;

// Connect to Redis and subscribe to "app:notifications" channel
var redisClient = redis.createClient(REDIS_SERVER);
redisClient.subscribe('app:notifications');

// Create & Start the WebSocket server
const server = new WebSocket.Server({ port : WEB_SOCKET_PORT });

// Register event for client connection
server.on('connection', function connection(ws) {

  // broadcast on web socket when receving a Redis PUB/SUB Event
  redisClient.on('message', function(channel, message){
    console.log(message);
    ws.send(message);
  })

});

```

This simple Node.js program is limited to the demonstration and focuses on:

- Connecting to Redis (line 9)
- Subscribing to the messages from the “app:notifications” channel (line 10)
- Starting a WebSocket server (line 13)
- Registering user client connections (line 16)
- Listening to Redis subscribe events (line 19)
- And sending the message to all WebSocket clients (21).

Lines 5 and 6 are simply used to configure the Redis server location and the port to use for the Web Socket server. As you can see it is pretty simple.

**Running the WebSocket server**

If you have not yet installed nodemon, install it now. Then start the WebSocket server using the following command:

```python
> nodemon server.js

```

Let’s now create the frontend that will receive the notifications and print them to the user.

## Creating the frontend with Vue.js

Open a new terminal and run the following command from the notifications directory:

If you have not already installed the Vue CLI tool already, do so now using the command npm install -g @vue/cli.

```python
> vue create webclient

> cd web-client

```

This command creates a new Vue project that is ready to be executed and extended.

One last package to install for this demonstration is [BootstrapVue](https://bootstrap-vue.org/), which makes it easy to use the CSS library and components from the popular [Bootstrap](https://getbootstrap.com/) framework.

```python
> npm install bootstrap-vue bootstrap

```

Open the web-client directory in your favorite code editor, then start the newly created Vue application:

```python
> npm run serve

```

The last command starts the Vue development server that will serve the pages and also automatically reloads the pages when you change them.

Open your browser, and go to [http://localhost:8080](http://localhost:8080); where you should see the default Vue welcome page:

![](/images/blog/49637533a10f594c68a4e68e430ceb5b207e0e6e-1016x788.webp)

**Adding WebSocket to the frontend**

The Vue framework is quite simple, and for this post we will keep the code as simple as possible. So let’s quickly look at the directory structure:

```javascript
├── README.md
├── babel.config.js
├── node_modules
├── package-lock.json
├── package.json
├── public
│   ├── favicon.ico
│   └── index.html
└── src
    ├── App.vue
    ├── assets
    │   └── logo.png
    ├── components
    │   └── HelloWorld.vue
    └── main.js
```

The files at the root level (babel.config.js, package.json, package-lock.json, node_modules) are used to configure the project. The most interesting part, at least for now, is located in the src directory:

- The main.js file is the main JavaScript file of the application, which will load all common elements and call the App.vue main screen. We will modify it later to add Bootstrap support.
- The App.vue is a file that contains in the HTML, CSS, and JavaScript for a specific page or template. As an entry point for the application, this part is shared by all screens by default, so it is a good place to write the notification-client piece in this file.

The public/index.html is the static entry point from where the DOM will be loaded. If you look at it you will see a <div id=”app”>, which is used to load the Vue application.

This demonstration is quite simple, and you will have to modify only two files: the App.vue and main.js files. In a real-life application, you would probably create a Vue.js component that would be reused in various places.

**Updating the App.vue file to show WebSocket messages**

Open the App.vue file in your editor and add the information listed below. At the bottom of the page, just before the </div> tag, add the following HTML block:

```python
<hr/>
<h3>
  {{message}}
</h3>
<hr/>

```

Using {{message}} notation, you are indicating to Vue to print the content of the message variable, which you will define in the next block.

In the <script>, replace the content with:

```python
<script>
import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'App',
  data() {
    return {
      message: "",
    }
  },
  created(){
    try {
      const ws = new WebSocket("ws://localhost:3000/");
      ws.onmessage = ({data}) => {
        this.message =  data;
        console.log(this.message);
      }
    } catch(err) {
      console.log(err);
    }
  },
  components: {
    HelloWorld
  }
}
</script>

```

These few lines of code are used to:

- Connect to the WebSocket server (line 13)
- Consume messages from the server and send them the local message variable (lines 13-17)

If you look carefully at what has been changed, you can see that you have added:

- A data() function that indicates to the Vue component that you are defining local variables that can be bound to the screen itself (lines 6-10)
- A created() function that is called by the Vue component automatically when it is initialized

**Sending messages from Redis to your Vue application**

The WebSocket server and the Vue frontend should now be running and connected thanks to the few lines of JavaScript you added. It’s time to test it!

Using the Redis CLI or RedisInsight, publish some messages to the app:notifications channel. For example, if you started Redis using Docker, you can connect to it using the following command and start publishing messages:

```python
> docker exec -it redis-server redis-cli

127.0.0.1:6379> PUBLISH app:notifications  "message from Redis2"

```

You should see the message appear at the bottom of the application in your browser:

![](/images/blog/d83a017f23bb380cbc40295b3f91967dc39adc49-733x1024.webp)

As you can see, it is pretty easy to push content to your web frontend in real time using WebSocket. So now lets improve the design and add a more user-friendly interface using Bootstrap.

**Creating an alert block with Bootstrap**

In this section, we’ll show you how to use a[ Bootstrap alert component](https://bootstrap-vue.org/docs/components/alert/), which appears when a new message is received and disappears automatically after a few seconds, using a simple countdown.

**Main.js file**

Open the main.js file and add the following lines after the last import:

```python
import { BootstrapVue } from 'bootstrap-vue';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

Vue.use(BootstrapVue);

```

These four lines import and register the Bootstrap components in your Vue application.

**App.js file**

In the App.vue file, replace the code you added earlier (everything between the two <hr/> tags and the tags themselves) with the following:

```python
<div class="d-inline-flex p-4">
   <b-alert id="notification" 
      :show="dismissCountDown"
      dismissible
      @dismissed="dismissCountDown=0"
      @dismiss-count-down="countDownChanged"
    >
    New notification: {{message}}
   </b-alert>
</div>

```

This component uses several attributes:

- id=”notification” is the element id used to reference the element in JavaScript or CSS code:show=”dismissCountDown” indicates that the component is visible only when the dismissCountDown variable is not null nor 0
- dismissible adds a small icon in the alert to let the user manually close it
- @dismissed=”dismissCountDown=0″ shows that the alert box will be closed then the value dismissCountDown equals 0
- @dismiss-count-down=”countDownChanged” is the countdown method

Let’s add a few lines of JavaScript to define the variables and methods used by the alert component:

```python
data() {
    return {
      message: "",
      dismissSecs: 5,
      dismissCountDown: 0,      
    }
  },
  created(){
    try {
      const ws = new WebSocket("ws://localhost:3000/");
      ws.onmessage = ({data}) => {
        this.message =  data;
        this.showAlert();
      }
    } catch(err) {
      console.log(err);
    }
  },
  methods: {
    countDownChanged(dismissCountDown) {
      this.dismissCountDown = dismissCountDown
    },
    showAlert() {
      this.dismissCountDown = this.dismissSecs
    }
  },

...

```

In this section you have:

- Added the dismissSecs and dismissCountDown and variables to the data() method (lines 4-5) that are used to control the timer that shows the alert before hiding it again
- Created methods to show and hide the alert component (line 10-26)
- Called the showAlert() method when a new message is received (line 13)

Let’s try it!

Go back to redis-cli or Redis Insight and post new messages to the app:notifications channel.

![](/images/blog/953736d7c55dcbcf9451f6485ce4b21353c2fde1-527x462.webp)

As you can see, it is easy to use Redis to create a powerful notification service for your application. This sample is pretty basic, using a single channel and server and broadcasting to all the clients.

The goal was really to provide an easy way to start with WebSocket and Redis Pub/Sub to push messages from Redis to a web application. There are many options to deliver messages to specific clients using various channels, and to scale and secure the application.

You can also use the WebSocket server in the other direction, to consume messages as well as to push messages to clients. But that’s a big topic for another blog post. In fact, stay tuned for more blog posts on how you can use [Redis Gears](/redis-enterprise/technology/gears/) to easily capture events directly in the Redis database and push some events to various clients.

For more information, see these resources:

- [Redis Microservices for Dummies ](/docs/redis-microservices-for-dummies/)(free ebook)
- [Introduction to Redis Streams](https://redis.io/docs/latest/develop/) (Redis documentation)
- [Redis Pub/Sub](https://redis.io/topics/pubsub) (Redis documentation)
- Take a free online course at [Redis University](https://university.redis.com/)
- Check out [Redis Enterprise Cloud](/redis-enterprise-cloud/)
