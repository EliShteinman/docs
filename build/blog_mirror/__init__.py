"""Mirror the Redis blog into the docs site as Hugo content.

Much of what Redis publishes about its own architecture exists only on the
blog, so an air-gapped reader who follows one of the ~180 blog links in the
docs loses that material entirely. This package brings the posts inside.

The blog is not scraped. redis.io is a Sanity-backed site whose `production`
dataset is publicly readable, so the posts come across as structured content --
Portable Text, not HTML -- which is why a post lands here as 8 KB of markdown
instead of the 1.6 MB of Next.js payload its rendered page weighs.

Everything it writes is generated: `content/blog/` and `static/images/blog/`
are outputs, not sources. Re-running the sync reproduces them.
"""
