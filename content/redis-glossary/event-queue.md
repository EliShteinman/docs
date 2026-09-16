---
title: "Event Queue"
linkTitle: "Event Queue"
url: "/glossary/event-queue/"
description: "An event queue is a data structure used in computer programming to manage and process events in an asynchronous, non-blocking way. It is typically used in event-driven programming, where an..."
lastmod: 2026-05-21
mirrored: true
---

*updated 21 May 2026*

## Event Queue Defined

An event queue is a data structure used in computer programming to manage and process events in an asynchronous, non-blocking way. It is typically used in event-driven programming, where an application responds to user input or system events by executing a sequence of code known as an event handler.

When an event occurs, such as a button click or a network request completion, it is added to the event queue along with any associated data. The event queue then processes the events in the order they were received, typically by invoking the appropriate event handler function for each event.

By using an event queue, an application can handle multiple events simultaneously without blocking the main execution thread. This allows for more efficient use of system resources and can improve the responsiveness of the application.

Event queues can be implemented using a variety of data structures, such as linked lists or priority queues, depending on the specific requirements of the application. They are used in many types of applications, including graphical user interfaces, web servers, and video games.

## Event Queue Best Practices

Redis Lists are an ordered list of strings very much akin to the linked lists in which you may be familiar. Pushing, adding a value to a list, and popping, removing a value from a list (from either the left/head/start or right/tail/end), are very lightweight operations. As you might imagine, this is a very good structure for managing a queue: add items to the list to the head and read items out the tail for a first-in-first-out (FIFO) queue.

Redis also provides additional features that make this type of pattern more efficient, reliable, and easy to use. There is a subset of the list commands that allow for “blocking” behavior. The term “blocking” applies only to a single client connected—in effect these commands stop the client from doing anything until a list has an a value (or a timeout has elapsed). This removes the need to poll Redis for results. Since the client can’t do anything while waiting for values, we’ll need two open clients to illustrate this:

In this example in row 1, we see that the blocking client does not immediately return anything as the list (“my-q”) does not have any values in it. The last argument is the timeout—in this case the zero means that it will never timeout and will wait forever. The second row the sending client issues a LPUSH to the my-q key and immediately the other client ends its blocking. On the third row we can issue another BRPOP command (usually accomplished with a loop in your client language) and wait for any further list values. You can get out of blocking in redis-cli with ctrl-c.

Let’s invert this example and see how BRPOP works with a non-empty list:

In this example in row 1, we see that the blocking client does not immediately return anything as the list (“my-q”) does not have any values in it. The last argument is the timeout—in this case the zero means that it will never timeout and will wait forever. The second row the sending client issues a LPUSH to the my-q key and immediately the other client ends its blocking. On the third row we can issue another BRPOP command (usually accomplished with a loop in your client language) and wait for any further list values. You can get out of blocking in redis-cli with ctrl-c.

Let’s invert this example and see how BRPOP works with a non-empty list:

In rows 1-3 we push three values into the list and the we can see the response growing (representing the number of items in the list). Row 4, despite issuing a BRPOP command, returns the value immediately? Why because the blocking behavior applies only only if there is no items in the queue. We can see the same immediate response in rows 5-6 because it’s going through each item in the queue. In row 7, BRPOP encounters an empty queue and blocks until items are added to the queue.

Queues often represent some sort of job that needs to be accomplished in another process (a worker). Critical in this type of workload is that if a worker has a fault and dies for some reason during processing, the job is not lost. Redis can support this type of queue as well. Instead of using BRPOP, substitute BRPOPLPUSH. BRPOPLPUSH (what a mouthful) waits for a values in one list and once it’s got one, it pushes it to another list. This is all accomplished atomicly, so it’s not possible for two workers to remove/take the same value. Let’s take a look at how this would work:

In rows 1 and 2, we’re not doing anything yet since worker-q is empty. If something came out of woker-q, we would process it and remove it then jump back to 1 to see if anything else is in the queue. This way we are clearing the worker queue first and doing whatever jobs already exist. In row 4 we wait until a value is added to to my-q and when we get a value it’s atomicly added to worker-q. Next, we do some type of non-Redis operation to “hello” when we’re done we remove one instance from the worker-q with LREM and loop back to row 1.

The real key is that if the process dies during the operation in row 6, we still have this job in worker-q. Upon restart of the process, we’ll immediately clear any jobs that haven’t been removed by row 7. This pattern greatly reduces the possibility that jobs will be lost. It is possible, however, that a job could be processed twice, but only if the worker dies “between” rows 2 and 3 or 5 and 6, which is unlikely, but it would be a best practice to account for this circumstance in your worker logic.
