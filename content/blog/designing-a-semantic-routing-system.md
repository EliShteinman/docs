---
title: "Designing a semantic routing system: From static rules to dynamic intelligence with Redis and Java"
linkTitle: "Designing a semantic routing system: From static rules to dynamic intelligence with Redis and Java"
url: "/blog/designing-a-semantic-routing-system/"
description: "A semantic routing pattern is a powerful technique used in intelligent systems to classify incoming requests based on their meaning and direct them to the most appropriate processing path. Unlike..."
date: 2026-04-08
blogCategories:
- "Tech"
authors:
- "Tony Wu"
lastmod: 2026-04-08
hidden: true
mirrored: true
---

*By Tony Wu, Sr. Solution Architect · Published 8 April 2026*

![Designing a semantic routing system: From static rules to dynamic intelligence with Redis and Java](/images/site-mirror/5af107492cc62cc440f95b210bde904289dfdde6-1200x628.webp)

A **semantic routing pattern** is a powerful technique used in intelligent systems to classify incoming requests based on their meaning and direct them to the most appropriate processing path. Unlike traditional rule-based approaches that rely on keywords or binary logic, semantic routing leverages embeddings and similarity matching to understand user intent. By comparing an input against predefined categories—such as FAQ, restricted topics, or complex queries—the system can efficiently determine how to handle each request. This enables use cases like routing simple questions to low-cost pipelines, blocking sensitive topics, or escalating complex queries to advanced models, all within milliseconds.

In a production environment, flexibility is critical. Rather than hardcoding routing rules, modern systems allow configurations to be defined and updated dynamically. In this approach, routing definitions are stored in Redis as a centralized source of truth. The application loads these configurations at runtime to build the router, while also exposing services that enable users to update or extend routing rules without requiring redeployment. This design ensures scalability, maintainability, and real-time adaptability.

To support semantic routing, this sample leverages **RedisVL for Java**, a library that simplifies working with vector embeddings and similarity search in Redis. RedisVL provides high-level abstractions for vector indexing, embedding storage, and similarity-based retrieval. In this setup, the stored example queries act as reference data that can be vectorized and used by the semantic router to match incoming user inputs based on meaning rather than exact keywords.

