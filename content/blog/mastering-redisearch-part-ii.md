---
title: "Mastering RediSearch / Part II"
linkTitle: "Mastering RediSearch / Part II"
url: "/blog/mastering-redisearch-part-ii/"
description: "In our last installment, we started looking at RediSearch, the Redis search engine built as a module. We explored the curious nature of the keys and indexed a single document. In this segment,..."
date: 2017-12-07
blogCategories:
- "Company"
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Redis   · Published 7 December 2017 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/d5aae5e828916206e497a5d3802c021bf8c5a232-300x237.webp)

## Abstracting RediSearch

In [our last installment](/blog/mastering-redisearch-part/), we started looking at RediSearch, the Redis search engine built as a module. We explored the curious nature of the keys and indexed a single document. In this segment, we’ll lay the groundwork necessary to make working with RediSearch more productive and useful in Node.js.

## Welcoming RediSearch into Javascript

Now, we could certainly bring in all this data using the RediSearch commands directly or with [the bindings](https://github.com/stockholmux/node_redis-redisearch), but with a large amount of data using direct syntax becomes difficult to manage. Let’s take some time to develop a small Node.js module that will make our lives easier.

I’m a big fan of the so-called “fluent” Javascript syntax, wherein you chain methods together so that functions are separated by dots when operating over a single object. If you’ve used jQuery then you’ve seen this style.

```javascript
$('.some-class')
    .css('color','red')
    .addClass('another-class')
    .on('click',function() { ... });

```

This approach will present some challenges. Firstly, we need to make sure that we can interoperate with “normal” Redis commands and still be able to use pipelining/batching (we’ll address the use of [MULTI](https://redis.io/commands/multi) in a later installment). Also, RediSearch commands have a highly variadic syntax (e.g. commands can have a small or large number of arguments). Translating this directly into Javascript wouldn’t gain us much over the simple bindings. We can, however, leverage a handful of arguments and then supply optional arguments in the guise of function-level *options* objects. What I’m aiming to design looks a little like this:

```javascript
const myRediSearch = rediSearch(redisClient,'index-key');
 myRediSearch.createIndex([ ...fields... ],cbFn);
 myRediSearch
    .add(itemUniqueId,itemDataAsObject,cbFn)
    .add(anotherItemUniqueId,anotherItemDataAsObject,addOptions, cbFn);


```

Overall, this is a much more idiomatic way of doing things in Javascript and that’s important when trying to get a team up to speed, or even just to improve the development experience.

Another goal of this module is to make the results more usable. In Redis, results are returned in what is known as a “nested multi bulk” reply. Unfortunately, this can get quite complex with RediSearch. Let’s take a look at some results returned from redis-cli:

```javascript
1) (integer) 564
2) "52fe47729251416c75099985"
3)   1) "movie_id"
     2) "18292"
     3) "title"
     4) "George Washington"
     5) "department"
     6) "Editing"
     7) "job"
     8) "Editor"
     9) "name"
    10) "Zene Baker"
    11) "crew"
    12) "1"
 4) "52fe48cbc3a36847f8179cc7"
 5)  1) "movie_id"
     2) "55420"
     3) "title"
     4) "Another Earth"
     5) "character"
     6) "Kim Williams"
     7) "cast_id"
     8) "149550"
     9) "name"
    10) "Jordan Baker"
    11) "cast"
    12) "1"


```

So, when using [node_redis](https://github.com/NodeRedis/node_redis) you would get nested arrays at two levels, but positions are associative (except for the first one which is the number of results). Without writing an abstraction, it’ll be a mess to use. We can abstract the results into more meaningful nested objects with an array to represent the actual results. The same query would return this type of result:

```python
{
  "results": [
    {
      "docId": "52fe47729251416c75099985",
      "doc": {
        "movie_id": "18292",
        "title": "George Washington",
        "department": "Editing",
        "job": "Editor",
        "name": "Zene Baker",
        "crew": "1"
      }
    },
    {
      "docId": "52fe48cbc3a36847f8179cc7",
      "doc": {
        "movie_id": "55420",
        "title": "Another Earth",
        "character": "Kim Williams",
        "cast_id": "149550",
        "name": "Jordan Baker",
        "cast": "1"
      }
    }
  ],
  "totalResults": 564,
  "offset": 0,
  "requestedResultSize": 2,
  "resultSize": 2
}

```

So, let’s get started on writing a client library to abstract RediSearch.

## RediSearchClient Abstraction Components

Let’s first examine the entire “stack” of components that let you access RediSearch at a higher level.

```python
[Your Application]
  ├── RediSearchClient - Abstraction
  │   ├── node_redis-redisearch - Bindings to Redis module commands 
  └───┴── node_redis - Redis library for Node.js
          └── Redis - Data Store
               └── RediSearch - Redis Module

```

This is a bit confusing due to the terminology and duplication, but each layer has its own job.

[node_redis-redisearch](https://github.com/stockholmux/node_redis-redisearch) just provides the commands to node_redis, without any parsing or abstraction. node_redis just opens up the world of Redis to Javascript. Got it? Good.

## Detecting RediSearch Bindings

Since RediSearch isn’t a default part of Redis, we need to check that it is installed. We’re going to make the assumption that RediSearch is installed on the underlying Redis server. If it isn’t installed then you’ll simply get a Redis error similar to this:

```javascript
ERR unknown command 'ft.search'
```

Not having the bindings is a more subtle error (complaining about an undefined function), so we’ll build in a simple check for the *ft_create* command on the instance of the Redis client.

## Creating the client

To be able to manage multiple different indexes and potentially different clients in a way that isn’t syntactically ugly and inefficient, we’ll use a factory pattern to pass in both the client and the index key. You won’t need to pass these again. The last two arguments are optional: an *options* object and/or a callback.

It looks like this:

```javascript
...
rediSearchBindings(redis);
let mySearch = rediSearch(client,'my-index');
//with optional options object
let mySearch = rediSearch(client,'my-index', { ... });
//with optional options object and callback.
let mySearch = rediSearch(client,'my-index', { ... }, function() { ... });
...
```

The callback here doesn’t actually provide an error in its arguments; it is just issued when the node_redis client is ready. It is entirely optional and provided primarily for benchmarking so you don’t start counting down the time until the connection is fully established.

Another useful feature of this function is that the first argument can optionally be the node_redis module. We’ll also automatically add in the RediSearch bindings in this case. You can designate this library to manage the creation of your client and specify other connection preferences in the *options* object located at *clientOptions*. Many scripts have specialized connection management routines so it is completely optional to pass either a client or the node_redis module.

We’ll be using similar signatures for most functions and the final two arguments are optional: an *options* object and a callback. Consistency is good.

## Creating an index

Creating an index in RediSearch is a one-time affair. You set up your schema prior to indexing data and then you can’t alter the schema without re-indexing the data.

As previously discussed, there are three basic types of indexes in RediSearch:

- Numeric
- Text
- Geo

*(Note: there is a fourth type of index, the tag index, but we’ll cover that in a later installment)*

Each field can have a number of options—this can be a lot to manage! So let’s abstract this by returning a *fieldDefinition* object that has three functions: *numeric*, *text*, and *geo*. Seems familiar, eh?

All three methods have two required options and text fields have an optional *options* object. They are in this order:

- Field Name — String
- Sortable — Boolean
- Options — Object (optional, *text* fields only) with two possible properties: *noStem* (do not [stem](https://en.wikipedia.org/wiki/Stemming) words) and *weight* (sorting weight)

These methods return arrays of strings that can be used to build a RediSearch index. Let’s take a look at a few examples:

```javascript
mySearch.fieldDefinition.text('companyName',true,{ noStem : true }); // -> [ 'companyName', 'TEXT', 'NOSTEM', 'SORTABLE' ]
mySearch.fieldDefinition.numeric('revenue',false); // -> [ 'revenue', 'NUMERIC' ]
mySearch.fieldDefinition.geo('location',true); // -> [ 'location', 'GEO', 'SORTABLE' ]

```

So, what do we do with these little functions? Of course, we use them to specify a schema.

```javascript
mySearch.createIndex([
    mySearch.fieldDefinition.text('companyName',true,{ noStem : true }),
    mySearch.fieldDefinition.numeric('revenue',false),
    mySearch.fieldDefinition.geo('location',true)],
    function(err) {
       /* ... do stuff after the creation of the index ... */
    }
 );

```

This makes a clear and expressive statement on the fields in the schema. One note here: while we use an array to contain the fields, RediSearch has no concept of order in fields, so it doesn’t really matter in which order you specify fields in the array.

## Adding items to an index

Adding the item to a RediSearch index is pretty simple. To add an item, we supply two required arguments and consider two optional arguments. The required arguments are (in order):

- a unique ID
- the data as an object

The two optional arguments follow our common signature: *options* and a callback. As per common Node.js patterns, the first argument of the callback is an error object (unset if no errors) and the second argument of the callback is the actual data.

```javascript
myRediSearch
    .add('kyle',{
       dbofchoice       : 'redis',
       languageofchoice : 'javascript'
    },
    {
      score             : 5
    }, 
    function(err) {
       if (err) { throw err; }
       console.log('added!');
    }
 );

```

## Batches (aka Pipelines)

Batch, or “pipeline” as it’s called in the non-Node.js Redis world, is a useful structure in Redis, it allows for multiple commands to be sent at a time without waiting for a reply for each command.

The batch function works pretty similarly to any batch you’d find in node_redis — you can chain them together with an *exec()* at the end. This does cause a conflict, though. Since ‘normal’ node_redis allows you to batch together commands, you need to distinguish between RediSearch and non-RediSearch commands. First, you need to start a RediSearch batch using one of two methods:

### Start a new batch

```javascript
let searchBatch = mySearch.batch() // a new, RediSearch enhanced batch
```

### Or, with an existing batch

```javascript
let myBatch = client.batch();
let searchBatch = mySearch.batch(myBatch) // a batch command, perhaps already in progress

```

After you have created the batch, you can add normal node_redis commands to it or you can use RediSearch commands.

```javascript
searchBatch
   .rediSearch.add(...)
   .hgetall(...)
   .rediSearch.add(...)
```

Take note of the HGETALL stuck in the middle of this chain; this is to illustrate that you can intermix abstracted RediSearch commands with ‘normal’ Redis commands. Cool, right?

As mentioned earlier, the output of RediSearch (and many Redis commands) is likely in a form that you wouldn’t use directly. FT.GET and FT.SEARCH produce interleaved field / value results that get represented as an array, for example. The idiomatic way of dealing with data like this in Javascript is through plain objects. So we need to do some simple parsing of the interleaved data. There are many ways to accomplish this, but the simplest way is to use a [lodash](https://lodash.com/) chain to first [chunk](https://lodash.com/docs/4.17.4#chunk) the array into 2-length individual arrays then use the [fromPairs](https://lodash.com/docs/4.17.4#fromPairs) function to convert the 2-length arrays into field/values in a single object. We’ll be using this quite a bit so we’ll contain it in the non-public function *deinterleave* in order to reduce repetition.

```python
const deinterleave = function(doc) { // `doc` is an array like this `['fname','kyle','lname','davis']`
  return  _(doc)                     // Start the lodash chain with `doc`
    .chunk(2)                        // `chunk` to convert `doc` to `[['fname','kyle'],['lname','davis']]`
    .fromPairs()                     // `fromPairs` converts paired arrays into objects `{ fname : 'kyle', lname : 'davis }`
    .value();                        // Stop the chain and return it back
}

```

If we didn’t need to contend with pipelines, adding these parsing functions would be a somewhat simple process of monkey patching the client. But with batches in node_redis, the results are provided both in a function-level callback and at the end of the batch, with many scripts omitting function-level callbacks and just dealing with all the results at the end. Given this, we need to make sure that the commands are only parsing these values when needed—but always at the end.

Additionally, this opens up a can-of-worms when writing our abstraction. Normal client objects and pipeline objects both need RediSearch-specific commands injected. To prevent writing two different repetitious functions, we need to have one function that can be dynamically injected. To accomplish this, the factory pattern is employed : the outer function is passed in a client or pipeline object (let’s call it *cObj*) and then it returns a function with the normal arguments. *cObj* can represent either a pipeline or just a node_redis client.

Thankfully, node_redis is consistent in how it handles pipelined and non-pipelined commands, so the only thing that changes is the object being chained. There are only two exceptions:

- In the commands that need special result parsing, we augment the pipeline object with a parser property that is itself a plain object. This contains the appropriate parsing function to be completed at the end. We need to use a plain object here rather than an array in order to avoid sparseness when the parsing is not needed.
- To enable chaining you need to be able to return the correct value: either the general *rediSearch* object for non-pipelined calls or the pipeline object itself.

These two exceptions only need to be applied when pipelined, thus we need to be able to detect pipelining. To do this, we have to look at the name of the constructor. It’s been abstracted into the function *chainer*.

## Searching

In the RediSearch module, search is executed with the FT.SEARCH command, which has a ton of options. We’ll abstract this into our *search* method. At this point we’re going to provide only the bare minimum of searching abilities — we’ll pass in a search string (where you can use RediSearch’s extensive query language), then an optional Options argument and finally, a callback. Technically the callback is optional, but it would be silly not to include it.

In our initial implementation, we’ll just make a couple of options available:

- *offset* – where to begin the result set
- *numberOfResults* – the number of results to be returned

These options map directly to the RediSearch LIMIT argument (very similar to the LIMIT argument found throughout SQL implementations).

The search also implements a result parser to make things a little more useable. The output object ends up looking like this:

```python
{
  "results": [
    {
      "docId": "19995",
      "doc": {
        "budget": "237000000",
        "homepage": "http://www.avatarmovie.com/",
        "original_language": "en",
        "original_title": "Avatar",
        "overview": "In the 22nd century, a paraplegic Marine is dispatched to the moon Pandora on a unique mission, but becomes torn between following orders and protecting an alien civilization.",
        "popularity": "150.437577",
        "release_date": "1260403200000",
        "revenue": "2787965087",
        "runtime": "162",
        "status": "Released",
        "tagline": "Enter the World of Pandora.",
        "title": "Avatar",
        "vote_average": "7.2",
        "vote_count": "11800"
      }
    }
  ],
  "totalResults": 1,
  "offset": 0,
  "requestedResultSize": 10,
  "resultSize": 1
}

```

The property *results* is an ordered array of the results (with the most relevant results at the top). Notice that each result has both the ID of the document (*docId*) and the fields in the document (*doc*). *totalResults* is the number of items index that match the query (irrespective of any limiting). *requestedResultSize* is the maximum number of results to be returned. *resultSize* is the number of results returned.

## Getting a document

In the previous section you may have noticed the *docId* property. RediSearch stores each document by a unique ID that you need to specify at the time of indexing. Documents can be retrieved by searching or by directly fetching the *docId* using the RediSearch command FT.GET. In our abstraction, we’ll call this method *getDoc* ([*get*](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/get)[ has a specific meaning in Javascript](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/get), so it should be avoided as a method name). *getDoc*, like most other commands in our module, has a familiar argument signature:

- *docId* is the first argument and only required argument. You pass in the ID of the previously indexed item.
- *options* is the second argument and is optional. We aren’t actually using it yet, but we’ll keep it here for future expansion.
- *cb* is the third argument and is technically optional—this is where you provide your callback function to get your results.

Like the *search* method, *getDoc* does some parsing to turn the document from an interleaved array into a plain Javascript object.

## Getting rid of an index

One more important thing to cover before we have a minimal set of functionalities — the *dropIndex*, which is just a simple wrapper for the command FT.DROP is a little different as all it takes is a callback for when the index is dropped.

Neither *dropIndex* nor *createIndex* allow for chaining as the nature of these commands prevent them from having further chained functions.

## Conclusion

In this piece we’ve discussed the creation of a limited abstraction library for RediSearch in Node.js, as well as its syntax. Reaching back to our previous piece, let’s look at the same small example to see the complete index lifecycle.

```python
/* jshint node: true, esversion: 6 */

const 
  argv        = require('yargs')                                              // `yargs` is a command line argument parser
                .demand('connection')                                         // pass in the node_redis connection object location with '--connection'
                .argv,                                                        // return it back as a plain object
  connection  = require(argv.connection),                                     // load and parse the JSON file at `argv.connection`
  redis       = require('redis'),                                             // node_redis module
  rediSearch  = require('./index.js'),                                        // rediSearch Abstraction library
  data        = rediSearch(redis,'the-bard',{ clientOptions : connection });  // create an instance of the abstraction module using the index 'the-bard'
                                                                              // since we passed in redis module instead of a client instance, it will create a client instance
                                                                              // using the options specified in the 3rd argument.
data.createIndex([                                                            // create the index using the following fields
    data.fieldDefinition.text('line', true),                                  // field named 'line' that holds text values and will be sortable later on
    data.fieldDefinition.text('play', true, { noStem : true }),               // 'play' field is a text values that won’t be stemmed
    data.fieldDefinition.numeric('speech',true),                              // 'speech' is a numeric field that is sortable
    data.fieldDefinition.text('speaker', false, { noStem : true }),           // 'speaker' is a text field that is not stemmed and not sortable
    data.fieldDefinition.text('entry', false),                                // 'entry' is a text field that stemmed and not sortable
    data.fieldDefinition.geo('location')                                      // 'location' is a geospatial index
  ],
  function(err) {                                                             // Error first callback after the index is created
    if (err) { throw err; }                                                   // Handle the errors
    data.batch()                                                              // Start a 'batch' pipeline
      .rediSearch.add(57956, {                                                // index the object at the ID 57956
        entry     : 'Out, damned spot! out, I say!--One: two: why,',
        line      : '5.1.31',
        play      : 'macbeth',
        speech    : '15',
        speaker   : 'LADY MACBETH',
        location  : '-3.9264,57.5243'
      })
      .rediSearch.getDoc(57956)                                               // Get the document index at 57956
      .rediSearch.search('spot')                                              // Search all fields for the term 'spot'
      .rediSearch.exec(function(err,results) {                                // execute the pipeline
        if (err) { throw err; }                                               // Handle the errors
        console.log(JSON.stringify(results[1],null,2));                       // show the results from the second pipeline item (`getDoc`)
        console.log(JSON.stringify(results[2],null,2));                       // show the results from the third pipeline item (`search`)
        data.dropIndex(function(err) {                                        // drop the index and send any errors to `err`
          if (err) { throw err; }                                             // handle the errors
          data.client.quit();                                                 // `data.client` is direct access to the client created in the `rediSearch` function
        });
      });
  }
);

```

As you can see, this example covers all the bases, though it probably isn’t very useful in a real-world scenario. In our next installment we’ll dig into the TMDB dataset and start playing with real data and further expanding our client library for RediSearch.

In the meantime, I suggest you take a look at the [GitHub repo](https://github.com/stockholmux/RediSearchClient) to see how it’s all structured.
