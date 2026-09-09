---
title: "How to Eliminate Waste and Promote a Greener Planet Using Redis"
linkTitle: "How to Eliminate Waste and Promote a Greener Planet Using Redis"
url: "/blog/how-to-eliminate-waste-and-promote-a-greener-planet-using-redis/"
description: "What generates 300 million tons of solid waste within a year? American consumers. Of this amount, only half goes straight into landfills to be stored. When one is at overcapacity, it’s sealed off..."
date: 2022-01-18
blogCategories:
- "How To and Tutorials"
- "Tech"
authors:
- "Growth Team"
lastmod: 2025-03-27
hidden: true
---

*By Growth Team · Published 18 January 2022 · updated 27 March 2025*

![Blog tile image](/images/blog/6e0436f7942cb6c143053295f67f2ac4fde8f31e-772x550.webp)

What generates 300 million tons of solid waste within a year? American consumers. Of this amount, only half goes straight into landfills to be stored. When one is at overcapacity, it’s sealed off to prevent leakage. Meanwhile, deep beneath the surface, the trash continues to decompose, creating many toxic byproducts such as leachate, which is contaminated water. Carbon monoxide is also produced, contributing to rising CO2 levels in our air.

What’s just as harrowing is that *50%* of this landfill trash is compostable, reusable, and recyclable. Recognizing that this is completely avoidable, [Rajesh Ramamurthy](https://github.com/rajkram) has created an exceptional application, [GreenEarth](https://www.youtube.com/watch?v=4SEACl3E3vY), that can reduce waste and promote a greener planet. The application creates a platform where people from all over the world can find projects that utilize common household trash to repurpose them into useful items or creative art projects.

Redis was used to retrieve user information from the cloud database and for storing individual user attributes with hyper-efficiency. This was critical to Greener Earth’s functionality since data processing needs to be performed at speed to maximize the user’s experience.

Let’s take a look at how [Rajesh ](https://github.com/rajkram)brought this innovative application to life. But before we dive in, we’d like to point out that we have 29 other exciting apps that are improving everyday lives on the [Redis Launchpad](https://launchpad.redis.com/). So make sure to have a browse after reading this post.

[Click here to view video](https://www.youtube.com/embed/iK2IeM9xI4g)

1. What will you build?
1. What will you need?
1. Architecture
1. Getting started
1. Setting up the features
1. How it works

## 1. What will you build?

An app. A community and a platform for people to help save the planet. This application connects environmentally conscious people with projects that utilize household items. If, for example, a user wants to make use of their empty tin cans, Green Earth will connect them with projects that demonstrate how these items can be used to create useful household items.

Below we’ll show you exactly how to build this application by going through each step in chronological order. We’ll also highlight what components you’ll need, along with their functionality.

![GreenEarth website with a description of how to repurpose tin cans into flower pots, pencil holders, even tumblers. ](/images/blog/1e9cacc12a0479b4a0bc826e04900105ee285fae-1240x648.webp)

## 2. What will you need?

- [JavaScript](https://en.wikipedia.org/wiki/JavaScript)
- [Redis Enterprise Cloud](/redis-enterprise-cloud/overview/)
- [RedisJSON module enabled](/json/)

## 3. Architecture

![Image showing the architecture of building an app with Redis.](/images/blog/0bb9e44e2f0c859fccdb10f53a300e1d491a98bf-1024x301.webp)

## 4. Getting started

- Install NPM
- Setup Redis Enterprise Cloud Database with RedisJSON module enabled

## Install NPM

```javascript
brew install npm
```

## Setting up Redis Enterprise Cloud Database

Create your free [Redis Enterprise Cloud account](/try-free/). Once you click on “Get Started”, you will receive an email with a link to activate your account and complete your signup process.

[Follow this link](https://redis.io/docs/data-types/json/) to enable RedisJSON module under Redis Enterprise Cloud database.

## Clone the repository

```javascript
git clone https://github.com/redis-developer/greenearth
```

## Install NPM dependencies

Change directory to greenearth directory and install the required dependencies:

```javascript
npm install
```

## Configure the index.js

To connect to Redis Enterprise Cloud Database with RedisJSON enabled, you’ll need to edit the following code in index.js.

```
const client = redis.createClient({
     port      : // database port,
     host      : // database url,  
     password  : // database password
});

```

## Start the application

You’ll also have to run npm start to start the local server at http://localhost:3000.

```javascript
npm start
```

## 5. Setting up the features

Below there are a number of features that need to be set up for the application to function. Let’s take a look at what needs to be done.

**Users**

- **Signup**

Creates user account.

SADD – Adds username to global users set

HMSET – Creates user object with information including hashed password, description, and profile picture

- **Login**

Allows users to log in to an existing account.

```
async function login(name, password) {
	if (client.sismember(['users', name])) {
		const hash = crypto.createHash('sha256');
		hash.update(password);
		var pwdhash = hash.digest('hex');
		const hget = promisify(client.hget).bind(client);
		var pwd = await hget([name, 'pwd']);

		if (pwdhash === pwd) {
			console.log("Successful sign-in");
			var token = uuidv4();
			const hset = promisify(client.hset).bind(client);
			await hset(['active', token, name]);
			return token;
		} else {
			console.log("Incorrect password");
			return null;
		}
	} else {
		console.log("Account does not exist");
		return null;
	}
}


```

SISMEMBER – Checks whether if the entered username is a valid member

HGET – Validates the entered password by retrieving the registered one and comparing them

HSET – Adds username with generated session token to active user group br>

- **Logout**

Logs out of the signed in account.

```
async function logout(token) {
var name = await authUser(token);
	console.log(token);
	console.log(name);
	if (name == null) {
		console.log("Not signed in");
	} else {
		const hdel = promisify(client.hdel).bind(client);
		await hdel(['active', token]);
		console.log("Successful logout");
	}
}

```

HGET – Retrieves user from the provided session token

HDEL – Removes the user and session token from the active user group

- **UserInfo**

Retrieves information (username, description, profile picture) of the specified user.

```
app.get('/userInfo', async (req, res) => {
  var name = req.query.name;
  const hmget = promisify(client.hmget).bind(client);
  var user = await hmget(name, 'id', 'description', 'image');
  res.send([name, ...user]);
})

```

HMGET – Retrieves user data from provided attributes

- **SetField**

Sets specific attributes (description, profile picture) of specified user.

```
async function setField(token, field, value) {
var name = await authUser(token);
	const hmset = promisify(client.hmset).bind(client);
	await hmset(name, field, value);

}


```

HMSET – Sets user attributes with provided data

### Posts

- **AddPost**

Adds a post from provided user information.

```
app.get('/allPosts', async (req, res) => {
	var name = req.query.name;
	const hget = promisify(client.hget).bind(client);
	const lr = promisify(client.lrange).bind(client);
	const hgetall = promisify(client.hgetall).bind(client);

	const json_get = promisify(client.json_get).bind(client);

	var id = await hget([name, 'id']);
	var posts = await json_get(id);
	posts = JSON.parse(posts);
	var newposts = {"posts": []};
	if (posts != null) {
		for (var i = 0; i < posts.length; i++) {
			var p = posts[i];

			if (p["visibility"] === "on") {
				newposts["posts"].push(p);
			}
		}
	}
	console.log(newposts);
	res.send(newposts);

})

```

HGET – Retrieves user post list ID

JSON.SET – Creates a post from the provided information and adds to the user post list

JSON.GET – Retrieves user post list

- **EditPost**

Edits the existing post that’s created by the user.

```
async function editPost(token, pid, title, description, image, recipe, steps, visibility) {
	var name = await authUser(token);
	const hget = promisify(client.hget).bind(client);
	const json_get = promisify(client.json_get).bind(client);
	const json_set = promisify(client.json_set).bind(client);
	var id = await hget([name, 'id']);

	var posts = await json_get(id, ".");
	var globalPosts = await json_get('globalPosts', ".");
	posts = JSON.parse(posts);
	globalPosts = JSON.parse(globalPosts);
	console.log(posts);

	const newpost = {
	  pid: pid,
	  title: title,
	  description: description,
	  author: "",
	  image: image,
	  recipe: recipe,
	  steps: steps,
	  comments: [],
	  visibility: visibility
	}
	var vis;

	if (posts != null) {
		for (var i = 0; i < posts.length; i++) {
			if (posts[i]["pid"] === pid) {
				vis = posts[i]["visibility"];
				newpost.author = posts[i]["author"];
				newpost.comments = posts[i]["comments"];
				posts[i] = newpost;

				break;
			}
}
	}
	if (vis === "on") {
		if (globalPosts != null) {
			for (var i = 0; i < globalPosts.length; i++) {
				if (globalPosts[i]["pid"] === pid) {
					globalPosts[i] = newpost;
					if (visibility === "off") {
						globalPosts.splice(i, 1);
					} else if (visibility === "on") {
						globalPosts[i] = newpost;
					}
					break;
				}
			}
		}
	} else {
		if (visibility === "on") {
			globalPosts.push(newpost);
		}
	}
	await json_set(id, '.', JSON.stringify(posts));
	await json_set('globalPosts', '.', JSON.stringify(globalPosts));
	console.log("Post edited");
}

```

HGET – Retrieves user post list ID

JSON.SET – Replaces the existing post with a new one based off the provided information in the user post list

JSON.GET – Retrieves user post list

- **DeletePost**

Deletes the existing post created by the user.

```
async function deletePost(token, pid) {
	var name = await authUser(token);
const hget = promisify(client.hget).bind(client);
	var id = await hget([name, 'id']);


	const json_get = promisify(client.json_get).bind(client);
	const json_set = promisify(client.json_set).bind(client);
	var posts = await json_get(id, ".");
	posts = JSON.parse(posts);
	console.log(posts);
	if (posts == null) {
		posts = [];
	}
	var vis;
	for (var i = 0; i < posts.length; i++) {
		if (posts[i]["pid"] == pid) {
			vis = posts[i]["visibility"];
			posts.splice(i, 1);
			break;
		}
	}
	await json_set(id, '.', JSON.stringify(posts));

	if (vis === "on") {
		var posts = await json_get('globalPosts', ".");
		posts = JSON.parse(posts);
		if (posts == null) {
			posts = [];
		}
		for (var i = 0; i < posts.length; i++) {
			if (posts[i]["pid"] == pid) {
				posts.splice(i, 1);
				break;
			}
		}
		await json_set('globalPosts', '.', JSON.stringify(posts));
	}

}


```

HGET – Retrieves user post list ID

JSON.SET – Removes post and adds to the user post list

JSON.GET – Retrieves the user post list

- **PostInfo**

Retrieves information (title, description, image, materials, directions, comments) of specified post.

```
app.get('/postInfo', async (req, res) => {
	var pid = req.query.pid;
	var post = await findPostByID(pid);
	res.send(post);

})


```

JSON.GET – Retrieves post from the user post list

- **AllPosts**

Retrieves all global posts or those created by the specific user.

```
app.get('/allPosts', async (req, res) => {
	var name = req.query.name;
	const hget = promisify(client.hget).bind(client);
	const lr = promisify(client.lrange).bind(client);
	const hgetall = promisify(client.hgetall).bind(client);

	const json_get = promisify(client.json_get).bind(client);

	var id = await hget([name, 'id']);
	var posts = await json_get(id);
	posts = JSON.parse(posts);
	var newposts = {"posts": []};
	if (posts != null) {
		for (var i = 0; i < posts.length; i++) {
			var p = posts[i];

			if (p["visibility"] === "on") {
				newposts["posts"].push(p);
			}
		}
	}
	console.log(newposts);
	res.send(newposts);
})


```

JSON.GET – Retrieves user or global post list

- **AllDrafts**

Retrieves all drafts created by the user.

```
app.get('/allDrafts', async (req, res) => {
	var name = req.query.name;
	const hget = promisify(client.hget).bind(client);
	const lr = promisify(client.lrange).bind(client);
	const hgetall = promisify(client.hgetall).bind(client);

	const json_get = promisify(client.json_get).bind(client);

	var id = await hget([name, 'id']);
	var posts = await json_get(id);
	posts = JSON.parse(posts);
	var newposts = {"posts": []};
	if (posts != null) {
		for (var i = 0; i < posts.length; i++) {
			var p = posts[i];

			if (p["visibility"] === "off") {
				newposts["posts"].push(p);
			}
		}
	}
	console.log(newposts);
	res.send(newposts);
})


```

JSON.GET – Retrieves user draft list

- **AddComment**

Allows users to comment on posts.

HGET – Retrieve post comment list ID

JSON.SET – Creates comment ands add to post comment list

JSON.GET – Retrieves post comment list

## 6. How it works

Anyone who’s on the site can search for materials they have or projects they’re interested in. To begin, simply visit the [Green Earth homepage](https://launchpad.redis.com/?id=project%3Agreenearth#:~:text=Images-,Homepage,-Post%20Search).

![The homepage screen of GreenEarth page with image of the Earth in space.](/images/blog/2ab9b870177dee6e69e2f2d7bd148180a176c8d5-1600x693.webp)

### How to find a project

Click on the ‘posts’ tab at the top of the page. This will take you to a search bar for you to enter the household item you’re looking to recycle. So for example, if you have a lot of tin cans that you want to repurpose, simply type in ‘tin cans’ or variations of that keyword (see image below).

![Image of tin cans repurposed as flower pots in the GreenEarth site.](/images/blog/a109403ea182ea69e1028c53c2ebb885ab2cda64-1600x841.webp)

Once you’ve typed this in, a list of projects that require your household item will be displayed. Clicking on one of the results will take you to the project page of that post.

Here you’ll discover everything you need to know about the project, ranging from user comments to the required materials through to the directions you’ll need to follow (see below).

![The Description section of the GreenEarth site.](/images/blog/8ed78779e8e5d323d1c654cf9de08dba7200724d-1600x841.webp)

![The Materials section of the GreenEarth site.](/images/blog/9efdfe1006d63175352ba20816b7e53361700f4f-1600x841.webp)

### How to create an account

Click on the ‘sign up’ tab at the top of the page. Here you’ll be able to create a username and password for your account.

Once you’ve created an account and are logged in, the next step will be to update your profile. You can do this by clicking on your username at the top of the navigation bar and selecting ‘profile.’

You’ll then be directed to your profile page which will be empty (see below).

![A page in the GreenEarth site for filling out a profile description.](/images/blog/9f48ac924acfa795201ded44f6f0084d0861154a-1600x622.webp)

From here you’ll be able to update every section of your profile, including your profile photo and bio.

### How to leave a comment

Once you’ve set-up a profile, you’ll then be able to leave comments on posts. To do this, first find a post you want to comment on (see ‘how to find a project’ section). The comment section in each post can be found at the bottom of the project page (see example below).

![Showing the Comments section of GreenEarth website.](/images/blog/378b6a5833272c7d96df5d50625f8173f984aec8-1600x788.webp)

### How to create a post

To create a post, you first need to go to your profile dashboard. Click on the ‘+’ sign at the top right hand corner of your profile (see below).

![A dashboard for creating a post in GreenEarth app with picture of Gandalf.](/images/blog/43683c7b3ca541320c36791bf6ffefb34eeee961-1600x788.webp)

You’ll then be directed to the ‘create a post page.’ From here you’ll see a number of different fields that need to be filled in, ranging from project name to directions through to the materials required to bring this project to life.

Add the details of your project in each section as demonstrated below.

![GreenEarth site image of a repurposed plastic bottle as a sprinkler. ](/images/blog/4cae3b878eba5bf51043ce3b676ec6d95096e3c5-1600x636.webp)

![A list of materials.](/images/blog/050d62e4dc3d9c8284d031eaf75c2bd56e978224-1600x636.webp)

Once you’ve completed each section, you’ll have the option to either delete, save or publish this post at the bottom of the page.

### How to edit a post

All of your drafts and posts will be displayed in your profile dashboard.

![A dashboard for editing a post in GreenEarth. ](/images/blog/f63b809f3489eefff6ab8654dcf64af6921c683e-1600x749.webp)

To edit one of these, first, click on the post or draft you want to edit. Next, click on the edit button on the bottom-left-hand side of the page. Alternatively, you can delete the post by clicking on the trash icon next to it.

## Conclusion: Championing the green movement with Redis

Climate change is on everyone’s radar, galvanizing people to adopt a greener way of living. But for green initiatives to come to fruition, online platforms need to be efficient and powered by a database that’s capable of transmitting data at great speed.

This is because any delays will hamper the user’s experience and push people away from these platforms. With Redis however, GreenEarth was able to function at such a speed that it enabled all components within the application to become more interconnected.

Thanks to Redis, retrieving user information from the cloud database, along with storing individual user attributes, was an effortless process. From start to finish, *everything* was carried out with hyper-efficiency.

![A redislaunchpad apps banner](/images/blog/4286535b4f0ad548b626a7e3bc36792d2aa0c568-1600x593.webp)

## Who built this app?

![Rajesh Ramamurthy](/images/blog/fb1e73b8a64a0f26fe8cdfec9211add87695c68c-400x400.webp)

### Rajesh Ramamurthy

Rajesh is a renowned problem solver in the tech-sphere, providing clients with simple solutions to complex problems.

Make sure to [check out his GitHub](https://github.com/rajkram) page to see what other projects he’s been involved with.

If you want to discover more about how this application was deployed, make sure to check out [Rajesh’s YouTube video here](https://www.youtube.com/watch?v=4SEACl3E3vY).

We also have a great selection of different applications for you to check out on the [Redis Launchpad](https://launchpad.redis.com/) where programmers across the globe are harnessing the power of Redis to change everyday lives. Check it out. Be inspired. And join in the fun.