Find the source code here: [https://github.com/Redislabs-Solution-Architects/semantic-router-with-redis](https://github.com/Redislabs-Solution-Architects/semantic-router-with-redis)

## 1. Define default routing config in Java and store in Redis

The first step is to establish a default routing configuration directly in the application code. This configuration maps each category—such as sports, technology, or business—to a set of representative example queries that define its semantic intent. When the `loaddefaultRouterConfig()` method is executed, it begins by clearing any existing routing data in Redis to prevent inconsistencies or stale entries. It then iterates through each category and stores the associated queries in Redis using a structured key format (e.g., `router:sports`). Each query is saved as a field in a Redis hash. By persisting this data in Redis, the system externalizes its routing knowledge, making it reusable, shareable, and independent of application memory.

Code snippet is as follows.

```
public Boolean loaddefaultRouterConfig() {
    Map<String, List<String>> defaultRouterConfig = new HashMap<>();

    defaultRouterConfig.put("sports", List.of(
            "who won the game last night?",
            "tell me about the upcoming sports events",
            "what's the latest in the world of sports?",
            "sports",
            "basketball and football"
    ));

    defaultRouterConfig.put("entertainment", List.of(
            "what are the top movies right now?",
            "who won the best actor award?",
            "what's new in the entertainment industry?"
    ));

    defaultRouterConfig.put("technology", List.of(
            "what are the latest advancements in AI?",
            "tell me about the newest gadgets",
            "what's trending in tech?"
    ));

    defaultRouterConfig.put("politics", List.of(
            "what are the latest political developments?",
            "who won the recent election?",
            "what policies are being debated right now?",
            "politics",
            "government and public policy"
    ));

    defaultRouterConfig.put("business", List.of(
            "what are the latest stock market trends?",
            "tell me about major company mergers?",
            "what's happening in the global economy?",
            "business",
            "finance and investment news"
    ));

    System.out.println("Map size: " + defaultRouterConfig.size());
    System.out.println(defaultRouterConfig.keySet());

    try {
        //delete all old keys
        String pattern = "router:*";
        Set<String> keys = jedis.keys(pattern);

        if (!keys.isEmpty()) {
            jedis.del(keys.toArray(new String[0]));
        }

        for (Map.Entry<String, List<String>> entry : defaultRouterConfig.entrySet()) {
            String redisKey = "router:" + entry.getKey();
            int index = 0;
            for (String question : entry.getValue()) {
                jedis.hset(redisKey, String.valueOf(index), question);
                index++;
            }
        }

        return true;
    }
    catch (Exception e) {
        System.err.println(e.getMessage());
        return false;
    }
}

```

## 2. Build a service to update router settings dynamically

To support runtime flexibility, a service layer is introduced to allow users or external systems to modify routing configurations dynamically. The `updateRouter()` method serves this purpose by accepting a new set of categories and example queries. For each category, it replaces the existing Redis entry by deleting the old key and inserting the updated values. This ensures that updates are applied cleanly and consistently at the category level. In a real-world app, this functionality would typically be exposed via a REST API, letting users add new categories, refine example queries, or adjust routing behavior without redeploying the system. This approach transforms routing from a static configuration into a dynamic, user-driven capability.

Code snippet is as follows.

```
public Boolean updateRouter(Map<String, List<String>> newRouterConfig) {
    newRouterConfig.forEach((className, questions) -> {
        System.out.println("Class: " + className);
        questions.forEach(q -> System.out.println("Question: " + q));

        String redisKey = "router:" + className;
        jedis.del(redisKey);

        int index = 0;
        for (String question : questions) {
            jedis.hset(redisKey, String.valueOf(index), question);
            index++;
        }
    });

    return true;
}

```

## 3. Build the semantic router dynamically from Redis

Once routing data is stored in Redis, the system can dynamically construct the semantic router at runtime. The `build()` method scans all Redis keys that match the routing pattern, retrieves their associated queries, and transforms each category into a `Route` object. Each route includes a name, a set of reference examples for semantic comparison, metadata such as category and priority, and a distance threshold that controls matching sensitivity. These routes are then aggregated into a router configuration, which defines how many matches to consider and how similarity scores are calculated. Finally, the `SemanticRouter` is instantiated using this configuration along with a vectorizer for embedding generation. Because the router is built entirely from Redis data, any updates made through the service layer are automatically reflected, resulting in a fully dynamic and data-driven routing system.

Code snippet is as follows.

```
public SemanticRouter build(){
    String cursor = ScanParams.SCAN_POINTER_START;
    ScanParams params = new ScanParams().match("router:*").count(100);
    List<Route> routeList = new ArrayList<>();

    do {
        ScanResult<String> scanResult = jedis.scan(cursor, params);
        List<String> scannedKeys = scanResult.getResult();

        if (!scannedKeys.isEmpty()) {
            for (String key : scannedKeys) {
                Map<String, String> hashValues = jedis.hgetAll(key);
                List<String> values = new ArrayList<>(hashValues.values());

                /*List<String> values = jedis.lrange(key, 0, -1);*/

                Route routes = Route.builder()
                        .name(key)
                        .references(values)
                        .metadata(Map.of("category", key, "priority", 1))
                        .distanceThreshold(0.71)
                        .build();

                routeList.add(routes);
            }
        }
        cursor = scanResult.getCursor();
    } while (!cursor.equals(ScanParams.SCAN_POINTER_START));

    // maxK = how many routes you get back;
    // aggregationMethod = how their per-reference distances are combined into a single route distance for ranking.
    RoutingConfig cfg = RoutingConfig.builder()
            .maxK(5)
            .aggregationMethod(DistanceAggregationMethod.AVG) // or MIN / SUM
            .build();
}

```

## Workflow

1. **Initialize** → Load default categories and store them in Redis
1. **Update** → Users modify routing rules via a service → Redis is updated
1. **Runtime** → The router reads from Redis, builds routes, and processes queries

## Frontend view to use the service

The frontend might appear as shown below.

 1. The Semantic routing configuration is visible to the user.

![Semantic routing settings](/images/site-mirror/67a0643b66010bb76a72b677c8178952563de7b1-1600x503.webp)

 2. The user has the ability to submit queries for verification of the routing outcome.

![Router for questions](/images/site-mirror/d559d8c843878fd4fb30c848b5a5cacac11da389-545x182.webp)

 3. User can submit new question list and assign a category like “health”

![Submit question list](/images/site-mirror/16941d85e0e4dc1c84f390a7c5a5e5b804c15579-688x356.webp)

 4. Load the router for questions can get the updated routing settings

![Load the router for questions can get the updated routing settings](/images/site-mirror/bc8f5a36be46d1c2750131b10bc2de76ace1c1de-721x289.webp)

 5. The user can then inquire about "Health" to retrieve results for a new question category.

![The user can then inquire about "Health" to retrieve results for a new question category.](/images/site-mirror/d7906dd1bb40b615da53baa222bb302e7e633a68-411x176.webp)

## Flexible and scalable system architecture

This architecture cleanly separates **routing data** from **routing logic**, enabling a flexible and scalable system. By leveraging Redis as a dynamic configuration store and semantic similarity for intelligent classification, you create a routing mechanism that is both efficient and adaptable. As a result, your system can evolve over time—supporting new categories, refining intent recognition, and improving user experience—without requiring code changes or redeployments.
