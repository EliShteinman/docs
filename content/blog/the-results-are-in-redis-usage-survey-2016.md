---
title: "The Results Are In – Redis Usage Survey 2016!"
linkTitle: "The Results Are In – Redis Usage Survey 2016!"
url: "/blog/the-results-are-in-redis-usage-survey-2016/"
description: "Over Oct and Nov, Redis conducted two surveys on Redis usage. One survey was of Redis customers, conducted by TechValidate, who provides third-party validation of the results. A second survey was..."
date: 2016-12-14
blogCategories:
- "Tech"
authors:
- "Leena Joshi"
lastmod: 2025-03-04
hidden: true
---

*By Leena Joshi, VP Product Marketing · Published 14 December 2016 · updated 4 March 2025*

![Blog tile image](/images/blog/91cea322547515c914b3f12502653182ccf7cad4-635x200.webp)

![](/images/blog/91cea322547515c914b3f12502653182ccf7cad4-635x200.webp)

Over Oct and Nov, Redis conducted two surveys on Redis usage. One survey was of Redis customers, conducted by TechValidate, who provides third-party validation of the results. A second survey was done through SurveyMonkey and was mostly promoted to open source Redis users. The two surveys yielded many similarities and differences, highlighted in the details. But to keep the line clear between validated input from Redis’ customers and general input from a larger audience, we divide this into two blog posts.

- [TechValidate Results – How Redis’ customers are using Redis](/blog/redis-labs-customers-award-accolades)
- SurveyMonkey Results – Redis Usage Survey

## SurveyMonkey Results: How Redis Users Use Redis

Some notes on this survey – this survey was promoted to the community via various channels, and 80% of the folks who took this survey are open source redis users. A link to the full results is [here](https://www.surveymonkey.com/results/SM-HCBY978F/), but in the interest of protecting the privacy of the survey takers, it is password protected. I will do my best to make the results clear in this blog post. ( but interested parties may contact me for additional insights). So 96 folks took this survey, and 80% of them were OSS Redis users.

![](/images/blog/247b1541b4c43aeccc09f312b66f70a244429e28-650x483.webp)

We asked the Redis use cases question, with more options than last year – and we see the results below:

![](/images/blog/3b3014634ef3f35486f140b1e3b12ff18d5ab3ef-595x752.webp)

![](/images/blog/577c972510885dea7c9de9442ddea66a3cbb6e69-595x583.webp)

Compared to [last year’s results](/blog/how-redis-is-used-in-practice), we see a distinct uptick in use cases such as job & queue management, and real-time analytics but we also see substantial usage as a user session store, for high-speed transactions, notifications, distributed lock, and even machine learning! (we hadn’t asked precisely this last year – I was still new ☺). We were more successful in unearthing the broad range of uses that Redis supports this year as compared to last!

The industry-wide applicability of Redis remains broad as ever, but this time around there were distinct mentions from customers of IoT, bots, meteorology, environmental data and much more.

![](/images/blog/242d648ab44a40ca8ba483c747c05d951b620109-650x887.webp)

The next question was asked slightly differently from the Techvalidate survey ( I neglected to include a tier for mobile applications!). Other than that, the responses line up pretty closely. I had also mistakenly included caching in here, I have excluded those responses since we already caught the content caching in the above question.

### Q3: What type of solution are you using Redis in? (Choose multiple options if applicable)

### 

![](/images/blog/87150276ce51e47cd275a0bc414b0bbb71cf9095-595x371.webp)

Similar to the Redis users, when asked, “Is Redis used for data not stored in any other database”, about 67% of survey respondents use Redis as their primary datastore for some of their data.

![](/images/blog/fceed17358fbf1ea7e1571b7e33753b085394e67-595x321.webp)

When asked “Do you want to increase your Redis usage”, about 90% of users intend to increase their Redis usage, and they want to for similar reasons as the TechValidate survey.

Reasons for increasing Redis usage are below:

![](/images/blog/9ee3133195982b3d9cf54585d3e2c302276fc553-595x411.webp)

![](/images/blog/00f89e66d078a50ad181f237fa8ba6c4db24cd80-595x243.webp)

There are few conclusions to draw about Redis usage from both surveys:

- Redis is used broadly across a range of industries and use cases
- Redis usage continues to grow, especially as application usage and data processing needs are growing
- Redis is being used as a primary datastore and increasingly so, compared to last year

If you have additional questions about either of the surveys, you can always reach me on twitter ([@socialeena](http://www.twitter.com/socialeena)).
