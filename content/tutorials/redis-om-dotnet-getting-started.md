---
title: "Using Redis OM .NET to work with JSON and Hashes in Redis"
linkTitle: "Using Redis OM .NET to work with JSON and Hashes in Redis"
url: "/tutorials/redis-om-dotnet-getting-started/"
description: "Redis OM provides high-level abstractions for using Redis in .NET, making it easy to model and query your Redis domain objects."
date: 2026-02-25
lastmod: 2026-02-25
hidden: true
---

*Published 25 February 2026*

> **TL;DR:**
>
> Redis OM .NET is an object-mapping library that lets you persist, query, and aggregate C# objects in Redis using declarative attributes and LINQ-style syntax. It builds on top of the lower-level [StackExchange.Redis](/tutorials/develop/dotnet/) client and adds features like automatic index creation, full-text search, and server-side aggregations.

## What you'll learn

- How to map C# classes to Redis hashes and JSON documents using `[Document]` and field-level attributes
- How to store and retrieve .NET objects with `RedisCollection` and `RedisConnection`
- How to create secondary indexes for searching and sorting
- How to run full-text search and numeric range queries with LINQ expressions
- How to perform server-side aggregations, groupings, and reductions
- How to use geo-filters for location-based queries

## Prerequisites

- [.NET 6+ SDK](https://dotnet.microsoft.com/download) installed
- A running Redis instance (e.g., [Redis Cloud](https://redis.io/try-free/) or [Docker](https://hub.docker.com/_/redis): `docker run -dp 6379:6379 redis`)
- An IDE such as [VS Code](https://code.visualstudio.com/download), [Visual Studio](https://visualstudio.microsoft.com/), or [Rider](https://www.jetbrains.com/rider/)

Redis OM provides high-level abstractions for using Redis in .NET, making it easy to model and query your Redis domain objects.

Redis OM contains the following features:

- Declarative object mapping for Redis objects
- Declarative secondary-index generation
- Fluent APIs for querying Redis
- Fluent APIs for performing Redis aggregations

## Add and retrieve objects using Redis OM .NET

The Redis OM library supports declarative storage and retrieval of objects from Redis. You will still use the Document Attribute to decorate a class you'd like to store in Redis. From there, all you need to do is either call Insert or InsertAsync on the RedisCollection or Set or SetAsync on the RedisConnection, passing in the object you want to set in Redis. You can then retrieve those objects with Get<T> or GetAsync<T> with the RedisConnection or with FindById or FindByIdAsync in the RedisCollection.

```csharp
public class Program
{
    [Document(Prefixes = new []{"Employee"})]
    public class Employee
    {
        [RedisIdField]
        public string Id{ get; set; }

        public string Name { get; set; }

        public int Age { get; set; }

        public double Sales { get; set; }

        public string Department { get; set; }
    }

    static async Task Main(string[] args)
    {
        var provider = new RedisConnectionProvider("redis://localhost:6379");
        var connection = provider.Connection;
        var employees = provider.RedisCollection<Employee>();
        var employee1 = new Employee{Name="Bob", Age=32, Sales = 100000, Department="Partner Sales"};
        var employee2 = new Employee{Name="Alice", Age=45, Sales = 200000, Department="EMEA Sales"};
        var idp1 = await connection.SetAsync(employee1);
        var idp2 = await employees.InsertAsync(employee2);

        var reconstitutedE1 = await connection.GetAsync<Employee>(idp1);
        var reconstitutedE2 = await employees.FindByIdAsync(idp2);
        Console.WriteLine($"First Employee's name is {reconstitutedE1.Name}, they are {reconstitutedE1.Age} years old, " +
                          $"they work in the {reconstitutedE1.Department} department and have sold {reconstitutedE1.Sales}, " +
                          $"their ID is: {reconstitutedE1.Id}");
        Console.WriteLine($"Second Employee's name is {reconstitutedE2.Name}, they are {reconstitutedE2.Age} years old, " +
                        $"they work in the {reconstitutedE2.Department} department and have sold {reconstitutedE2.Sales}, " +
                        $"their ID is: {reconstitutedE2.Id}");
    }
}
```

The Code above will declare an Employee class, and allow you to add employees to Redis, and then retrieve Employees from Redis the output from this method will look like this:

```json
First Employee's name is Bob, they are 32 years old, they work in the Partner Sales department and have sold 100000, their ID is: 01FHDFE115DKRWZW0XNF17V2RK
Second Employee's name is Alice, they are 45 years old, they work in the EMEA Sales department and have sold 200000, their ID is: 01FHDFE11T23K6FCJQNHVEF92F
```

If you wanted to find them in Redis directly you could run HGETALL Employee:01FHDFE115DKRWZW0XNF17V2RK and that will retrieve the Employee object as a Hash from Redis. If you do not specify a prefix, the prefix will be the fully-qualified class name.

## Creating an index with Redis OM .NET

To unlock some of the nicest functionality of Redis OM, e.g., running searches, matches, aggregations, reductions, mappings, etc... You will need to tell Redis how you want data to be stored and how you want it indexed. One of the features the Redis OM library provides is creating indices that map directly to your objects by declaring the indices as attributes on your class.

Let's start with an example class.

```csharp
[Document]
public partial class Person
{
    [RedisIdField]
    public string Id { get; set; }

    [Searchable(Sortable = true)]
    public string Name { get; set; }

    [Indexed(Aggregatable = true)]
    public GeoLoc? Home { get; set; }

    [Indexed(Aggregatable = true)]
    public GeoLoc? Work { get; set; }

    [Indexed(Sortable = true)]
    public int? Age { get; set; }

    [Indexed(Sortable = true)]
    public int? DepartmentNumber { get; set; }

    [Indexed(Sortable = true)]
    public double? Sales { get; set; }

    [Indexed(Sortable = true)]
    public double? SalesAdjustment { get; set; }

    [Indexed(Sortable = true)]
    public long? LastTimeOnline { get; set; }

    [Indexed(Aggregatable = true)]
    public string Email { get; set; }
}
```

As shown above, you can declare a class as being indexed with the Document Attribute. In the Document attribute, you can set a few fields to help build the index:

| **Property Name**    | **Description**                                                                                                                       | **Default**                                   | **Optional**       |
| -------------------- | :------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------- | ------------------ | ---- |
| StorageType          | Defines the underlying data structure used to store the object in Redis, options are HASH and JSON                                    | HASH                                          | true               |
| IndexName            | The name of the index                                                                                                                 | `$"{SimpleClassName`                          | `.ToLower()}-idx}` | true |
| Prefixes             | The key prefixes for redis to build an index off of                                                                                   | `new string[]{$"{FullyQualifiedClassName}:"}` | true               |
| Language             | Language to use for full-text search indexing                                                                                         | `null`                                        | true               |
| LanguageField        | The name of the field in which the document stores its Language                                                                       | `null`                                        | true               |
| Filter               | The filter to use to determine whether a particular item is indexed, e.g. `@Age>=18`                                                  | `null`                                        | true               |
| IdGenerationStrategy | The strategy used to generate Ids for documents, if left blank it will use a [ULID](https://github.com/ulid/spec) generation strategy | UlidGenerationStrategy                        | true               |

### Field level declarations

#### Id fields

Every class indexed by Redis must contain an Id Field marked with the `RedisIdField`.

#### Indexed fields

In addition to declaring an Id Field, you can also declare indexed fields, which will let you search for values within those fields afterward. There are two types of Field level attributes.

1.  Indexed - This type of index is valid for fields that are of the type string, a Numeric type (double/int/float etc. . .), or can be decorated for fields that are of the type GeoLoc, the exact way that the indexed field is interpreted depends on the indexed type
2.  Searchable - This type is only valid for string fields, but this enables full-text search on the decorated fields.

##### IndexedAttribute properties

There are properties inside the IndexedAttribute that let you further customize how things are stored & queried.

| **PropertyName** | **type** | **Description**                                                                                                                                                                                                                                                                                                                                                 | **Default**                            | **Optional** |
| ---------------- | -------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- | ------------ |
| PropertyName     | `string` | The name of the property to be indexed                                                                                                                                                                                                                                                                                                                          | The name of the property being indexed | true         |
| Sortable         | `bool`   | Whether to index the item so it can be sorted on in queries, enables use of `OrderBy` & `OrderByDescending` \-> `collection.OrderBy(x=>x.Email)`                                                                                                                                                                                                                | `false`                                | true         |
| Normalize        | `bool`   | Only applicable for `string` type fields Determines whether the text in a field is normalized (sent to lower case) for purposes of sorting                                                                                                                                                                                                                      | `true`                                 | true         |
| Separator        | `char`   | Only applicable for `string` type fields Character to use for separating tag field, allows the application of multiple tags fo the same item e.g. `article.Category = technology,parenting` is delineated by a `,` means that `collection.Where(x=>x.Category == "technology")` and `collection.Where(x=>x.Category == "parenting")` will both match the record | `,`                                    | true         |
| CaseSensitive    | `bool`   | Only applicable for `string` type fields - Determines whether case is considered when performing matches on tags                                                                                                                                                                                                                                                | `false`                                | true         |

##### SearchableAttribute properties

There are properties for the SearchableAttribute that let you further customize how the full-text search determines matches

| **PropertyName** | **type** | **Description**                                                                                                                                                                                                                                           | **Default**                      | **Optional** |
| ---------------- | -------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------- | ------------ |
| PropertyName     | `string` | The name of the property to be indexed                                                                                                                                                                                                                    | The name of the indexed property | true         |
| Sortable         | `bool`   | Whether to index the item so it can be sorted on in queries, enables use of `OrderB`y & `OrderByDescending` -> `collection.OrderBy(x=>x.Email)`                                                                                                           | `false`                          | true         |
| NoStem           | `bool`   | Determines whether to use [stemming](https://redis.io/docs/latest/develop/ai/search-and-query/advanced-concepts/stemming/), in other words adding the stem of the word to the index, setting to true will stop the Redis from indexing the stems of words | `false`                          | true         |
| PhoneticMatcher  | `string` | The phonetic matcher to use if you'd like the index to use (PhoneticMatching)\[https://redis.io/docs/latest/develop/ai/search-and-query/advanced-concepts/phonetic_matching/] with the index                                                              | null                             | true         |
| Weight           | `double` | determines the importance of the field for checking result accuracy                                                                                                                                                                                       | 1.0                              | true         |

### Creating the index

After declaring the index, the creation of the index is pretty straightforward. All you have to do is call CreateIndex for the decorated type. The library will take care of serializing the provided type into a searchable index. The library does not try to be particularly clever, so if the index already exists it will the creation request will be rejected, and you will have to drop and re-add the index (migrations is a feature that may be added in the future)

```csharp
var connection = provider.Connection;
connection.CreateIndex(typeof(Person));
```

## Text searches in Redis OM .NET

The `RedisCollection` provides a fluent interface for querying objects stored in redis. This means that if you store an object in Redis with the Redis OM library you can query objects stored in Redis with ease using the LINQ syntax you're used to.

### Define the model

Let's start off by defining a model that we will be using for querying, we will use a `Employee` Class which will have some basic stuff we may want to query in it

```csharp
[Document]
public class Employee
{
    [Indexed]
    public string Name { get; set; }

    [Indexed(Aggregatable = true)]
    public int Age { get; set; }

    [Indexed(Aggregatable = true)]
    public double Sales { get; set; }

    [Searchable(Aggregatable = true)]
    public string Department { get; set; }
}
```

### Connect to Redis

Now we will initialize a RedisConnectionProvider, and grab a handle to a RedisCollection for Employee

```csharp
static async Task Main(string[] args)
{
    var provider = new RedisConnectionProvider("redis://localhost:6379");
    var connection = provider.Connection;
    var employees = prover.RedisCollection<Employee>();
    await connection.CreateIndexAsync(typeof(Employee));
}
```

### Create our index

Next we'll create the index, so next in our Main method, let's take our type and condense it into an index

### Seed some data

Next we'll seed a few piece of data in our database to play around with:

```csharp
var e1 = new Employee {Name = "Bob", Age = 35, Sales = 100000, Department = "EMEA Sales"};
var e2 = new Employee {Name = "Alice", Age = 52, Sales = 300000, Department = "Partner Sales"};
var e3 = new Employee {Name = "Marcus", Age = 42, Sales = 250000, Department = "NA Sales"};
var e4 = new Employee {Name = "Susan", Age = 27, Sales = 200000, Department = "EMEA Sales"};
var e5 = new Employee {Name = "John", Age = 38, Sales = 275000, Department = "APAC Sales"};
var e6 = new Employee {Name = "Theresa", Age = 30, Department = "EMEA Ops"};
var insertTasks = new []
    {
        employees.InsertAsync(e1),
        employees.InsertAsync(e2),
        employees.InsertAsync(e3),
        employees.InsertAsync(e4),
        employees.InsertAsync(e5)
        employees.InsertAsync(e6)
    };
await Task.WhenAll(insertTasks);
```

### Simple text query of an indexed field

With these data inserted into our database, we can now go ahead and begin querying. Let's start out by trying to query people by name. We can search for all employees named `Susan` with a simple Where predicate:

```csharp
var susans = employees.Where(x => x.Name == "Susan");
await foreach (var susan in susans)
{
    Console.WriteLine($"Susan is {susan.Age} years old and works in the {susan.Department} department ");
}
```

The `Where` Predicates also support `and`/`or` operators, e.g. to find all employees named `Alice` or `Bob` you can use:

```csharp
var AliceOrBobs = employees.Where(x => x.Name == "Alice" || x.Name == "Bob");
await foreach (var employee in AliceOrBobs)
{
    Console.WriteLine($"{employee.Name} is {employee.Age} years old and works in the {employee.Department} Department");
}
```

#### Limiting result object fields

When you are querying larger Documents in Redis, you may not want to have to drag back the entire object over the network, in that case you can limit the results to only what you want using a `Select` predicate. E.g. if you only wanted to find out the ages of employees, all you would need to do is select the age of employees:

```csharp
var employeeAges = employees.Select(x => x.Age);
await foreach (var age in employeeAges)
{
    Console.WriteLine($"age: {age}");
}
```

Or if you want to select more than one field you can create a new anonymous object:

```csharp
var employeeAges = employees.Select(x => new {x.Name, x.Age});
await foreach (var e in employeeAges)
{
    Console.WriteLine($"{e.Name} is age: {e.Age} years old");
}
```

#### Limiting returned objects

You can limit the size of your result (in the number of objects returned) with `Skip` & `Take` predicates. `Skip` will skip over the specified number of records, and `Take` will take only the number of records provided (at most);

```csharp
var people = employees.Skip(1).Take(2);
await foreach (var e in people)
{
    Console.WriteLine($"{e.Name} is age: {e.Age} years old");
}
```

### Full text search

There are two types of attributes that can decorate strings, `Indexed`, which we've gone over and `Searchable` which we've yet to discuss. The `Searchable` attribute considers equality slightly differently than Indexed, it operates off a full-text search. In expressions involving Searchable fields, equality—`==`— means a match. A match in the context of a searchable field is not necessarily a full exact match but rather that the string contains the search text. Let's look at some examples.

#### Find employee's in sales

So we have a `Department` string which is marked as `Searchable` in our Employee class. Notice how we've named our departments. They contain a region and a department type. If we wanted only to find all employee's in `Sales` we could do so with:

```csharp
var salesPeople = employees.Where(x => x.Department == "Sales");
await foreach (var employee in salesPeople)
{
    Console.WriteLine($"{employee.Name} is in the {employee.Department} department");
}
```

This will produce:

```json
Bob is in the EMEA Sales department
Alice is in the Partner Sales department
Marcus is in the NA Sales department
Susan is in the EMEA Sales department
John is in the APAC Sales department
```

Because they are all folks in departments called `sales`

If you wanted to search for everyone in a department in `EMEA` you could search with:

```csharp
var emeaFolks = employees.Where(x => x.Department == "EMEA");
await foreach (var employee in emeaFolks)
{
    Console.WriteLine($"{employee.Name} is in the {employee.Department} department");
}
```

Which of course would produce:

```json
Bob is in the EMEA Sales department
Susan is in the EMEA Sales department
Theresa is in the EMEA Ops department
```

### Sorting

If a `Searchable` or `Indexed` field is marked as `Sortable`, or `Aggregatable`, you can order by that field using `OrderBy` predicates.

```csharp
var employeesBySales = employees.OrderBy(x=>x.Name);
var employeesBySalesDescending = employees.OrderByDescending(x=>x.Name);
```

## Performing numeric queries with Redis OM .NET

In addition to providing capabilities for text queries, Redis OM also provides you the ability to perform numeric equality and numeric range queries. Let us assume a model of:

```csharp
[Document]
public class Employee
{
    [Indexed]
    public string Name { get; set; }

    [Indexed(Aggregatable = true)]
    public int Age { get; set; }

    [Indexed(Aggregatable = true)]
    public double Sales { get; set; }

    [Searchable(Aggregatable = true)]
    public string Department { get; set; }
}
```

Assume that we've connected to Redis already and retrieved a `RedisCollection` and seeded some data as such:

```csharp
var employees = provider.RedisCollection<Employee>();
var e1 = new Employee {Name = "Bob", Age = 35, Sales = 100000, Department = "EMEA Sales"};
var e2 = new Employee {Name = "Alice", Age = 52, Sales = 300000, Department = "Partner Sales"};
var e3 = new Employee {Name = "Marcus", Age = 42, Sales = 250000, Department = "NA Sales"};
var e4 = new Employee {Name = "Susan", Age = 27, Sales = 200000, Department = "EMEA Sales"};
var e5 = new Employee {Name = "John", Age = 38, Sales = 275000, Department = "APAC Sales"};
var e6 = new Employee {Name = "Theresa", Age = 30, Department = "EMEA Ops"};
employees.Insert(e1);
employees.Insert(e2);
employees.Insert(e3);
employees.Insert(e4);
employees.Insert(e5);
employees.Insert(e6);
```

We can now perform queries against the numeric values in our data as you would with any other collection using LINQ expressions.

```csharp
var underThirty = employees.Where(x=>x.Age < 30);
var middleTierSales = employees.Where(x=>x.Sales > 100000 && x.Sales < 300000);
```

You can of course also pair numeric queries with Text Queries:

```csharp
var emeaMidTier = employees.Where(x=>x.Sales>100000 & x.Sales <300000 && x.Department == "EMEA");
```

### Sorting

If an `Indexed` field is marked as `Sortable`, or `Aggregatable`, you can order by that field using `OrderBy` predicates.

```csharp
var employeesBySales = employees.OrderBy(x=>x.Sales);
var employeesBySalesDescending = employees.OrderByDescending(x=>x.Sales);
```

## Aggregations with Redis OM .NET

[Aggregations](https://redis.io/docs/latest/develop/ai/search-and-query/query/aggregation/) are a method of grouping documents together and run processing on them on the server to transform them into data that you need in your application, without having to perform the computation client-side.

### Anatomy of a Pipeline

Aggregations in Redis are build around an aggregation pipeline, you will start off with a RedisAggregationSet<T> of objects that you have indexed in Redis. From there you can

- Query to filter down the results you want
- Apply functions to them to combine functions to them
- Group like features together
- Run reductions on groups
- Sort records
- Further filter down records

### Setting up for Aggregations

Redis OM .NET provides an RedisAggregationSet<T> class that will let you perform aggregations on employees, let's start off with a trivial aggregation. Let's start off by defining a model:

```csharp
[Document]
public class Employee
{
    [Indexed]
    public string Name { get; set; }

    [Indexed]
    public GeoLoc? HomeLoc { get; set; }

    [Indexed(Aggregatable = true)]
    public int Age { get; set; }

    [Indexed(Aggregatable = true)]
    public double Sales { get; set; }

    [Indexed(Aggregatable = true)]
    public double SalesAdjustment { get; set; }

    [Searchable(Aggregatable = true)]
    public string Department { get; set; }
}
```

We'll then create the index for that model, pull out a RedisAggregationSet<T> from our provider, and initialize the index, and seed some data into our database

```csharp
var provider = new RedisConnectionProvider("redis://localhost:6379");
await provider.Connection.CreateIndexAsync(typeof(Restaurant));
var employees = provider.RedisCollection<Employee>();
var employeeAggregations = provider.AggregationSet<Employee>();
var e1 = new Employee {Name = "Bob", Age = 35, Sales = 100000, SalesAdjustment = 1.5,  Department = "EMEA Sales"};
var e2 = new Employee {Name = "Alice", Age = 52, Sales = 300000, SalesAdjustment = 1.02, Department = "Partner Sales"};
var e3 = new Employee {Name = "Marcus", Age = 42, Sales = 250000, SalesAdjustment = 1.1, Department = "NA Sales"};
var e4 = new Employee {Name = "Susan", Age = 27, Sales = 200000, SalesAdjustment = .95, Department = "EMEA Sales"};
var e5 = new Employee {Name = "John", Age = 38, Sales = 275000, SalesAdjustment = .9, Department = "APAC Sales"};
var e6 = new Employee {Name = "Theresa", Age = 30, Department = "EMEA Ops"};
employees.Insert(e1);
employees.Insert(e2);
employees.Insert(e3);
employees.Insert(e4);
employees.Insert(e5);
employees.Insert(e6);
```

### The AggregationResult

The Aggregations pipeline is all built around the `RedisAggregationSet<T>` this Set is generic, so you can provide the model that you want to build your aggregations around (an Indexed type), but you will notice that the return type from queries to the `RedisAggregationSet` is the generic type passed into it. Rather it is an `AggregationResult<T>` where `T` is the generic type you passed into it. This is a really important concept, when results are returned from aggregations, they are not hydrated into an object like they are with queries. That's because Aggregations aren't meant to pull out your model data from the database, rather they are meant to pull out aggregated results. The AggregationResult has a `RecordShell` field, which is ALWAYS null outside of the pipeline. It can be used to build expressions for querying objects in Redis, but when the AggregationResult lands, it will not contain a hydrated record, rather it will contain a dictionary of Aggregations built by the Aggregation pipeline. This means that you can access the results of your aggregations by indexing into the AggregationResult.

### Simple Aggregations

Let's try running an aggregation where we find the Sum of the sales for all our employees in EMEA. So the Aggregations Pipeline will use the `RecordShell` object, which is a reference to the generic type of the aggregation set, for something as simple as a group-less SUM, you will simply get back a numeric type from the aggregation.

```csharp
var sumOfSalesEmea = employeeAggregations.Where(x => x.RecordShell.Department == "EMEA")
    .Sum(x => x.RecordShell.Sales);
Console.WriteLine($"EMEA sold:{sumOfSalesEmea}");
```

The `Where` expression tells the aggregation pipeline which records to consider, and subsequently the `SUM` expression indicates which field to sum. Aggregations are a rich feature and this only scratches the surface of it, these pipelines are remarkably flexible and provide you the ability to do all sorts of neat operations on your Data in Redis.

### Apply functions

Apply functions are functions that you can define as expressions to apply to your data in Redis. In essence, they allow you to combine your data together, and extract the information you want.

#### Apply functions data model

For the remainder of this article we will be using this data model:

```csharp
[Document]
public class Employee
{
    [Indexed(Aggregatable = true)]
    public string Name { get; set; }

    [Indexed]
    public GeoLoc? HomeLoc { get; set; }

    [Indexed(Aggregatable = true)]
    public int Age { get; set; }

    [Indexed(Aggregatable = true)]
    public double Sales { get; set; }

    [Indexed(Aggregatable = true)]
    public double SalesAdjustment { get; set; }

    [Searchable(Aggregatable = true)]
    public string Department { get; set; }

    [Indexed(Aggregatable = true)]
    public long LastOnline { get; set; } = DateTimeOffset.UtcNow.ToUnixTimeSeconds();
}
```

#### Anatomy of an apply function

`Apply` is a method on the `RedisAggregationSet<T>` class which takes two arguments, each of which is a component of the apply function.

First it takes the expression that you want Redis to execute on every record in the pipeline, this expression takes a single parameter, an `AggregationResult<T>`, where `T` is the generic type of your `RedisAggregationSet`. This AggregationResult has two things we should think about, first it contains a `RecordShell` which is a placeholder for the generic type, and secondly it has an `Aggregations` property - which is a dictionary containing the results from your pipeline. Both of these can be used in apply functions.

The second component is the alias, that's the name the result of the function is stored in when the pipeline executes.

#### Adjusted sales

Our data model has two properties related to sales, `Sales`, how much the employee has sold, and `SalesAdjustment`, a figure used to adjust sales based off various factors, perhaps territory covered, experience, etc. . . The idea being that perhaps a fair way to analyze an employee's performance is a combination of these two fields rather than each individually. So let's say we wanted to find what everyone's adjusted sales were, we could do that by creating an apply function to calculate it.

```csharp
var adjustedSales = employeeAggregations.Apply(x => x.RecordShell.SalesAdjustment * x.RecordShell.Sales,
    "ADJUSTED_SALES");
foreach (var result in adjustedSales)
{
    Console.WriteLine($"Adjusted Sales were: {result["ADJUSTED_SALES"]}");
}
```

#### Arithmetic apply functions

Functions that use arithmetic and math can use the mathematical operators `+` for addition, `-` for subtraction, `*` for multiplication, `/` for division, and `%` for modular division, also the `^` operator, which is typically used for bitiwise exclusive-or operations, has been reserved for power functions. Additionally, you can use many `System.Math` library operations within Apply functions, and those will be translated to the appropriate methods for use by Redis.

##### Available math functions

| **Function** | **Type** | **Description**                                                  | **Example**                      |
| ------------ | -------- | ---------------------------------------------------------------- | -------------------------------- |
| Log10        | Math     | yields the 10 base log for the number                            | `Math.Log10(x["AdjustedSales"])` |
| Abs          | Math     | yields the absolute value of the provided number                 | `Math.Abs(x["AdjustedSales"])`   |
| Ceil         | Math     | yields the smallest integer not less than the provided number    | `Math.Ceil(x["AdjustedSales"])`  |
| Floor        | Math     | yields the smallest integer not greater than the provided number | `Math.Floor(x["AdjustedSales"])` |
| Log          | Math     | yields the Log base 2 for the provided number                    | `Math.Log(x["AdjustedSales"])`   |
| Exp          | Math     | yields the natural exponent for the provided number (e^y)        | `Math.Exp(x["AdjustedSales"])`   |
| Sqrt         | Math     | yields the Square root for the provided number                   | `Math.Sqrt(x["AdjustedSales"])`  |

#### String functions

You can also apply multiple string functions to your data, if for example you wanted to create a birthday message for each employee you could do so by calling String.Format on your records:

```csharp
var birthdayMessages = employeeAggregations.Apply(x =>
    string.Format("Congratulations {0} you are {1} years old!", x.RecordShell.Name, x.RecordShell.Age), "message");
await foreach (var message in birthdayMessages)
{
    Console.WriteLine(message["message"].ToString());
}
```

##### List of string functions

| **Function** | **Type** | **Description**                                                                                                                                                                                                                                                                               | **Example**                                                                               |
| ------------ | -------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------- |
| ToUpper      | String   | yields the provided string to upper case                                                                                                                                                                                                                                                      | `x.RecordShell.Name.ToUpper()`                                                            |
| ToLower      | String   | yields the provided string to lower case                                                                                                                                                                                                                                                      | `x.RecordShell.Name.ToLower()`                                                            |
| StartsWith   | String   | Boolean expression - yields 1 if the string starts with the argument                                                                                                                                                                                                                          | `x.RecordShell.Name.StartsWith("bob")`                                                    |
| Contains     | String   | Boolean expression - yields 1 if the string contains the argument                                                                                                                                                                                                                             | `x.RecordShell.Name.Contains("bob")`                                                      |
| Substring    | String   | yields the substring starting at the given 0 based index, the length of the second argument, if the second argument is not provided, it will simply return the balance of the string                                                                                                          | `x.RecordShell.Name.Substring(4, 10)`                                                     |
| Format       | String   | Formats the string based off the provided pattern                                                                                                                                                                                                                                             | `string.Format("Hello {0} You are {1} years old", x.RecordShell.Name, x.RecordShell.Age)` |
| Split        | String   | Split's the string with the provided string - unfortunately if you are only passing in a single splitter, because of how expressions work, you'll need to provide string split options so that no optional parameters exist when building the expression, just pass `StringSplitOptions.None` | `x.RecordShell.Name.Split(",", StringSplitOptions.None)`                                  |

#### Time functions

You can also perform functions on time data in Redis. If you have a timestamp stored in a useable format, a unix timestamp or a timestamp string that can be translated from [strftime](http://strftime.org/), you can operate on them. For example if you wanted to translate a unix timestamp to YYYY-MM-DDTHH:MM::SSZ you can do so by just calling ApplyFunctions.FormatTimestamp on the record inside of your apply function. E.g.

```csharp
var lastOnline = employeeAggregations.Apply(x => ApplyFunctions.FormatTimestamp(x.RecordShell.LastOnline),
    "LAST_ONLINE_STRING");

foreach (var employee in lastOnline)
{
    Console.WriteLine(employee["LAST_ONLINE_STRING"].ToString());
}
```

##### Time functions available

| **Function**                   | **Type** | **Description**                                                                                               | **Example**                                                    |
| ------------------------------ | -------- | ------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| ApplyFunctions.FormatTimestamp | time     | transforms a unix timestamp to a formatted time string based off [strftime](http://strftime.org/) conventions | `ApplyFunctions.FormatTimestamp(x.RecordShell.LastTimeOnline)` |
| ApplyFunctions.ParseTime       | time     | Parsers the provided formatted timestamp to a unix timestamp                                                  | `ApplyFunctions.ParseTime(x.RecordShell.TimeString, "%FT%ZT")` |
| ApplyFunctions.Day             | time     | Rounds a unix timestamp to the beginning of the day                                                           | `ApplyFunctions.Day(x.RecordShell.LastTimeOnline)`             |
| ApplyFunctions.Hour            | time     | Rounds a unix timestamp to the beginning of current hour                                                      | `ApplyFunctions.Hour(x.RecordShell.LastTimeOnline)`            |
| ApplyFunctions.Minute          | time     | Round a unix timestamp to the beginning of the current minute                                                 | `ApplyFunctions.Minute(x.RecordShell.LastTimeOnline)`          |
| ApplyFunctions.Month           | time     | Rounds a unix timestamp to the beginning of the current month                                                 | `ApplyFunctions.Month(x.RecordShell.LastTimeOnline)`           |
| ApplyFunctions.DayOfWeek       | time     | Converts the unix timestamp to the day number with Sunday being 0                                             | `ApplyFunctions.DayOfWeek(x.RecordShell.LastTimeOnline)`       |
| ApplyFunctions.DayOfMonth      | time     | Converts the unix timestamp to the current day of the month (1..31)                                           | `ApplyFunctions.DayOfMonth(x.RecordShell.LastTimeOnline)`      |
| ApplyFunctions.DayOfYear       | time     | Converts the unix timestamp to the current day of the year (1..31)                                            | `ApplyFunctions.DayOfYear(x.RecordShell.LastTimeOnline)`       |
| ApplyFunctions.Year            | time     | Converts the unix timestamp to the current year                                                               | `ApplyFunctions.Year(x.RecordShell.LastTimeOnline)`            |
| ApplyFunctions.MonthOfYear     | time     | Converts the unix timestamp to the current year                                                               | `ApplyFunctions.MonthOfYear(x.RecordShell.LastTimeOnline)`     |

#### Geo distance

Another useful function is the `GeoDistance` function, which allows you computer the distance between two points, e.g. if you wanted to see how far away from the office each employee was you could use the `ApplyFunctions.GeoDistance` function inside your pipeline:

```csharp
var officeLoc = new GeoLoc(-122.064181, 37.377207);
var distanceFromWork =
    employeeAggregations.Apply(x => ApplyFunctions.GeoDistance(x.RecordShell.HomeLoc, officeLoc), "DistanceToWork");
await foreach (var element in distancesFromWork)
{
    Console.WriteLine(element["DistanceToWork"].ToString());
}
```

## Grouping and reductions with Redis OM .NET

Grouping and reducing operations using aggregations can be extremely powerful.

### What Is a Group

A group is simply a group of like records in Redis.

e.g.

```json
{
    "Name":"Susan",
    "Department":"Sales",
    "Sales":600000
}

{
    "Name":"Tom",
    "Department":"Sales",
    "Sales":500000
}
```

If grouped together by `Department` would be one group. When grouped by `Name`, they would be two groups.

### Reductions

What makes groups so useful in Redis Aggregations is that you can run reductions on them to aggregate items within the group. For example, you can calculate summary statistics on numeric fields, retrieve random samples, distinct counts, approximate distinct counts of any aggregatable field in the set.

### Using Groups and Reductions with Redis OM .NET

You can run reductions against an `RedisAggregationSet` either with or without a group. If you run a reduction without a group, the result of the reduction will materialize immediately as the desired type. If you run a reduction against a group, the results will materialize when they are enumerated.

#### Reductions without a Group

If you wanted to calculate a reduction on all the records indexed by Redis in the collection, you would simply call the reduction on the `RedisAggregationSet`

```csharp
var sumSales = employeeAggregations.Sum(x=>x.RecordShell.Sales);
Console.WriteLine($"The sum of sales for all employees was {sumSales}");
```

#### Reductions with a Group

If you want to build a group to run reductions on, e.g. you wanted to calculate the average sales in a department, you would use a `GroupBy` predicate to specify which field or fields to group by. If you want to group by 1 field, your lambda function for the group by will yield just the field you want to group by. If you want to group by multiple fields, `new` up an anonymous type in line:

```csharp
var oneFieldGroup = employeeAggregations.GroupBy(x=>x.RecordShell.Department);

var multiFieldGroup = employeeAggregations.GroupBy(x=>new {x.RecordShell.Department, x.RecordShell.WorkLoc});
```

From here you can run reductions on your groups. To run a Reduction, execute a reduction function. When the collection materializes the `AggregationResult<T>` will have the reduction stored in a formatted string which is the `PropertyName_COMMAND_POSTFIX`, see supported operations table below for postfixes. If you wanted to calculate the sum of the sales of all the departments you could:

```csharp
var departments = employeeAggregations.GroupBy(x=>x.RecordShell.Department).Sum(x=>x.RecordShell.Sales);
foreach(var department in departments)
{
    Console.WriteLine($"The {department[nameof(Employee.Department)]} department sold {department["Sales_SUM"]}");
}
```

| **Command Name**  | **Command Postfix**      | **Description**                                                                                                                                              |
| ----------------- | ------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Count             | COUNT                    | number of records meeting the query, or in the group                                                                                                         |
| CountDistinct     | COUNT_DISTINCT           | Counts the distinct occurrences of a given property in a group                                                                                               |
| CountDistinctish  | COUNT_DISTINCTISH        | Provides an approximate count of distinct occurrences of a given property in each group - less expensive computationally but does have a small 3% error rate |
| Sum               | SUM                      | The sum of all occurrences of the provided field in each group                                                                                               |
| Min               | MIN                      | Minimum occurrence for the provided field in each group                                                                                                      |
| Max               | MAX                      | Maximum occurrence for the provided field in each group                                                                                                      |
| Average           | AVG                      | Arithmetic mean of all the occurrences for the provided field in a group                                                                                     |
| StandardDeviation | STDDEV                   | Standard deviation from the arithmetic mean of all the occurrences for the provided field in each group                                                      |
| Quantile          | QUANTLE                  | The value of a record at the provided quantile for a field in each group, e.g., the Median of the field would be sitting at quantile .5                      |
| Distinct          | TOLIST                   | Enumerates all the distinct values of a given field in each group                                                                                            |
| FirstValue        | FIRST_VALUE              | Retrieves the first occurrence of a given field in each group                                                                                                |
| RandomSample      | RANDOMSAMPLE{NumRecords} | Random sample of the given field in each group                                                                                                               |

### Closing Groups

When you invoke a `GroupBy` the type of return type changes from `RedisAggregationSet` to a `GroupedAggregationSet`. In some instances you may need to close a group out and use its results further down the pipeline. To do this, all you need to do is call `CloseGroup` on the `GroupedAggregationSet` - that will end the group predicates and allow you to use the results further down the pipeline.

## Using geo filters in Redis OM .NET

A really nifty bit of indexing you can do with Redis OM is geo-indexing. To GeoIndex, all you need to do is to mark a `GeoLoc` field in your model as `Indexed` and create the index

```csharp
[Document]
public class Restaurant
{
    [Indexed]
    public string Name { get; set; }

    [Indexed]
    public GeoLoc Location{get; set;}

    [Indexed(Aggregatable = true)]
    public double CostPerPerson{get;set;}
}
```

So let's create the index and seed some data.

```csharp
// connect
var provider = new RedisConnectionProvider("redis://localhost:6379");

// get connection
var connection = provider.Connection;

// get collection
var restaurants = provider.RedisCollection<Restaurant>();

// Create index
await connection.CreateIndexAsync(typeof(Restaurant));

// seed with dummy data
 var r1 = new Restaurant {Name = "Tony's Pizza & Pasta", CostPerPerson = 12.00, Location = new (-122.076751,37.369929)};
var r2 = new Restaurant {Name = "Nizi Sushi", CostPerPerson = 16.00, Location = new (-122.057360,37.371207)};
var r3 = new Restaurant {Name = "Thai Thai", CostPerPerson = 11.50, Location = new (-122.04382,37.38)};
var r4 = new Restaurant {Name = "Chipotles", CostPerPerson = 8.50, Location = new (-122.0524,37.359719 )};
restaurants.Insert(r1);
restaurants.Insert(r2);
restaurants.Insert(r3);
restaurants.Insert(r4);
```

## Querying Based off Location

With our data seeded, we can now run geo-filters on our restaurants data, let's say we had an office (e.g. Redis's offices in Mountain View at `-122.064224,37.377266`) and we wanted to find nearby restaurants, we could do so by using a `GeoFilter` query restaurants within a certain radius, say 1 mile we can:

```csharp
var nearbyRestaurants = restaurants.GeoFilter(x => x.Location, -122.064224, 37.377266, 5, GeoLocDistanceUnit.Miles);
foreach (var restaurant in nearbyRestaurants)
{
    Console.WriteLine($"{restaurant.Name} is within 1 mile of work");
}
```

## Next steps

Now that you know how to model, store, and query .NET objects with Redis OM, explore these related tutorials:

- [.NET and Redis](/tutorials/develop/dotnet/) — learn the fundamentals of the StackExchange.Redis client that Redis OM builds on
- [API Caching with ASP.NET Core and Redis](/tutorials/develop/dotnet/aspnetcore/caching/basic-api-caching/) — add Redis-backed caching to your ASP.NET Core APIs
- [Rate Limiting in .NET with Redis](/tutorials/rate-limiting-in-dotnet-with-redis/) — implement rate limiting middleware using Redis
