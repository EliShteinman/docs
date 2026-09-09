---
title: "Groovy Datasets for Test Databases"
linkTitle: "Groovy Datasets for Test Databases"
url: "/blog/datasets-for-test-databases/"
description: "When you experiment with a new-to-you data science skill, you need some sort of data to work with. Why be boring?"
date: 2023-04-04
blogCategories:
- "Tech"
authors:
- "Esther Schindler"
lastmod: 2025-03-27
hidden: true
---

*By Esther Schindler · Published 4 April 2023 · updated 27 March 2025*

![Blog tile image](/images/blog/024e354370a5f7a6b06cd8e4c7f061e3b4b88757-772x550.webp)

**When you experiment with a new-to-you data science skill, you need some sort of data to work with. Why be boring?**

Teaching yourself new tech skills often requires a “starter project” and data to support that project. Your motivation for learning the new skill could be anything: [preparing for a career upgrade](/blog/future-proof-your-dev-career/), curiosity about a hot, new programming language, or an intent to better exploit features in an existing development environment.

Good starter projects – once you’re done with “[Hello, world](https://www.thesoftwareguild.com/blog/the-history-of-hello-world/),” – accomplish *some*thing, however trivial, even if they have nothing to do with work. You need to experiment with realistic coding scenarios, including edge-cases, so the starter project should represent the way you’ll use the tool in real life. On the other hand, you don’t want to spend months debugging a practice application.

Which is to say: Why not have fun? Choose a starter project that lets you *play*. In my past, such projects have included creating dungeon master tools, food co-op ordering systems, and software developer market research.

With that in mind, I offer several entertaining datasets for inspiration – from astronomy to science fiction to parking meter revenue – many of which support a range of data types. I like to think you’ll use them as you teach yourself about Redis features.

These datasets are all free to access, though a few require you to create a site login. They are downloadable (most are CSV) or accessible via an API. A lot of cool archives are designed for interactive search (such as the [Women and Gender Marginalized Composers Repertoire Database](https://www.boulangerinitiative.org/database/database-info), [Baseball Reference](https://www.baseball-reference.com/), or the [Tulsa Historical Society’s photo archive](https://tulsahistory.pastperfectonline.com/)), However, this list is for developers, not for people who like to scan fascinating data collections.

I haven’t explored the data in any depth, nor do I vouch for their accuracy. This is purely a pointer to useful resources and a source of many, many internet rabbit holes.

## Science fiction datasets

The [Star Trek API](http://stapi.co) provides a read-only model of all things Star Trek, including characters, performers, species, episodes, spacecrafts, books, astronomical objects, and video releases. For an idea of its scope, this dataset has information about 7,560 characters, 3,207 technology pieces, 2,497 locations, and 2,348 astronomical objects. Similar information is available from a shared Airtable with “[every official Star Trek book](https://www.airtable.com/universe/expsZ6vRPGwedtNfq/every-star-trek-book-ever?explore=true), audiobook, comic, episode, movie, and more.”

If your science fiction fandom lies elsewhere, you might choose the [Mutant Moneyball](https://rallyrd.com/mutant-moneyball-a-data-driven-ultimate-x-men/) project, which tracks comic book market data for individual X-Men characters’ financial value. The project’s [dataset](https://github.com/EliCash82/mutantmoneyball) has [decade-by-decade](https://github.com/EliCash82/mutantmoneyball/blob/main/MutantMoneyballOpenData.csv) statistics for 26 X-Men characters drawn from sales histories and pricing guides.

## Programming languages in all their glory

If you prefer to geek out with tech relevance, the [programming language database](https://pldb.com/) describes several thousand programming languages, including their file formats, communications protocols, and other related concepts. You get information on the year the language was announced, its technical features, creators, countries and communities of origin, relevant books and URLs, and popularity metrics.

## World music

For a different set of data characteristics, consult the [Global Jukebox](https://theglobaljukebox.org/), an interactive map, and its accompanying [compilation of datasets](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0275469#pone-0275469-t001). It’s focused on traditional songs from around the world, based on information collected by musicologist [Alan Lomax](https://archive.culturalequity.org/about). The [core dataset](https://github.com/theglobaljukebox/cantometrics), called Cantometrics, encodes “37 aspects of musical style for 5,776 traditional songs from 1,026 societies.”

## Coconut acoustics

This is my favorite find: the extracted acoustic signal features of tall Philippine coconut fruits. In the Philippines, it turns out, coconuts are classified manually into their maturity levels. “Traders often use their fingernails, knuckles, or the blunt end of the knife to tap the coconuts before assessing the sounds produced,” [write the study’s authors](https://www.sciencedirect.com/science/article/pii/S2352340923000549), who developed hardware and software to emulate that process. They used it to collect [acoustic signal data](https://data.mendeley.com/datasets/hxh8kd3snj) from 129 premature, mature, and overmature coconuts, each mechanically knocked on each of its three ridges.

This may be a good data source for AI or machine learning experimentation, particularly if you are interested in digital-signal processing or audio signal processing. Though really, we know the reason to look at this dataset is that you want to tell your friends, “I’m working on an application evaluating coconut acoustics.” I don’t blame you.

## Exploding stars

![exploding stars datasets](/images/blog/8604a4346ba94b8c4a9c1827b1bf519a977639e8-300x169.webp)

The University of Hawai’i released what it claims is [the largest catalog of exploding stars](https://zenodo.org/record/7317476#.ZBZePi-B1ei).” The largest data release of relatively nearby supernovae (colossal explosions of stars), containing three years of data from the University of Hawaii Institute for Astronomy’s (IfA) Pan-STARRS telescope atop Haleakalā on Maui, is publicly available via the Young Supernova Experiment,” [reports the university](https://www.hawaii.edu/news/2023/03/15/largest-catalog-exploding-stars/). The data contains information on nearly 2,000 supernovae and other luminous variable objects with observations in multiple colors, and also extensively uses multi-color imaging to classify the supernovae and estimate their distances.

## Literary prizes

If you want a bookish application for your sample project, build on the [Post45 Data Collective](https://data.post45.org/)’s dataset of [major literary prizes](https://view.data.post45.org/mlpwinners). It has more than 7,100 “winners and judges of prizes for prose, poetry, or unspecified genre between 1918 and 2020 with a purse of $10,000 and over.” The data represent 50 awards and fellowships, plus the Library of Congress’s poet laureateship. This dataset is heavily text-based, with entries including the prize name, institution, type, genre, year, and dollar amount, among other fields.

If you are looking for less literary text-based data, consider the [Dad Jokes API](https://fatherhood.gov/jsonapi/node/dad_jokes) managed by the [national responsible fatherhood clearinghouse](https://fatherhood.gov/).

## FIFA World Cup

The [Fjelstul World Cup Database](https://github.com/jfjelstul/worldcup) covers 22 men’s World Cup tournaments from 1930-2022. The database includes 27 datasets that cover all aspects of the event, accounting for about 1.1 million data points. (I’d say more about this one, but you all know that I’m a baseball girl. I do note that Brazil is the only team with five World Cups.)

## Swiss apartment layouts

Maybe you plan to work with spatial and architectural data? The [Swiss Dwellings dataset](https://zenodo.org/record/7716698#.ZCCfoy-B1eg) contains detailed data on over 42,500 apartments (250,000 rooms) in about 3,100 buildings, including their geometries and room typology as well as the apartments’ visual, acoustical, topological, and daylight characteristics. It also has location-specific characteristics for the buildings, including climatic data and points of interest within walking distance.

## Datasets are a girl’s best friend

If you’re interested in gem quality, [diamond pricing](https://www.thediamondauthority.org/the-diamond-grading-system/), or merely a good-sized dataset for your sample application to chew on, consider this [diamond dataset](https://www.kaggle.com/datasets/hrokrin/the-largest-diamond-dataset-currely-on-kaggle). It has information on about 220,000 diamonds, with 25 columns of data including fluor (measuring the effect of longwave UV light), the stone’s measurements, and the total sales price. That should add a bit of sparkle to your analysis.

## Bird locations

Vendors sometimes offer (anonymized) data for public use and analysis. For instance, in addition to a cool world map that shows you live bird pictures that are taken with the company’s smart bird feeder, you can download [Bird Buddy](https://live.mybirdbuddy.com/)’s monthly datasets with longitude, latitude, and species name. Surely you can build a geospatial application that incorporates a northern cardinal, tufted titmouse, and red-headed woodpecker?

Another example that’s less visually attractive comes from BackBlaze, which regularly provides reports about true hard drive failure rates based on its extensive hardware use – 231,309 hard drives at the end of 2022. In addition to its own [in-depth analysis](https://www.backblaze.com/blog/backblaze-drive-stats-for-2022/), the company also provides [its source data](https://www.backblaze.com/b2/hard-drive-test-data.html).

## Government and municipal data

Open-data policies made it easy to find and download datasets that government agencies collect or generate. And it’s a *lot* of data. The [U.S. government](https://data.gov/) has a data search site where you can look for statistics on a wide range of topics, such as [healthcare](/industries/healthcare/), car sales, and sensor data gathered from agricultural farm use. Whether any of these qualify as “cool datasets” is an exercise left to the user – but they often are large enough to be useful for experimental programming, and some have unique data types.

For instance, if you are exploring geospatial database features, you might want to use a data set that includes location data. One such example is the 31 million parking meter receipts collected since 2015 by the city of [Arlington, Virginia](https://data.arlingtonva.us/dataset/148), which includes where the meter is as well as the monies paid ($68.6 million dollars in revenue, if you are keeping score).

Similarly, the City of Los Angeles publishes the [location and orientation of more than 50,000 stop signs](https://geohub.lacity.org/datasets/lahub::stop-and-yield-signs/about); you can find similar information for [Houston](https://geohub.houstontx.gov/datasets/625faeaffe924a0c968f216bf3c321fc_1/about), [San Francisco](https://data.sfgov.org/Transportation/Stop-Signs/4542-gpa3), and [Detroit](https://data.detroitmi.gov/datasets/detroitmi::traffic-sign-locations/about). Some datasets, such as from [OpenStreetMap](https://www.openstreetmap.org/), are available through an API as well as downloadable files; if you can think of something to do with information about [1.4 million stop signs](https://wiki.openstreetmap.org/wiki/Tag:highway%3Dstop) around the world, you can do so with ease.

## Choose a dataset to support your tool exploration

I like to think that these datasets can help you expand your database skills – particularly as you explore what you can accomplish with Redis features such as [search](/search/), [gaming leaderboards](/solutions/leaderboards/), [vector similarity search](/solutions/vector-search/), [time series](/timeseries/), and [geospatial](/glossary/geospatial-indexing/) capabilities. Choose datasets that match the application domain you want to learn about.

For example, if you want to experiment with database processing that incorporates geospatial analysis, your sample data need location data (birds! Stop signs!). To expand your knowledge of database search features (because ultimately, you want to speed up internal searches in production databases), choose a huge dataset (stars! diamonds!); your performance testing needs something to work with. Pick a numbers-heavy dataset when you want to learn how to create data visualizations that make everyone say, “Oooh!” And so on.

### This isn’t silly. It’s a wise business choice

Don’t feel foolish about choosing one of these datasets. It’s a bad idea to use existing internal data for a starter project. Banging on real customer data raises privacy concerns, particularly when you aren’t using it for the reasons it was gathered.

You certainly cannot use real information when you speak at an industry conference. But you can entertain and engage an audience when you describe the [graph database essentials in the context of Dungeons and Dragons](/blog/redisgraph-and-redis/). Mental models help us reframe our knowledge with familiar examples, turning abstract functions into practical analysis.

And, speaking from personal experience, if your intent is to show the boss a technology proof-of-concept (“Here’s what we could accomplish if we deployed this database feature!”), they could be distracted by the “real” data. (True story. A user saw the output of a “play with the tool” experiment – “show a graph of hotel reservations made, displayed by the day of the week” – and said, “Oh, can I get a copy of this report monthly?”)

## Need more? This is just a start

If you’re interested in collecting datasets (oh look, a dataset of datasets!), I highly recommend the [Data is Plural](https://buttondown.email/data-is-plural) newsletter, which I drew on liberally to inform my suggestions. You also should visit and subscribe to [ResearchBuzz](https://researchbuzz.me/), which shares dataset descriptions as well as archive-related news and tools (a recent example: [Turn Wikipedia into an RSS Search Engine With WikiRSS](https://researchbuzz.me/2023/03/20/turn-wikipedia-into-an-rss-search-engine-with-wikirss/)). Google Research maintains [a search site for test datasets](https://datasetsearch.research.google.com/), too, if you know what you’re looking for.

If you use any of these datasets in your personal projects, please [tell me about them](https://hachyderm.io/@estherschindler)!
