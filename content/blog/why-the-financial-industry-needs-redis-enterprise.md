---
title: "Why the Financial Industry Needs Redis Enterprise"
linkTitle: "Why the Financial Industry Needs Redis Enterprise"
url: "/blog/why-the-financial-industry-needs-redis-enterprise/"
description: "The financial industry faces massive challenges. Consumer expectations have increased while regulators have ramped up their scrutiny of financial institutions."
date: 2020-10-07
blogCategories:
- "Company"
authors:
- "Prasanna Rajagopal"
lastmod: 2025-03-27
hidden: true
---

*By Prasanna Rajagopal · Published 7 October 2020 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/a44793d0570fc2d3a19326791adcf8cf70987ed4-4793x2663.webp)

The financial industry faces massive challenges. Consumer expectations have increased while regulators have ramped up their scrutiny of financial institutions.

Consumers have many choices when it comes to meeting their financial needs and they expect real-time performance and fast decisions from their financial institutions. That puts immense [downward pressure on fees](https://www.citibank.com/mss/sa/flippingbook/2019/The-Struggle-is-Real-How-Asset-Managers-are-Coping-With-Fee-Pressure/3/) while increased volatility and competition is pressuring returns. Investment opportunities vanish as quickly as they appear.

At the same time, amidst the global pandemic and associated economic turmoil, central banks are holding [interest rates near zero](https://www.cnbc.com/2020/06/10/fed-holds-rates-near-zero-heres-what-that-means-for-your-wallet.html) and even discussing[ negative interest rates](https://www.bbc.com/news/business-54314971), which has affected[ net interest income](https://www.cnbc.com/2019/07/17/bank-of-america-shares-fall-after-cfo-warns-lower-rates-will-hit-net-interest-income-growth.html) and inflated asset prices. Financial institutions are responding by looking to improve profitability by making business decisions faster, for example by approving loans and credit applications more quickly.

At the center of these myriad challenges is the need for real-time data. Algorithmic and retail trading volumes have exploded, for example, and consumers now expect real-time data on their banking and brokerage applications, while an explosion in exchange traded funds (ETFs) has created arbitrage opportunities for authorized participants. To take advantage of these opportunities, financial institutions require a high-performance database that delivers sub-millisecond response times for reads and writes, stores data from dozens of data sources in multiple data models, and provides high availability and multi-layered security. [Redis Enterprise](/enterprise/)—built on the popular open-source Redis database—is the perfect tool to address these issues and help make banks competitive.

[Redis Enterprise ](/redis-enterprise/advantages/)can add value to every facet of finance. In this blog, I highlight use cases in three areas of the financial industry—risk modeling, apps for banking and brokerage, and solutions for buy-side institutions—that illustrate the power and potential that Redis Enterprise can bring to your financial institution.

## Redis Enterprise for financial modeling and risk assessment

Risk and financial modeling have always been an integral part of the industry. But now stricter regulations, increased complexity, and the large volume of transactions undertaken by many institutions make modeling a central tool.

Systems built on traditional relational databases can fall short when it comes to the streaming of market data and providing query answers in real time. Modern models must account for thousands (if not millions) of data points and transactions each day, deal with data in multiple formats such as time series for asset pricing and executed trades, JSON for details on each asset or trade, and so on. The complexity of storing and executing multiple risk models at the same time is difficult to architect in a relational database.

But that’s only part of the problem. Since the subprime mortgage crisis of 2007-2010, lawmakers have introduced regulations requiring banks to model their financial losses on loans and credit cards for various economic outcomes. The [stress tests of the U.S. banking system](https://www.federalreserve.gov/supervisionreg/stress-tests-capital-planning.htm) conducted by the Federal Reserve are an example of this type of risk assessment and modeling. This type of modeling has real implications for the bank’s capital requirements, to shareholders, and even to the economy. The results of these models can force banks to increase their loan-loss reserves, capital available to make new loans and thus earn a profit, or [constrain the bank’s ability to pay dividends or do share buybacks](https://www.marketwatch.com/story/fed-caps-bank-dividend-payments-and-suspends-share-buybacks-for-third-quarter-after-stress-tests-2020-06-25).

In response to the financial crisis, the [Financial Accounting Standards Board ](https://www.fasb.org/home)(FASB) introduced the [Current Expected Credit Loss](https://www.fasb.org/creditlosses&pf=true) (CECL) as the new standard to recognize expected losses. Companies must now be able to model and forecast losses for a multitude of economic outcomes.

Earlier this year, [PwC](https://www.pwc.com/us/en.html) noted that the COVID-19 pandemic is [putting this standard to the test in real time](https://www.pwc.com/us/en/cfodirect/accounting-podcast/cecl-faqs-amid-covid-19.html). The [FASB](https://www.fasb.org/home) intends to have companies recognize losses on a timely basis. As [Deloitte has pointed out](https://www2.deloitte.com/us/en/pages/audit/articles/us-current-expected-credit-losses-cecl-implementation-insights.html), new accounting standards usually impact just the accounting department and the software it uses. But CECL requires a robust credit-risk modeling, financial reporting, and governance model. The implementation of these standards and regulations must be underpinned by a robust, fast, and flexible data infrastructure. And these are just two examples of the importance of risk modeling in a financial institution.

With Redis Enterprise, you can be proactive in addressing your regulatory and compliance needs. Redis Enterprise can easily scale to store years of data on risk models in memory and score it in real time while [offering high-availability deployment models](/redis-enterprise/technology/highly-available-redis/) that ensure you are protected against data loss. Changes can be quickly applied and the results can be assessed in seconds or minutes whereas a traditional relational database could take hours to return results.

Significantly, Redis Enterprise can be described as a [multi-model database.](/redis-enterprise/multi-model/) You do not need a separate database management system for each model. For instance, detailed loan information for each loan can be stored in [JSON](/json/). Time-series data on past or expected losses for various economic scenarios can be [stored in Time Series](/blog/unlocking-timeseries-data-redis/). You can use [Probabilistic](/modules/redis-bloom/) to help detect unusual account activity.

## Customer engagement is the currency

In a recent [interview with Barron’s magazine](https://www.barrons.com/articles/microsofts-xbox-series-x-price-is-a-big-deal-for-consumers-and-inverstors-51599869069), Tim Stuart, CFO of Microsoft’s Xbox division, said: **“I like to talk about how engagement equals currency…”**. This summarizes the attitudes of today’s customers. They prize engagement over everything else.

With that in mind, consumer expectations from their financial institutions have never been higher. Their default mode of interaction is now via a mobile device—younger consumers [rarely visit a physical banking location](https://thefinancialbrand.com/66228/bank-credit-union-branch-traffic/). Consumers demand their apps be engaging to use and responsive to the touch. Mobile banking and brokerage apps now rank among the [most-used apps](https://www.prnewswire.com/news-releases/mobile-banking-one-of-top-three-most-used-apps-by-americans-2018-citi-mobile-banking-study-reveals-300636938.html) by consumers. These consumers demand real-time data about their financial status—at any time and in any location.

A sleek user interface is the minimum bar for a client-facing financial application. Getting the financial data to be responsive is a tougher data challenge. Many banks have built their banking applications on top of relational databases built for an era of few transactions and minimal customer queries. They weren’t designed for millions of customers constantly accessing their accounts and transacting millions of times.

In some cases, banks have improved the scalability of their relational databases by adding a cache. In other cases, they have upgraded to more expensive, specialized database hardware appliances to buy time. These architecture and hardware changes improve scalability, but often at the expense of increased cost, complexity, and management.

You can rethink your mobile application to be responsive, scalable, and highly available using Redis Enterprise. You can use Redis as [your primary database](/blog/goodbye-cache-redis-as-a-primary-database/) and thus reduce complexity while meeting your customers’ ever-increasing demands. When a customer makes a banking transaction or searches for an analyst’s opinion on a stock, [Search and Query](/redis-enterprise/technology/redis-search/)—a powerful text search and secondary indexing engine built on top of Redis—can provide real-time data.

## Redis Enterprise reduces latency for institutional investors

Asset managers have seen their management fees fall. Clients in search of superior returns eagerly switch from one firm to another. This has increased costs for asset managers as they must offer more incentives to attract investors.

Portfolio managers, meanwhile, must analyze thousands of investment opportunities each day to find the best investment ideas. The number of data sources that portfolio management software must deal with has exploded. Real-time risk analysis of a portfolio can be a challenging exercise. Managers want to see a real-time [Investment Book of Record](https://capitalmarketsblog.accenture.com/three-steps-building-powerful-investment-book-of-record) (IBOR) on their positions to make timely decisions during trading hours. Asset managers also have a need for net asset value (NAV) calculations during the trading hours. NAV calculations for ETFs are a good example of this. Generating an accurate IBOR or NAV during the trading day can be technically challenging without a data infrastructure that offers millisecond-level latency.

In today’s financial industry, milliseconds can make or break a trade. [Redis Enterprise](/redis-enterprise/advantages/) can ingest and process millions of data points per second with sub-millisecond latency. Calculating accurate position data in IBOR becomes a breeze at the speed of Redis. Redis Enterprise offers multiple modules such as Search and Query, Time Series, JSON, and others that make life easy for technology teams. Asset management firms can reduce the complexity of their technology stack, reduce cost, and make critical information available in real time to asset managers.

These three use cases represent just the tip of the iceberg when it comes to the value that Redis Enterprise can bring to your financial institution. Financial solutions can leverage Redis Enterprise to help reduce costs and friction when dealing with complex financial data from multiple sources and improve overall customer responsiveness while reducing the risks facing your enterprise.

To go deeper, read our whitepapers on [Building the Highway to Real-Time Financial Services](/docs/real-time-financial-services/) and [The Power of Personalization: Driving Digital Banking Success](/docs/power-of-personalization-driving-digital-banking-success/) and check out our case study on [Deutsche Börse](/case-studies/deutsche-borse/).

*Cover image via Chronis Yan on Unsplash*.
